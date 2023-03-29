import sys
import socket
import json

args = sys.argv    #input given
argsSize = len(args)    #get size of the input given
args.append(' ')     #index out of bounds prevention
print(args)

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
        accountNumber = int(potentialAccountNum)
        data['accountNumber'] = accountNumber       #json request being modified accountNumber added
        print('Acount number: ' + str(accountNumber))
    else:
        accountNumber = 13131313        #accountNumber 13131313 is for now an error number
        outputMsg = 'Insert a valid bank account number! e.g. 55555'
        run = False
    

#--------------------------------------------

#--------S_PARAMETER-------------------------
if '-s' in args:
    authFile = args[args.index("-s")+1]
    if(authFile == ' '):    #check if authFile name was inserted 
        authFile = 'bank.auth' 
else:
    authFile = 'bank.auth'
#--------------------------------------------

#--------I_PARAMETER-------------------------
if '-i' in args:    #it can be store or bank
    host = args[args.index("-i") + 1]
else: 
    host = '127.0.0.1'
#--------------------------------------------

#--------P_PARAMETER-------------------------
if '-p' in args: #it can be store or bank
    potentialPort = args[args.index("-p") + 1]
    
    if(potentialPort.isnumeric()):      #check if port inserted can be converted to an integer
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
if '-u' in args:
    userFile = args[args.index("-u")+1]
    if(userFile == ' '):    #check if userFile name was inserted 
        userFile = str(accountNumber) + '.user' 
else:
    userFile = str(accountNumber) + '.user'
#--------------------------------------------

#--------V_PARAMETER-------------------------

if '-v' in args:
    if isABankConnection:
        run = False
        outputMsg = 'Parameter -v invalid for a bank operation'
    else:    
        vccFile = args[args.index("-v")+1]
        if(vccFile == ' '):    #check if userFile name was inserted 
            seqNumber = 0
            vccFile = accountNumber + '_' + seqNumber + '.user'
else:
    if not isABankConnection:
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
                raise ValueError('Balance should be greater than 15.00')

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
                raise ValueError('Amount should be greater than 0.00')

        except ValueError:     #check if value meets the scope conditions
            outputMsg = CONSTANT_ERROR_130
            run = False
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
                raise ValueError('Amount should be greater than 0.00')

        except ValueError:     #check if value meets the scope conditions
            outputMsg = CONSTANT_ERROR_130
            run = False

    #--------G_PARAMETER-------------------------
    elif param == '-g':
        operation = 'getBalance'
        data['operation'] = 'getBalance'       #json request being modified operation added
        numberOfModes += 1
        G_FLAG = True
    #--------------------------------------------

    #--------M_PARAMETER-------------------------
    elif param == '-m':
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

            except ValueError:     #check if value meets the scope conditions
                outputMsg = CONSTANT_ERROR_130
                run = False
    #--------------------------------------------
    
if(numberOfModes == 0):     #check if at least one mode of operator was added
    outputMsg = CONSTANT_ERROR_130
    run = False
elif(numberOfModes > 1):    #check if multiple modes of operator were added
    outputMsg = CONSTANT_ERROR_130
    run = False

printActivated = True       #for debug porpuses, put False to not have the following prints

if(printActivated):
    print('Auth File: ' + str(authFile))
    print('Run: ' + str(run))
    print('Output: ' + outputMsg)
    print('Host: ' + host)
    print('Port: ' + str(port))
    print('User File: ' + userFile)
    print('Number of Modes: ' + str(numberOfModes))
    print('Operation: ' + str(operation))
    print('Is a Bank Conn: ' + str(isABankConnection))
    print('Account numb: ' + str(accountNumber))

if run:
    try:
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #create a socket object

        clientsocket.connect((host, port))     #connection to hostname on the port

        jsonRequest= json.dumps(data)       #turns into a json request, the data dictionary

        clientsocket.send(jsonRequest.encode('ascii'))      #sends the json request

        msg = clientsocket.recv(1024)      #receive the server answer, no more than 1024 bytes
    
        clientsocket.close()        #closes the server connection

        print(msg.decode('ascii'))      #prints the server answer received

    except Exception as e:
        print(e)
else:
    if outputMsg == CONSTANT_ERROR_130:
        print(CONSTANT_ERROR_130)
    else:
        print(outputMsg)