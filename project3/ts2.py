import threading
import time
import random
import sys, os
import socket
import hmac

def server(tsListenPort, tsConnections, key):
    
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    server_binding = (socket.gethostbyname(socket.gethostname()), int(tsListenPort))
    print("[S]: Server binding is {}".format(str(server_binding)))
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("[S]: Server bind is " + str(ss.bind(server_binding)))
    print("[S]: Server listen is " + str(ss.listen(5)))
    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))
        
    while True:
        csockid, addr = ss.accept()
        print ("[S]: Got a connection request from a client at {}".format(addr))
        # Receive client msg
        data_from_server=csockid.recv(200)
        print("[C]: Data received from client: {}".format(data_from_server.decode('utf-8')))
        test = data_from_server.split('.')
        if not data_from_server or data_from_server == 'END':
            print("[S]: Data from client: " + data_from_server)
            csockid.send('END'.encode('utf-8'))
            break
        elif len(test) == 1:
            #Create and send back digest
            digest_query = hmac.new(key.encode("utf-8"), data_from_server.encode("utf-8"))
            print digest_query
            print digest_query.hexdigest()
            csockid.send(digest_query.hexdigest())
            continue

        data_from_server = data_from_server.lower()

        # Response section
        #if hostname is in hashtable, connection is in RS. if not, redirect to tS
        connectionValues = tsConnections.get(data_from_server)
        #print(connectionValues)
        msg = ''
        if connectionValues != None:
            msg = data_from_server + ' ' + connectionValues[0] + ' ' + connectionValues[1]
        else:
            msg = data_from_server + ' - Error:HOST NOT FOUND'
        csockid.send(msg.encode('utf-8'))
        

    # Close the server socket
    # print("TS Com socket closed after AS: " +  str(ss.close()))
    print("TS socket closed after AS")
    ss.close()
    exit()

def readFile(filename):
    fileContent = []
    for line in filename.readlines():
        fileContent.append(line.rstrip())
    #fileContent.append('END')
    filename.close()
    return fileContent

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

def createConnections(tsConnections, fileContent):
    for connection in fileContent:
        substrings = connection.split(' ')
        #print substrings
        tsConnections[substrings[0]] = (substrings[1], substrings[2])
    
    #print tsConnections


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
    filename = open('PROJ3-DNSTS2.txt')
    keyFilename = open('PROJ3-KEY2.txt')
    DNSTSContent = readFile(filename)
    keyContent = readFile(keyFilename)[0]
    print("Key: " + keyContent)
    clientListenPort = sys.argv[2]
    #print DNSRSContent

    tsConnections = {}

    createConnections(tsConnections, DNSTSContent)
    

    t1 = threading.Thread(name='server', target=server, args=(sys.argv[1], tsConnections, keyContent))
    t1.start()
    
    t2 = threading.Thread(name='C_server', target=server, args=(clientListenPort, tsConnections, keyContent))
    t2.start()

    time.sleep(25)
    print("Done.")
    
    #Exit program
    sys.exit(0)
    os._exit(0)
