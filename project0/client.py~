import threading
import time
import random
import os
import socket

def client():
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()
        
    # Define the port on which you want to connect to the server
    port = 50007
    localhost_addr = '192.64.4.4'

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

if __name__ == "__main__":

    time.sleep(random.random() * 5)
    t2 = threading.Thread(name='client', target=client)
    t2.start()

    time.sleep(5)
    print("Done.")
    #Exit program
    os._exit(0)
