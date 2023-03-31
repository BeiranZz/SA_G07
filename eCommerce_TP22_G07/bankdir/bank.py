import sys
import socket 
import json

def main():
    
    run = True
    outputMsg = ''

    operation = ''     #to know which operation is being made

    for param in args:      #check if an invalid parameter was added
        if '-' in param:
            if param != '-s':
                if param != '-p':
                    run = False
                    outputMsg = CONSTANT_ERROR_125      #invalid parameter inserted

    
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

    host = "127.0.0.2"    #ip of the server

    try:
        serversocket.bind((host, port))     #bind the socket to a public host and a port
        serversocket.listen(1)

        if not run:
            print(outputMsg)

        while run: 
            clientsocket, addr = serversocket.accept()

            requestJson = clientsocket.recv(1024)       #receive the client request, no more than 1024 bytes

            requestDict = json.loads(requestJson)       #loads the json format, turns it into a dictionary

            accountNumber = requestDict['accountNumber']        #gets the request value of accountNumber 

            if(accountNumber != None):      
                print('Got a connection from client number ' + str(accountNumber))      #greet the user

                userAccountNum = requestDict['accountNumber']
                operation = requestDict['operation']
                print(requestDict)
                if operation == 'createAccount':
                    if userAccountNum not in clientInfo:     #checks if the accountNumber is in a valid format and if it already exists
                        userFile = requestDict['userFile']
                        balance = requestDict['balance']

                        if balance >= 15.0:
                            clientInfo[userAccountNum] = userFile, balance
                            answer = { 'status' : 'Account created!' }
                        else:
                            answer = { 'status' : 'Balance needs to be higher than 15!' } 
                        
                               #modify this answer for a more suitable one
                    else:
                        answer = { 'status' : 'Account number inserted is invalid!' }

                elif operation == 'deposit':
                    if userAccountNum in clientInfo:
                        userFile, balance = clientInfo[userAccountNum]
                        if userFile == requestDict['userFile']:     #check if the userFile corresponds to the given one
                            amount = requestDict['amount']      #get the amount to be deposit
                            if amount is not None and amount.isNumeric() and amount > 0:
                                clientInfo[userAccountNum] = userFile, balance + amount
                                answer = { 'status' : 'Deposit made successfully!' }       #modify this answer for a more suitable one

                elif operation == 'createVCard':
                    answer = { 'status' : 'Virtual Card created!' }       #modify this answer for a more suitable one

                elif operation == 'getBalance':
                    answer = { 'status' : 'This is your balance!' }       #modify this answer for a more suitable one

                else:
                    answer = { 'status' : 'ERROR: Uknonw operation!' } 

            else:
                answer = { 'status' : 'negative' }      #modify this answer for a more suitable one
            

            #PROCCESS THE REQUEST RECEIVED 
            
            #-----------------------------

            jsonAnswer = json.dumps(answer)     #puts the dictionary answer as a json format 
            jsonAnswerAscii = jsonAnswer.encode('ascii')

            clientsocket.send(jsonAnswerAscii)       #sends the json answer for the request received
            clientsocket.close()
        
    except Exception as e: 
        #print(outputMsg)
        #print(e)
        return e


#PROGRAM START
args = sys.argv    #input given
argsSize = len(args)    #get size of the input given
args.append(' ')     #index out of bounds prevention

CONSTANT_ERROR_125 = 'ERROR_125'

print(args)

clientInfo = {}     #to store every client info

main = main()

