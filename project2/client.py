import threading
import time
import random
import sys, os
import socket

def client(rsHostName, rsListenPort, hostNames):
    global outputString
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
    try:
        cs.connect(server_binding)
    except Exception as e:
        print(e)
        cs.close()
        exit()
        
    # send and receive data
    outputResults(cs, hostNames)
    # close the client socket
    try:
        os.remove('RESOLVED.txt')
    except OSError:
        pass
        
    output = open("RESOLVED.txt", "a+")
    #print(outputString)
    output.write(outputString)
    output.close()
    cs.close()
    exit()

def outputResults(cs, hostNames):
    global outputString
    for host in hostNames: 
        # Send data to the server
        data_to_server=cs.send(host.encode('utf-8'))
        print("[C]: Data sent to TServer: {}".format(host))

	      #Receive data from the server
        data_from_server=cs.recv(100)
        msg_rcv = data_from_server.decode('utf-8')
        print("[C]: Data received from TServer: {}".format(msg_rcv))
        
        if (not(format(msg_rcv) == 'END')):
            outputString = outputString + format(msg_rcv) + '\n'


def getAllHostNamesFromFile():
    fileName = open('PROJ2-HNS.txt')
    hostNames = []
    for line in fileName.readlines():
        hostNames.append(line.rstrip())
    hostNames.append('END')
    fileName.close()
    return hostNames

if __name__ == "__main__":
    global outputString
    outputString = ''
    if (len(sys.argv) is not 3 or not sys.argv[2].isdigit()):
        print("Please enter valid parameter syntax")
        sys.exit(0)
        
    hostNames = getAllHostNamesFromFile()
  
    time.sleep(random.random() * 5)
    t2 = threading.Thread(name='client', target=client, args=([sys.argv[1], sys.argv[2], hostNames]))
    t2.start()

    time.sleep(20)
    print("Done.")
    #Exit program
    sys.exit(0)
    os._exit(0)
