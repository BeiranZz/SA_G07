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



def isValidIpv4Address(ip):
    """
    Checks if a given IP address is a valid IPv4 address in dotted decimal notation.
    """
    parts = ip.split('.')       #split the IP address by '.'
    
    if len(parts) != 4:     #ensure that the IP address has four parts
        return False
    
    for part in parts:      
        if not part.isdigit() or int(part) < 0 or int(part) > 255:      #ensure that each part is a number between 0 and 255
            return False
    
    return True

#PROGRAM START
args = sys.argv    #input given
argsSize = len(args)    #get size of the input given
args.append(' ')     #index out of bounds prevention
#print(args)

MustHaveM = False
A_FLAG = False
V_Flag = False
G_FLAG = False      #since -g parameter doesnt have other params

run = True
outputMsg = ''

data = {}       #set up for the json response

CONSTANT_ERROR_130 = 'ERROR_130'

isABankConnection = False    #flag to keep in track if its a client -> bank connection

operation = ''      #to know which operation is being made

#--------A_PARAMETER-------------------------
if '-a' in args:
    isABankConnection = True    #only the bank connections have the -a parameter

    potentialAccountNum = args[args.index("-a") + 1]
    if(potentialAccountNum.isnumeric()):
        A_FLAG = True
        accountNumber = int(potentialAccountNum)
        data['accountNumber'] = accountNumber       #json request being modified accountNumber added
        print('Acount number: ' + str(accountNumber))
    else:
        outputMsg = 'Insert a valid bank account number! e.g. 55555'
        sys.exit(130)
else:
    if '-m' not in args:
        sys.exit(130)

#--------------------------------------------

#--------S_PARAMETER-------------------------
if '-s' in args:
    authFile = args[args.index("-s")+1]
    if(authFile == ' '):    #check if authFile name was inserted 
        authFile = 'bank.auth' 
else:
    authFile = 'bank.auth'

if not os.path.isfile(authFile):    #check if auth file exists
    sys.exit(130)
#--------------------------------------------

#--------I_PARAMETER-------------------------
if '-i' in args:    #it can be store or bank
    host = args[args.index("-i") + 1]
    if not isValidIpv4Address(host):
        sys.exit(130)
else: 
    host = '127.0.0.1'
#--------------------------------------------

#--------P_PARAMETER-------------------------
if '-p' in args: #it can be store or bank
    potentialPort = args[args.index("-p") + 1]
    
    if(potentialPort.isnumeric()):      #check if port inserted can be converted to an integer CHANGE TO THE PROJECT FORMAT
        port = int(potentialPort)
    else: 
        outputMsg = 'Port parameter should be an Integer!'
        run = False
else:
    if isABankConnection:
        port = 3000     #bank connection, if port is not passed as a parameter
    else:
        port = 5000     #store connection, if port is not passed as a parameter
#--------------------------------------------

#--------U_PARAMETER-------------------------
if A_FLAG:
    if '-u' in args:
        userFileName = args[args.index("-u")+1]
        if(userFileName == ' '):    #check if userFile name was inserted 
            userFileName = str(accountNumber) + '.user' 
        data['userFile'] = userFileName
    else:
        userFileName = str(accountNumber) + '.user'

    data['userFile'] = userFileName
#--------------------------------------------

#--------V_PARAMETER-------------------------

if '-v' in args:
    if isABankConnection:
        sys.exit(130)
    else:    
        vccFile = args[args.index("-v")+1]
        V_Flag = True
        data['vccFile'] = vccFile
        if(vccFile == ' '):    #check if vccFile name was inserted 
            sys.exit(130)     #CHECK THE QUESTION ON THIS (TEMPORARY)
            seqNumber = 0
            vccFile = accountNumber + '_' + seqNumber + '.user'
else:
    if not isABankConnection:
        sys.exit(130)    #CHECK THE QUESTION ON THIS (TEMPORARY)
        seqNumber = 0
        vccFile = accountNumber + '_' + seqNumber + '.user'
#--------------------------------------------

numberOfModes = 0

