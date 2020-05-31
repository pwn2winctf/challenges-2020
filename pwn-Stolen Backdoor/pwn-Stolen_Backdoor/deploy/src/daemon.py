#!/usr/bin/python3
import threading
import traceback
import socket
import time
import collections
import os
import subprocess
import psutil


HOST=os.getenv("HOST")
PORT=int(os.getenv("PORT"))
NUSERS=int(os.getenv("NUSERS"))
TIME_TO_SLEEP=float(os.getenv("TIME_TO_SLEEP"))
TIMEOUT=float(os.getenv("TIMEOUT"))
INTERVAL_PER_IP=float(os.getenv("INTERVAL_PER_IP"))
MINIMUM_FREQ=float(os.getenv("MINIMUM_FREQ"))
ALLOWED_IP=os.getenv("ALLOWED_IP").split(",")
BLOCKED_IP=os.getenv("BLOCKED_IP").split(",")
MAX_FILE_SIZE=int(os.getenv("MAX_FILE_SIZE"))

print("""[INFO] Starting server in %s:%s
[INFO] TIMEOUT=%f
[INFO] NUSERS=%i
[INFO] TIME_TO_SLEEP=%f
[INFO] INTERVAL_PER_IP=%f
[INFO] MINIMUM_FREQ=%f
[INFO] ALLOWED_IP=%s
[INFO] BLOCKED_IP=%s
[INFO] MAX_FILE_SIZE=%i
"""%(HOST,PORT,TIMEOUT,NUSERS,TIME_TO_SLEEP,INTERVAL_PER_IP,MINIMUM_FREQ,ALLOWED_IP,BLOCKED_IP,MAX_FILE_SIZE))

#important for the challenge, check it on server
os.system("head /proc/cpuinfo")

class connList(list):
    def pop(self, *args, **kwargs):
        ret=list.pop(self,*args,**kwargs)
        try:
            self.showQueue()
        except:
            pass
        return ret 

    def showQueue(self):
        for i in range(len(self)):
            self[i]["socket"].sendall(b"Position in queue: %i\n"%(i+1))
    

def recvall(sock, n,addr):
    start=time.time()
    data = b""
    loops=0
    while len(data) < n:
        #sock.settimeout(TIMEOUT)
        packet = sock.recv(n - len(data))
        if not packet:
            return b""
        data+=packet
        freq=len(data)/(time.time()-start)
        if freq < MINIMUM_FREQ and loops > 3:
            #avoid ddos with slow loris-like attacks
            print("[INFO] Frequency is too slow, maybe a slow attack! possible attacker:%s\n"%addr)
            sock.sendall(b"Wow, youre sending your file too slow. Dont waste my time!\n")
            raise socket.timeout
        loops+=1

    return data




class server:
    def __init__(self):
        
        self.todo=connList()
        self.antispam={}

        self.sem = threading.Semaphore()

        threading.Thread(target=self.runner).start()

        self.server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #self.server.settimeout(TIMEOUT)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((HOST,PORT))
        self.server.listen(NUSERS)

        self.mainloop()


    def execute(self,bytesarg):

        os.system("rm -rf /tmp/*")
        os.system("/home/manager/clean")        
    
        with open("/tmp/executable.bin","wb") as f:
            f.write(bytesarg)


        os.system("chmod +x /tmp/executable.bin")

        start=time.time()
        with open("/tmp/output.txt","wb") as f:
            backdoor=subprocess.Popen("su -m butcher -c \"/tmp/executable.bin\"",stdout=f,stderr=f,shell=True)
        
            try:
                backdoor.wait(timeout=TIME_TO_SLEEP)
            except subprocess.TimeoutExpired: 
                print("[INFO] Process terminated by force.")



        print("[INFO] Job executed in %f seconds"%(time.time()-start))        
        os.system("/home/manager/clean")    

        resp=b""
        with open("/tmp/output.txt","rb") as f:
            resp+=f.read(10000)
        
        os.system("rm -rf /tmp/*")

        return resp


    
    def runner(self):
        while True:
            try:
                if len(self.todo)>0:
                    self.sem.acquire()
                    job=self.todo.pop(0)
                    self.sem.release()

                    conn=job["socket"]
                    payload=job["payload"]
                    #conn.sendall(b"Executing your file...\n")

                    print("[INFO] Running job!")
                    resp=self.execute(payload)
                    conn.sendall(b"Here are the first 10000 bytes of your output:\n")
                    conn.sendall(resp)
                    conn.close()

                else:
                    time.sleep(0.1)
            except:
                print("[ERROR] RUNNER CRASHED!")
                traceback.print_exc()

    def warpWelcome(self,conn,addr):
        try:
            self.welcome(conn,addr)
             
        except socket.timeout:
            conn.sendall(b"Timeout reached. Bye!\n")
            conn.close()
        except IOError:
            print("[INFO] client disconected")
            

    def welcome(self,conn,addr):
        
        ip=addr[0]
        conn.settimeout(TIMEOUT)
        
        if ip in BLOCKED_IP:
            print("[INFO] BLOCKED IP tried to access: %s ."%ip)
            conn.sendall(b"Looks like you're blocked conntact an admin. Bye!\n")
            conn.close()
            return

        if (ip in self.antispam) and (not ip in ALLOWED_IP):
            dtime=time.time()-self.antispam[ip]
            if dtime < INTERVAL_PER_IP:
                print("[INFO] Repeated request made too quickly from same IP: %s ."%ip)
                conn.sendall(b"Wow, too fast! Try again after %i seconds!\n"%(INTERVAL_PER_IP -dtime))
                conn.close()
                return

        self.antispam[ip]=time.time()
        process = subprocess.Popen('ps -aux | grep encoder', stdout=subprocess.PIPE,shell=True)
        output = process.stdout.readline()

        conn.sendall(b"Hello there. Send me your ELF.\n")
        conn.sendall(b"ps -aux | grep encoder\n")
        conn.sendall(output)
        conn.sendall(b"Give me how many bytes (max: %i)\n"%MAX_FILE_SIZE)
        response=conn.recv(len(str(MAX_FILE_SIZE))+2)
        try:
            lenbytes=int(response)
        except:
            print("[INFO] Erro in size conversion.")
            conn.sendall(b"Error in size conversion. Bye!\n")
            conn.close()
            return

        if lenbytes>MAX_FILE_SIZE or lenbytes<=0:
            print("[INFO] Invalid number.")
            conn.sendall(b"invalid number. Bye!\n")
            conn.close()
            return
        else:
            conn.sendall(b"Send 'em!\n")
            payload=recvall(conn,lenbytes,ip)

        if payload[:4]!=b"\x7fELF":
            print("[INFO] Not ELF format.")
            conn.sendall(b"Not ELF. bye!\n")
            conn.close()
            return
        else:
            self.sem.acquire()
            pos=len(self.todo)+1
            self.todo.append({"socket":conn,"payload":payload})
            self.sem.release()
            conn.sendall(b"Position in queue: %i\n"%pos)
            return


    
    def mainloop(self):
        while 1:
            try:
                conn,addr = self.server.accept()
                print("[INFO] Connected with %s. Todo length: %i"%(addr,len(self.todo)))
                threading.Thread(target=self.warpWelcome,args=(conn,addr)).start()
            except Exception: 
                print("[ERROR] unkown Exception occurred")
                traceback.print_exc()
                


if __name__=="__main__":
    x=server()

