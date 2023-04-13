from cryptography.fernet import Fernet
import signal
import sys
import socket 
import json
import os

def encrypt(authFile, plaintext):

    with open(authFile, 'rb') as f:
        key = f.read()
    
    fernet = Fernet(key)    # create a Fernet object with the key

    ciphertext = fernet.encrypt(plaintext)      #encrypt the plaintext
    
    return ciphertext

def decrypt(authFile, ciphertext):

    with open(authFile, 'rb') as f:
        key = f.read()
    
    fernet = Fernet(key)    # create a Fernet object with the key

    plaintext = fernet.decrypt(ciphertext)      #decrypt the ciphertext
    
    return plaintext

#PROGRAM START
args = sys.argv    #input given
argsSize = len(args)    #get size of the input given
args.append(' ')     #index out of bounds prevention

print(args)

clientInfo = {}     #to store every client info

clientsWithCards = []

vCardCount = 1

run = True
outputMsg = ''

operation = ''     #to know which operation is being made

for param in args:      #check if an invalid parameter was added
    if '-' in param:
        if param != '-s':
            if param != '-p':
                sys.exit(125)     #invalid parameter inserted


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
else: 
    authFile = 'bank.auth'    #if authFile is not passed as a parameter

if not os.path.isfile(authFile):    #check if auth file exists
    key = Fernet.generate_key()     # generate a new key

    with open(authFile, 'wb') as f:
        f.write(key)        # stores the key in the file
    print('created')
else: 
    sys.exit(125)       #auth file doesnt exist
    
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #create a socket 

host = "127.0.0.1"    #ip of the server

try:
    serversocket.bind((host, port))     #bind the socket to a public host and a port
    serversocket.listen(1)

    while run: 

        # Accept a client connection
        clientsocket, addr = serversocket.accept()

        # Receive the encrypted nonce from the client
        #encrypted_nonce = clientsocket.recv(1024)  # Use an appropriate buffer size

        # Decrypt the nonce
        #decrypted_nonce = decrypt(authFile, encrypted_nonce)  # Replace with your decryption function

        #clientsocket.sendall(decrypted_nonce)

        #serversocket.listen(1)

        requestJsonEncrypted = clientsocket.recv(1024)       #receive the client request, no more than 1024 bytes
        
        requestJson = decrypt(authFile, requestJsonEncrypted)
            
        requestDict = json.loads(requestJson)       #loads the json format, turns it into a dictionary

        if requestDict['entity'] == 'client':
            accountNumber = requestDict['accountNumber']        #gets the request value of accountNumber 

            if(accountNumber != None):      

                if operation != 'createAccount':
                    print('Got a connection from client number ' + str(accountNumber))      #greet the user

                userAccountNum = requestDict['accountNumber']
                operation = requestDict['operation']
                #print(requestDict)
                if operation == 'createAccount':
                    if userAccountNum not in clientInfo:     #checks if the accountNumber is in a valid format and if it already exists
                        userFile = requestDict['userFile']
                        balance = requestDict['balance']
                        clientInfo[userAccountNum] = userFile, balance
                        answer = { 'account' : userAccountNum, 'initial_balance': balance, 'status': 200}
                        print(answer)
                        
                    else:
                        answer = { 'status' : 'Account number inserted is invalid!' }

                elif operation == 'deposit':
                    
                    if userAccountNum in clientInfo:
                        userFile, balance = clientInfo[userAccountNum]
                        if userFile == requestDict['userFile']:     #check if the userFile corresponds to the given one
                            amount = requestDict['amount']      #get the amount to be deposit
                            if amount is not None and amount > 0:
                                clientInfo[userAccountNum] = userFile, balance + amount
                                answer = { 'account' : userAccountNum, 'deposit': amount, 'status': 200}      
                                print(answer)
                        else:
                            answer = { 'status' : 'User file given doesnt correspond with the userfile required!' }  
                    else:
                        answer = { 'status' : 'Account Number doesnt exist!' }  

                #-----------------------------------
                elif operation == 'createVCard':
                    userFile, balance = clientInfo[userAccountNum]
                    if userFile == requestDict['userFile']:     #check if the userFile corresponds to the given one
                        amount = requestDict['amount']      #get the amount to be deposit
                        if amount <= balance:
                            if userAccountNum not in clientsWithCards:
                                clientsWithCards.append(userAccountNum)     #adds the user to the list with the users with vCards

                                vCardFileName = str(userAccountNum) + '_' + str(vCardCount) + '.card'       #creates vCard file name in the format requested

                                vCardFile = open(vCardFileName, "w")     #create a vCard file with the correspondent name

                                vCardFile.write(str(amount))     #type the amount of the card in the file

                                vCardFile.close()

                                answer = { 'account' : userAccountNum, 'vcc_amount': amount, 'vcc_file': vCardFileName ,'status': 200}   
                                print(answer)

                                vCardCount += 1
                            else:
                                answer = { 'status' : 130 }  
                        else:
                            answer = { 'status' : 130 }  
                    else:
                        answer = { 'status' : 130 }  


                #-----------------------------------
                elif operation == 'getBalance':
                    if userAccountNum in clientInfo:
                        userFile, balance = clientInfo[userAccountNum]
                        if userFile == requestDict['userFile']:     #check if the userFile corresponds to the given one
                            answer = { 'account' : userAccountNum, 'balance': balance, 'status': 200}   
                            print(answer)
                        else:
                            answer = { 'status' : 130 }   
                    else:
                        answer = { 'status' : 130 } 
                    


                #-----------------------------------
                else:
                    answer = { 'status' : 130 } 

                #-----------------------------------
            else:
                answer = { 'status' : 130 } 
            

            #PROCCESS THE REQUEST RECEIVED 
            
            #-----------------------------
        elif(requestDict['entity'] == 'store'):     #check if its a store speaking
            print('Store connecting')

            vccFile = requestDict['vccFile']        #gets the vccFile passed
            amount = float(requestDict['amount'])     #gets the amount of the purchase

            accountNum = int(vccFile.split('_')[0])      #gets the user num using the vcc file

            if accountNum in clientsWithCards:      #check if given num has an active vcc card
                if os.path.isfile(vccFile):     #check if the file exists
                    #print('File exists')
                    file = open(vccFile, 'r')
                    
                    vccCredit = float(file.read())

                    # Close the file
                    file.close()

                    if amount <= vccCredit:
                        userFile, balance = clientInfo[accountNum]
                        print(balance)
                        if amount <= balance:       #checks if the client has enough balance to do the purchase
                            balance -= amount       #takes the purchase amount out of the client's balance 
                            os.remove(vccFile)      #deletes vcc file
                            clientsWithCards.remove(accountNum)
                            print(clientsWithCards)
                            clientInfo[accountNum] = userFile, balance
                            answer = { 'status' : 200 } 
                        else:
                            print('primeiro')
                            answer = { 'status' : 130 } 
                    else:
                        answer = { 'status' : 130 } 
                else:
                    answer = { 'status' : 130 } 
            else:
                answer = { 'status' : 130 } 
            



        jsonAnswer = json.dumps(answer)     #puts the dictionary answer as a json format 
        jsonAnswerAscii = jsonAnswer.encode('ascii')

        clientsocket.send(encrypt(authFile, jsonAnswerAscii))       #sends the json answer for the request received while encrypting it 
        clientsocket.close()

except KeyboardInterrupt:
    print("Stopped!")
    sys.exit(0)

except Exception as e: 
    #print(outputMsg)
    #print(e)
    sys.exit(130)

