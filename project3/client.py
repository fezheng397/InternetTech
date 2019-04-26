import threading
import time
import random
import sys, os
import socket
import hmac
import re

def client(asHostName, asListenPort, hostNames, ts1ListenPort, ts2ListenPort):
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('[ERROR]: Socket open error: {} \n'.format(err))
        exit()
        
    # Define the port on which you want to connect to the server
    port = int(asListenPort)
    localhost_addr = asHostName

    # connect to the server on local machine
    server_binding = (localhost_addr, port)
    try:
        cs.connect(server_binding)
    except Exception as e:
        print('[ERROR]: Connection error: {} \n'.format(e))
        cs.close()
        exit()
        
    # send and receive data
    ts_list = communicateWithAS(cs, hostNames)
    
    communicateWithTS(ts_list, ts1ListenPort, ts2ListenPort)
    
    exit()

def communicateWithAS(cs, hostNames):
    count = 0
    ts_list = []
    for host in hostNames: 
		# Send data to the server
        wordList = host.split()
        if (len(wordList) != 3):
            print("[ERROR]: Input is formatted incorrectly, please fix the file and try again.")
            cs.close()
            exit()
        
        key = wordList[0]
        challenge = wordList[1]
        digest = (hmac.new(key.encode("utf-8"), challenge.encode("utf-8"))).hexdigest()
        sentString = challenge + " " + digest
        
        data_to_server=cs.send(sentString.encode("utf-8"))
        print("[C]: Data sent to AServer: {}".format(sentString))

	    #Receive data from the server
        data_from_server=cs.recv(100)
        msg_rcv = data_from_server.decode('utf-8')
        print("[C]: Data received from AServer: {}".format(msg_rcv))
        
        if (msg_rcv is not 'END'):
            ts_list.append(msg_rcv + " " + str(count) + " " + wordList[2])
        count = count + 1
            
    return ts_list
    
def communicateWithTS(ts_list, ts1ListenPort, ts2ListenPort):
    final_list = []
    ts1_list = []
    ts2_list = []
    for ts_string in ts_list:
        ts_strings = ts_string.split()
        if (ts_strings[0] == 'TS1'):
            ts1_list.append(ts_string)
        else:
            ts2_list.append(ts_string)
    
    if (len(ts1_list) is not 0):
        ts1_host = ts1_list[0].split()[1]
        ts1_list.append('TS1 ' + ts1_host + ' -1 END')
        
    if (len(ts2_list) is not 0):
        ts2_host = ts2_list[0].split()[1]
        ts2_list.append('TS2 ' + ts2_host + ' -1 END')
        
    final_list = clientTS(ts1_list, ts1ListenPort, final_list)
    final_list = clientTS(ts2_list, ts2ListenPort, final_list)
    
    try:
        os.remove('RESOLVED.txt')
    except OSError:
        pass
        
    output = open("RESOLVED.txt", "a+")
    final_list.sort(key=getOrder)
    outputString = ''
    for item in final_list:
        outputString = outputString + item[0] + '\n'
    output.write(outputString)
    output.close()
    
def clientTS(ts_list, portStr, outputList):
    for ts_string in ts_list:
        ts_strings = ts_string.split()
        try:
            cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #print("[C]: Client socket created")
        except socket.error as err:
            print('[ERROR]: Socket open error: {} \n'.format(err))
            exit()
            
        # Define the port on which you want to connect to the server
        port = int(portStr)
        localhost_addr = ts_strings[1]

        # connect to the server on local machine
        server_binding = (localhost_addr, port)
        try:
            cs.connect(server_binding)
        except Exception as e:
            print('[ERROR]: Connection error: {} \n'.format(e))
            cs.close()
            exit()
            
        data_to_server=cs.send(ts_strings[3].encode("utf-8"))
        print("[C]: Data sent to TServer: {}".format(ts_strings[3]))

	      #Receive data from the server
        data_from_server=cs.recv(100)
        msg_rcv = data_from_server.decode('utf-8')
        print("[C]: Data received from TServer: {}".format(msg_rcv))
        if (format(msg_rcv) != 'END'):
            outputTuple = [msg_rcv, ts_strings[2]]
            outputList.append(outputTuple)
        cs.close()
    return outputList
            
       
def getOrder(x):
    return x[1]
    
def getAllHostNamesFromFile():
    fileName = open('PROJ3-HNS.txt')
    hostNames = []
    for line in fileName.readlines():
        hostNames.append(line.rstrip())
    fileName.close()
    return hostNames

if __name__ == "__main__":
    if (len(sys.argv) is not 5 or not sys.argv[2].isdigit() or not sys.argv[4].isdigit()):
        print("[ERROR]: Please enter valid parameter syntax")
        sys.exit(0)
        
    hostNames = getAllHostNamesFromFile()
  
    time.sleep(random.random() * 5)
    t2 = threading.Thread(name='client', target=client, args=([sys.argv[1], sys.argv[2], hostNames, sys.argv[3], sys.argv[4]]))
    t2.start()

    time.sleep(30)
    print("Done.")
    #Exit program
    sys.exit(0)
    os._exit(0)


