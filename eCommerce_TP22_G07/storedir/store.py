from cryptography.fernet import Fernet
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




args = sys.argv    #input given
argsSize = len(args)    #get size of the input given
args.append(' ')     #index out of bounds prevention

run = True
outputMsg = ''

CONSTANT_ERROR_135 = 'ERROR_135'

print(args)

for param in args:      #check if an invalid parameter was added
    if '-' in param:
        if param != '-s':
            if param != '-p':
                sys.exit(135)      #NOT SURE IF THE ERROR CODE IS RIGHT
                    


if "-p" in args:
    potentialPort = args[args.index("-p") + 1]
    
    if(potentialPort.isnumeric()):      #check if port inserted can be converted to an integer CHANGE TO THE PROJECT FORMAT
        port = int(potentialPort)
    else: 
        sys.exit(130)      #NOT SURE IF THE ERROR CODE IS RIGHT
else:
    port = 5000     #if port is not passed as a parameter


if "-s" in args:
    authFile = args[args.index("-s")+1]
    if(authFile == ' '):    #check if authFile name was inserted 
        authFile = 'bank.auth' 
else: 
    authFile = 'bank.auth'    #if authFile is not passed as a parameter

if not os.path.isfile(authFile):    #check if auth file exists
    sys.exit(130)

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #create a socket 

host = "127.0.0.1"    #ip of the store server

bankHost = "127.0.0.1" 
bankPort = 3000


try:
    bankSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #create a bank socket 
    
    serversocket.bind((host, port))     #bind the socket to a public host and a port
    serversocket.listen(1)

    while run:

        clientsocket, addr = serversocket.accept()

        # Receive the encrypted nonce from the client
        #encrypted_nonce = clientsocket.recv(1024)  # Use an appropriate buffer size

        # Decrypt the nonce
        #decrypted_nonce = decrypt(authFile, encrypted_nonce)  # Replace with your decryption function

        #clientsocket.sendall(decrypted_nonce)

        #serversocket.listen(1)

        requestJson = clientsocket.recv(1024)       #receive the client request, no more than 1024 bytes

        requestDict = json.loads(requestJson)       #loads the json format, turns it into a dictionary

        #accountNumber = requestDict['accountNumber']        #gets the request value of accountNumber 

        amount = requestDict['amount']
        vccFile = requestDict['vccFile']

        print('Got a connection from a new costumer')      #greet the user

        print('Connecting to bank...')      #begining of bank connection
        requestToBank = {}
        requestToBank['entity'] = 'store'       #tell the bank is a client speaking
        requestToBank['vccFile'] = vccFile
        requestToBank['amount'] = amount


        banksocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #create a socket object

        banksocket.connect((bankHost, bankPort))     #connection to hostname on the port

        jsonRequest= json.dumps(requestToBank)       #turns into a json request, the data dictionary

        banksocket.send(jsonRequest.encode('ascii'))      #sends the json request

        bankMsg = banksocket.recv(1024)      #receive the server answer, no more than 1024 bytes

        banksocket.close()        #closes the bank connection
        
        print('Connected to bank successfully!')
        
        bankMsg = bankMsg.decode('ascii')
        
        bankMsgDict = json.loads(bankMsg)

        if bankMsgDict['status'] == 200:
            print('tudo ok')
            answer = { 'vcc_file' : vccFile , 'vcc_amount_used': amount, 'status': 200}  
        else:
            answer = {'status': bankMsgDict['status']}
        
        #END OF BANK CONNECTION----------------------------
        
        jsonAnswer = json.dumps(answer)     #puts the dictionary answer as a json format 
        jsonAnswerAscii = jsonAnswer.encode('ascii')

        clientsocket.send(jsonAnswerAscii)       #sends the json answer for the request received
        clientsocket.close()
    
except Exception as e: 
    #print(outputMsg)
    sys.exit(130)

