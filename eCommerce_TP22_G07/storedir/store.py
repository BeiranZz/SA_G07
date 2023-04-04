import sys
import socket 
import json

def main():
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
                    return 130      #NOT SURE IF THE ERROR CODE IS RIGHT
                        

    
    if "-p" in args:
        potentialPort = args[args.index("-p") + 1]
        
        if(potentialPort.isnumeric()):      #check if port inserted can be converted to an integer CHANGE TO THE PROJECT FORMAT
            port = int(potentialPort)
        else: 
            return 130      #NOT SURE IF THE ERROR CODE IS RIGHT
    else:
        port = 5000     #if port is not passed as a parameter
    

    if "-s" in args:
        authFile = args[args.index("-s")+1]
        if(authFile == ' '):    #check if authFile name was inserted 
            authFile = 'bank.auth' 
    else: 
        authFile = 'bank.auth'    #if authFile is not passed as a parameter


    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #create a socket 

    host = "127.0.0.1"    #ip of the store server

    bankHost = "127.0.0.1" 
    bankPort = 3000

    bankSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #create a bank socket 
    try:
        serversocket.bind((host, port))     #bind the socket to a public host and a port
        serversocket.listen(1)

        while run:

            clientsocket, addr = serversocket.accept()

            requestJson = clientsocket.recv(1024)       #receive the client request, no more than 1024 bytes

            requestDict = json.loads(requestJson)       #loads the json format, turns it into a dictionary

            #accountNumber = requestDict['accountNumber']        #gets the request value of accountNumber 

            amount = requestDict['amount']
            vccFile = requestDict['vccFile']

            print('Got a connection from a new costumer')      #greet the user

            #BEGIN OF BANK CONNECTION--------------------------
            print('connecting to bank...')
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
            print('bank connected successfully')

            bankMsg = bankMsg.decode('ascii')
            
            bankMsgDict = json.loads(bankMsg)

            print(vccFile)
            print(amount)

            if bankMsgDict['status'] == 200:
                print('tudo ok')
                answer = { 'vcc_file' : vccFile , 'vcc_amount_used': amount, 'status': 200}  
            else:
                answer = {'status': bankMsgDict['status']}
            
            #END OF BANK CONNECTION----------------------------
            
            print('DUMPING')
            jsonAnswer = json.dumps(answer)     #puts the dictionary answer as a json format 
            print('DUMPING')
            jsonAnswerAscii = jsonAnswer.encode('ascii')

            clientsocket.send(jsonAnswerAscii)       #sends the json answer for the request received
            clientsocket.close()
        
    except Exception as e: 
        #print(outputMsg)
        print(e)

main = main()