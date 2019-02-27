import threading
import time
import random
import sys, os
import socket

def client(rsHostName, rsListenPort, hostNames, rsConnection):
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
    
    # send and receive data
    if rsConnection:
        interpretRSConnection(cs, hostNames)
        # close the client socket
        cs.close()
        exit()
    else:
        outputResults(cs, hostNames)

    
def interpretRSConnection(cs, hostNames):
    for host in hostNames: 
        # Send data to the server
        data_to_server=cs.send(host.encode('utf-8'))
        print("[C]: Data sent to RServer: {}".format(host))

	      #Receive data from the server
        data_from_server=cs.recv(100)
        msg_rcv = data_from_server.decode('utf-8')
        print("[C]: Data received from RServer: {}".format(msg_rcv))
        if msg_rcv == 'END':
            print("Close TS")
            client(tsHostName, sys.argv[3], ['END'], False)
            break
        elif msg_rcv[-2:] == 'NS':
            print(msg_rcv[:-5])
            tsHostName = msg_rcv[:-5]
            print("TS Port Num: " + str(sys.argv[3]))
            client(tsHostName, sys.argv[3], [host], False)
            
def outputResults(cs, hostNames):
    for host in hostNames: 
        # Send data to the server
        data_to_server=cs.send(host.encode('utf-8'))
        print("[C]: Data sent to TServer: {}".format(host))

	      #Receive data from the server
        data_from_server=cs.recv(100)
        msg_rcv = data_from_server.decode('utf-8')
        print("[C]: Data received from TServer: {}".format(msg_rcv))
        
    cs.close()
    #exit()
    
def getAllHostNamesFromFile():
    fileName = open('PROJI-HNS.txt')
    hostNames = []
    for line in fileName.readlines():
        hostNames.append(line.rstrip())
    hostNames.append('END')
    fileName.close()
    return hostNames

if __name__ == "__main__":

    if (len(sys.argv) is not 4 or not sys.argv[2].isdigit() or not sys.argv[3].isdigit()):
        print("Please enter valid parameter syntax")
        sys.exit(0)
        
    hostNames = getAllHostNamesFromFile()
  
    time.sleep(random.random() * 5)
    t2 = threading.Thread(name='client', target=client, args=([sys.argv[1], sys.argv[2], hostNames, True]))
    t2.start()

    time.sleep(15)
    print("Done.")
    #Exit program
    sys.exit(0)
    os._exit(0)
