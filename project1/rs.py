import threading
import time
import random
import sys, os
import socket

def server(rsListenPort, rsConnections, tsHostname):
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
            msg = tsHostname
        csockid.send(msg.encode('utf-8'))
        

    # Close the server socket
    ss.close()
    exit()

def reverse(msg):
	return msg[::-1]

def readFile(filename):
    fileContent = []
    for line in filename.readlines():
        fileContent.append(line.rstrip())
    #fileContent.append('END')
    filename.close()
    return fileContent

def createConnections(rsConnections, fileContent):
    contentLength = len(fileContent)
    tsHostname = fileContent[contentLength - 1]
    fileContent = fileContent[:(contentLength - 1)]
    for connection in fileContent:
        substrings = connection.split(' ')
        #print substrings
        rsConnections[substrings[0]] = (substrings[1], substrings[2])
    
    #print rsConnections
    return tsHostname


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
    filename = open('PROJI-DNSRS.txt')
    DNSRSContent = readFile(filename)
    #print DNSRSContent

    rsConnections = {}

    tsHostname = createConnections(rsConnections, DNSRSContent)
    print rsConnections
    
    t1 = threading.Thread(name='server', target=server, args=(sys.argv[1], rsConnections, tsHostname))
    t1.start()

    time.sleep(15)
    print("Done.")
    
    #Exit program
    sys.exit(0)
    os._exit(0)