for param in args:
    #--------N_PARAMETER-------------------------
    if param == '-n' :
        operation = 'createAccount'
        data['operation'] = 'createAccount'       #json request being modified operation added
        numberOfModes += 1

        potentialBalance = args[args.index("-n") + 1]

        try:
            balance = float(potentialBalance)
            if(balance < 15.0):
                sys.exit(130)
            else:
                data['balance'] = balance

        except ValueError:     #check if value meets the scope conditions
            outputMsg = CONSTANT_ERROR_130
            run = False
    #--------------------------------------------

    #--------D_PARAMETER-------------------------
    elif param == '-d':
        operation = 'deposit'
        data['operation'] = 'deposit'       #json request being modified operation added
        numberOfModes += 1

        potentialAmount = args[args.index("-d") + 1]

        try:
            amount = float(potentialAmount)
            if(amount <= 0.0):
                sys.exit(130)
            else:
                data['amount'] = amount

        except ValueError:     #check if value meets the scope conditions
            sys.exit(130)
    #--------------------------------------------

    #--------C_PARAMETER-------------------------
    elif param == '-c' :
        operation = 'createVCard'
        data['operation'] = 'createVCard'       #json request being modified operation added
        numberOfModes += 1

        potentialAmount = args[args.index("-c") + 1]

        try:
            amount = float(potentialAmount)
            if(amount <= 0.0):
                sys.exit(130)
            else:
                data['amount'] = amount

        except ValueError:     #check if value meets the scope conditions
            sys.exit(130)

    #--------G_PARAMETER-------------------------
    elif param == '-g':
        operation = 'getBalance'
        data['operation'] = 'getBalance'       #json request being modified operation added
        numberOfModes += 1
        G_FLAG = True
    #--------------------------------------------

    #--------M_PARAMETER-------------------------
    elif param == '-m':
        if A_FLAG == True or V_Flag == False:
            sys.exit(130)
        
        operation = 'purchase'
        data['operation'] = 'purchase'       #json request being modified operation added
        numberOfModes += 1    
        
        if isABankConnection:
            run = False
            outputMsg = 'Invalid mode of operation'
        else:
            potentialShoppingValue = args[args.index("-m") + 1]

            try:
                shoppingValue = float(potentialShoppingValue)
                if(shoppingValue < 0.0):
                    raise ValueError('Shopping value should be greater than 0')
                else:
                    data['amount'] = shoppingValue 

            except ValueError:     #check if value meets the scope conditions
                sys.exit(130)
    #--------------------------------------------
    
if(numberOfModes == 0):     #check if at least one mode of operator was added
    sys.exit(130)
elif(numberOfModes > 1):    #check if multiple modes of operator were added
    sys.exit(130)

printActivated = True       #for debug porpuses, put False to not have the following prints

if(printActivated):
    print('Auth File: ' + str(authFile))
    print('Run: ' + str(run))
    print('Output: ' + outputMsg)
    print('Host: ' + host)
    print('Port: ' + str(port))
    print('Number of Modes: ' + str(numberOfModes))
    print('Operation: ' + str(operation))
    print('Is a Bank Conn: ' + str(isABankConnection))
    if A_FLAG:
        print('Account numb: ' + str(accountNumber))
        print('User File: ' + userFileName)

if run:
    try:
        if operation == 'createAccount':
            if os.path.isfile(userFileName):    #check if the given userFile already exists
                sys.exit(130)
        
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #create a socket object
        
        clientsocket.connect((host, port))     #connection to hostname on the port

        #nonce = os.urandom(16)      # Generate a random nonce

        #encrypted_nonce = encrypt(authFile, nonce)      # Encrypt the nonce

        #clientsocket.sendall(encrypted_nonce)       # Send the encrypted nonce to the server

        #decrypted_nonce = clientsocket.recv(1024)  # Receive the decrypted nonce from the server

        #if nonce != decrypted_nonce:
            #sys.exit(130)

        data['entity'] = 'client'       #tell the bank is a client speaking

        jsonRequest= json.dumps(data)       #turns into a json request, the data dictionary
        
        jsonRequestAscii = jsonRequest.encode('ascii')
        
        clientsocket.send(encrypt(authFile, jsonRequestAscii))      #sends the json request
        
        msgEncrypted = clientsocket.recv(1024)      #receive the server answer, no more than 1024 bytes
        
        msg = decrypt(authFile, msgEncrypted)

        clientsocket.close()        #closes the server connection

        msg = msg.decode('ascii')
        msgDict = json.loads(msg)
        
        if operation == 'createAccount' and msgDict['status'] == 200:
            
            userFile = open(userFileName, "w")     #create a user file with the given or default name
            
            userFile.write(str(data['balance']))     #type the pin 123456 (FOR NOW)

            userFile.close()

            #os.chmod(userFile, 0o444)       #give the permission to only be viewd
        
        #print(msgDict)
        if msgDict['status'] == 130:
            sys.exit(130)
        
        print(msg)      #prints the server answer received

    except Exception as e:
        print(e)
else:
    if outputMsg == CONSTANT_ERROR_130:
        sys.exit(130)
    else:
        print(outputMsg)


