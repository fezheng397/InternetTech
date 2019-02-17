import threading
import time
import random
import sys, os
import socket

def client(rsHostName, rsListenPort):
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()
        
    # Define the port on which you want to connect to the server
    port = int(rsListenPort)
    localhost_addr = rsHostName

    # connect to the server on local machine
    server_binding = (localhost_addr, port)
    cs.connect(server_binding)

    # Send data to the server
    msg_snt = 'PALINDROME_TEST_STRING'
    data_to_server=cs.send(msg_snt.encode('utf-8'))
    print("[C]: Data sent to server: {}".format(msg_snt))

	#Receive data from the server
    data_from_server=cs.recv(100)
    msg_rcv = data_from_server.decode('utf-8')
    print("[C]: Data received from server: {}".format(msg_rcv))

    # close the client socket
    cs.close()
    exit()
    
def getAllHostNamesFromFile():
    fileName = open('in-proj0.txt')
    hostNames = []
    for line in fileName.readlines():
        hostNames.append(line.rstrip())
    hostNames.append('END')
    fileName.close()
    return hostNames

if __name__ == "__main__":

    if (len(sys.argv) is not 3 or not sys.argv[2].isdigit()):
        print("Please enter valid parameter syntax")
        sys.exit(0)
        

    hostNames = getAllHostNamesFromFile()
    for line in hostNames:
      print(line)
    
    time.sleep(random.random() * 5)
    t2 = threading.Thread(name='client', target=client, args=([sys.argv[1], sys.argv[2]]))
    t2.start()

    time.sleep(15)
    print("Done.")
    #Exit program
    sys.exit(0)
    os._exit(0)
