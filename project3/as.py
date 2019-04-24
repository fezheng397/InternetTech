import threading
import time
import random
import sys, os
import socket

def server(asListenPort, ts1Hostname, ts1ListenPort_a, ts2Hostname, ts2ListenPort_a):
    print(asListenPort)

    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    server_binding = (socket.gethostbyname(socket.gethostname()), int(asListenPort))
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))
    csockid, addr = ss.accept()
    print ("[S]: Got a connection request from a client at {}".format(addr))
    #count = 0
    while True:
        #count = count + 1
        #print ("Count: " + str(count))
        # Receive client msg
        data_from_server=csockid.recv(200)
        print("[C]: Data received from client: {}".format(data_from_server.decode('utf-8')))
        if not data_from_server or data_from_server == 'END':
            print("[S]: Data from client: " + data_from_server)
            #msg = clientTS(ts1Hostname, ts1ListenPort_a, 'END')
            #msg = clientTS(ts2Hostname, ts2ListenPort_a, 'END')
            csockid.send('END'.encode('utf-8'))
            break
        
        data_from_server = data_from_server.split(' ')
        challengeStr = data_from_server[0]
        digest = data_from_server[1]
        
        ts1Res = clientTS(ts1Hostname, ts1ListenPort_a, challengeStr)
        ts2Res = clientTS(ts2Hostname, ts2ListenPort_a, challengeStr)
        if(ts1Res == digest):
            msg = "TS1 " + ts1Hostname
        elif(ts2Res == digest):
            msg = "TS2 " + ts2Hostname
        else:
            msg = 'Hostname - Error:HOST NOT FOUND'

        csockid.send(msg.encode('utf-8'))
        

    # Close the server socket
    ss.close()
    exit()

def clientTS(tsHostName, tsListenPort, hostname):
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: ClientTS socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()
        
    # Define the port on which you want to connect to the server
    port = int(tsListenPort)
    localhost_addr = tsHostName

    # connect to the server on local machine
    server_binding = (localhost_addr, port)
    try:
        cs.connect(server_binding)
    except Exception as e:
        print(e)
        cs.close()
        exit()
        
    # Send data to the server
    data_to_server=cs.send(hostname.encode('utf-8'))
    print("[C]: Data sent to TServer: {}".format(hostname))

    #Receive data from the server
    data_from_server=cs.recv(100)
    msg_rcv = data_from_server.decode('utf-8')
    print("[C]: Data received from TServer: {}".format(msg_rcv))
    
    # close the client socket
    cs.close()
    return msg_rcv


def readFile(filename):
    fileContent = []
    for line in filename.readlines():
        fileContent.append(line.rstrip())
    #fileContent.append('END')
    filename.close()
    return fileContent

def createConnections(rsConnections, fileContent):
    for connection in fileContent:
        substrings = connection.split(' ')
        if substrings[2] == 'NS':
            temp = substrings[0].split('.')
            #print (temp)
            if(temp[len(temp) - 1] == 'com'):
                #add TSCOM to rsConnections
                rsConnections['ts1'] = (substrings[1], substrings[2])
            else:
                #add TSEDU to rsConnections
                rsConnections['ts2'] = (substrings[1], substrings[2])
        else:
            #print substrings
            rsConnections[substrings[0]] = (substrings[1], substrings[2])
    
    #print rsConnections
    #return tsHostname


if __name__ == "__main__":
    if(not sys.argv[1].isdigit()):
        print("Please enter an integer hostname")
        sys.exit(0)


    '''
        Read file and create hashmap
            Hashmap Params:
                Key: Hostname
                Value: Tuple containing (IP Address, String)
    '''
    #print DNSRSContent

    asListenPort = sys.argv[1]
    ts1Hostname = sys.argv[2]
    ts1ListenPort_a = sys.argv[3]
    ts2Hosname = sys.argv[4]
    ts2ListenPort_a = sys.argv[5]
    t1 = threading.Thread(name='server', target=server, args=(asListenPort, ts1Hostname, ts1ListenPort_a, ts2Hosname, ts2ListenPort_a))
    t1.start()

    time.sleep(20)
    print("Done.")
    
    #Exit program
    sys.exit(0)
    os._exit(0)
