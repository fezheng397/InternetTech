import threading
import time
import random
import sys, os
import socket

def server(rsListenPort):
    print(rsListenPort)

    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    server_binding = (socket.gethostbyname(socket.gethostname()), int(rsListenPort))
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))
    csockid, addr = ss.accept()
    print ("[S]: Got a connection request from a client at {}".format(addr))
    
    '''
        Read file and create hashmap
            Hashmap Params:
                Key: Hostname
                Value: Tuple containing (IP Address, String)
    '''
    filename = 'PROJI-DNSRS.txt'
    file = open(filename, 'r')
    
    while True:
        # Receive client msg
        data_from_server=csockid.recv(200)
        print("[C]: Data received from client: {}".format(data_from_server.decode('utf-8')))
        if not data_from_server or data_from_server == 'END':
            print("[S]: Data from client: " + data_from_server)
            csockid.send('END'.encode('utf-8'))
            break
        
        # Send reversed string
        msg = reverse(data_from_server.decode('utf-8'))
        csockid.send(msg.encode('utf-8'))
        

    # Close the server socket
    ss.close()
    exit()

def reverse(msg):
	return msg[::-1]

if __name__ == "__main__":
    if(not sys.argv[1].isdigit()):
        print("Please enter an integer hostname")
        sys.exit(0)
    
    t1 = threading.Thread(name='server', target=server, args=([sys.argv[1]]))
    t1.start()

    time.sleep(20)
    print("Done.")
    #Exit program
    sys.exit(0)
    os._exit(0)
