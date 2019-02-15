import threading
import time
import random
import sys
import socket

def server():
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    server_binding = ('', 50007)
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))
    csockid, addr = ss.accept()
    print ("[S]: Got a connection request from a client at {}".format(addr))
    
    # Receive client msg
    data_from_server=csockid.recv(100)
    print("[C]: Data received from client: {}".format(data_from_server.decode('utf-8')))
    
    # Send reversed string
    msg = reverse(data_from_server.decode('utf-8'))
    csockid.send(msg.encode('utf-8'))

    # Close the server socket
    ss.close()
    exit()

def reverse(msg):
	return msg[::-1]

if __name__ == "__main__":
    t1 = threading.Thread(name='server', target=server)
    t1.start()

    time.sleep(5)
    print("Done.")
    #Exit program
    sys.exit(0)
