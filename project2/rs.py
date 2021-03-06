import threading
import time
import random
import sys, os
import socket

def server(rsListenPort, rsConnections, tsHostname, tsEduListenPort, tsComListenPort):
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
    #count = 0
    while True:
        #count = count + 1
        #print ("Count: " + str(count))
        # Receive client msg
        data_from_server=csockid.recv(200)
        print("[C]: Data received from client: {}".format(data_from_server.decode('utf-8')))
        if not data_from_server or data_from_server == 'END':
            print("[S]: Data from client: " + data_from_server)
            msg = clientTS(rsConnections.get('tsCom')[0], tsComListenPort, 'END')
            msg = clientTS(rsConnections.get('tsEdu')[0], tsEduListenPort, 'END')
            csockid.send('END'.encode('utf-8'))
            break
        
        data_from_server = data_from_server.lower()

        # Response section
        #if hostname is in hashtable, connection is in RS. if not, redirect to tS
        connectionValues = rsConnections.get(data_from_server)
        #print(connectionValues)
        msg = ''
        if connectionValues != None:
            msg = data_from_server + ' ' + connectionValues[0] + ' ' + connectionValues[1]
        else:
            #Check for data_from_server ending block
            temp = data_from_server.split('.')
            tempLen = len(temp)
            #If end block is com - direct to tsCOM
            if temp[tempLen - 1] == 'com':
                msg = clientTS(rsConnections.get('tsCom')[0], tsComListenPort, data_from_server)
            #else if end block is edu - direct to tsEDU
            elif temp[tempLen - 1] == 'edu':
                msg = clientTS(rsConnections.get('tsEdu')[0], tsEduListenPort, data_from_server)
            #else return error msg
            else:
                msg = data_from_server + ' - Error:HOST NOT FOUND'

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
                rsConnections['tsCom'] = (substrings[1], substrings[2])
            else:
                #add TSEDU to rsConnections
                rsConnections['tsEdu'] = (substrings[1], substrings[2])
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
    filename = open('PROJ2-DNSRS.txt')
    DNSRSContent = readFile(filename)
    #print DNSRSContent

    rsConnections = {}

    tsHostname = createConnections(rsConnections, DNSRSContent)
    print rsConnections

    t1 = threading.Thread(name='server', target=server, args=(sys.argv[1], rsConnections, tsHostname, sys.argv[2], sys.argv[3]))
    t1.start()

    time.sleep(20)
    print("Done.")
    
    #Exit program
    sys.exit(0)
    os._exit(0)
