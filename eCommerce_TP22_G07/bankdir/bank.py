import sys
import socket 
import json

args = sys.argv    #input given
argsSize = len(args)    #get size of the input given
args.append(' ')     #index out of bounds prevention

run = True
outputMsg = ''

CONSTANT_ERROR_125 = 'ERROR_125'

operation = ''      #to know which operation is being made

print(args)

for param in args:      #check if an invalid parameter was added
    if '-' in param:
        if param != '-s':
            if param != '-p':
                run = False
                outputMsg = CONSTANT_ERROR_125      #invalid parameter inserted


if run:
    if "-p" in args:
        potentialPort = args[args.index("-p") + 1]
        
        if(potentialPort.isnumeric()):      #check if port inserted can be converted to an integer
            port = int(potentialPort)
        else: 
            run = False 
            outputMsg = 'Port parameter should be an Integer'
    else:
        port = 3000     #if port is not passed as a parameter
    

    if "-s" in args:
        authFile = args[args.index("-s")+1]
        if(authFile == ' '):    #check if authFile name was inserted 
            authFile = 'bank.auth' 
            #run = False
            #outputMsg = 'Insert a file name after the -s parameter'
    else: 
        authFile = 'bank.auth'    #if authFile is not passed as a parameter


    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #create a socket 

    host = "0.0.0.0"    #ip of the server

    try:
        serversocket.bind((host, port))     #bind the socket to a public host and a port
        serversocket.listen(1)

        if not run:
            print(outputMsg)

        while run: 
            clientsocket, addr = serversocket.accept()
            print("Got a connection from %s" % str(addr))
            msg = 'Thank you for connecting' + "\r\n"
            clientsocket.send(msg.encode('ascii'))
            clientsocket.close()
        
    except Exception as e: 
        #print(outputMsg)
        print(e)
else:
    print(outputMsg)