import subprocess

def run_command(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    exit_status = process.returncode
    return output.decode().strip(), error.decode().strip(), exit_status

print('-----------------------------------------------------')
print('-----------------------------------------------------')
# Test 1: Create an account 1 with 15 balance
test1_command = "java -jar mbec.jar -a 1 -n 15"
print('Testing command: ' + test1_command)
print('----')
test1_output, test1_error, test1_exit_status = run_command(test1_command)
print('Test Output: ' + test1_output)
print('Expected Test Output: ' + '{"account":"1","initial_balance":15.00}')
print('----')
#print("Test 1 Error:")
#print(test1_error)
print('Test Exit Status: ' + str(test1_exit_status))
print('Expected Test Exit Status: 0')
print('-----------------------------------------------------')
print('-----------------------------------------------------')


# Test 2: Trying to create an account that already exists
test2_command = "java -jar mbec.jar -a 1 -n 20"
print('Testing command: ' + test2_command)
print('----')
test2_output, test2_error, test2_exit_status = run_command(test2_command)
print('Test Output: ' + test2_output)
print('Expected Test Output: ')
print('----')
#print("Test 1 Error:")
#print(test1_error)
print('Test Exit Status: ' + str(test2_exit_status))
print('Expected Test Exit Status: 130')
print('-----------------------------------------------------')
print('-----------------------------------------------------')


# Test 3: Deposit 0.01 euros of balance in the account 1
test3_command = "java -jar mbec.jar -a 1 -d 0.01"
print('Testing command: ' + test3_command)
print('----')
test3_output, test3_error, test3_exit_status = run_command(test3_command)
print('Test Output: ' + str(test3_output))
print('Expected Test Output: ' + '{"account":"1","deposit":0.01}')
print('----')
#print("Test 1 Error:")
#print(test1_error)
print('Test Exit Status: ' + str(test3_exit_status))
print('Expected Test Exit Status: 0')
print('-----------------------------------------------------')
print('-----------------------------------------------------')


# Test 4: Deposit negative amount in account 1 
test4_command = "java -jar mbec.jar -a 1 -d -0.01"
print('Testing command: ' + test4_command)
print('----')
test4_output, test4_error, test4_exit_status = run_command(test4_command)
print('Test Output: ' + str(test4_output))
print('Expected Test Output: ')
print('----')
#print("Test 1 Error:")
#print(test1_error)
print('Test Exit Status: ' + str(test4_exit_status))
print('Expected Test Exit Status: 130')
print('-----------------------------------------------------')
print('-----------------------------------------------------')


# Test 5: java -jar mbec.jar -a 1 -g
test5_command = "java -jar mbec.jar -a 1 -g"
print('Testing command: ' + test5_command)
print('----')
test5_output, test5_error, test5_exit_status = run_command(test5_command)
print('Test Output: ' + str(test5_output))
print('Expected Test Output: ' + '{"account":"1","balance":15.01}')
print('----')
#print("Test 1 Error:")
#print(test1_error)
print('Test Exit Status: ' + str(test5_exit_status))
print('Expected Test Exit Status: 0')
print('-----------------------------------------------------')
print('-----------------------------------------------------')


# Test 6: Creating an account with a balance < 15
test6_command = "java -jar mbec.jar -a 2 -n 14"
print('Testing command: ' + test6_command)
print('----')
test6_output, test6_error, test6_exit_status = run_command(test6_command)
print('Test Output: ' + str(test6_output))
print('Expected Test Output: ')
print('----')
#print("Test 1 Error:")
#print(test1_error)
print('Test Exit Status: ' + str(test6_exit_status))
print('Expected Test Exit Status: 130')
print('-----------------------------------------------------')
print('-----------------------------------------------------')


# Test 7: Creating a card of an account that doesnt exist
test7_command = "java -jar mbec.jar -a 3 -c 5"
print('Testing command: ' + test7_command)
print('----')
test7_output, test7_error, test7_exit_status = run_command(test7_command)
print('Test Output: ' + str(test7_output))
print('Expected Test Output: ')
print('----')
#print("Test 1 Error:")
#print(test1_error)
print('Test Exit Status: ' + str(test7_exit_status))
print('Expected Test Exit Status: 130')
print('-----------------------------------------------------')
print('-----------------------------------------------------')


# Test 8: Creating a card with negative balance
test8_command = "java -jar mbec.jar -a 1 -c -5"
print('Testing command: ' + test8_command)
print('----')
test8_output, test8_error, test8_exit_status = run_command(test8_command)
print('Test Output: ' + str(test8_output))
print('Expected Test Output: ')
print('----')
#print("Test 1 Error:")
#print(test1_error)
print('Test Exit Status: ' + str(test8_exit_status))
print('Expected Test Exit Status: 130')
print('-----------------------------------------------------')
print('-----------------------------------------------------')


# Test 9: Creating a card with more money than in bank acc
test9_command = "java -jar mbec.jar -a 1 -c 50"
print('Testing command: ' + test9_command)
print('----')
test9_output, test9_error, test9_exit_status = run_command(test9_command)
print('Test Output: ' + str(test9_output))
print('Expected Test Output: ')
print('----')
#print("Test 1 Error:")
#print(test1_error)
print('Test Exit Status: ' + str(test9_exit_status))
print('Expected Test Exit Status: 130')
print('-----------------------------------------------------')
print('-----------------------------------------------------')


# Test 10: Creating a card successfully with 5 euros
test10_command = "java -jar mbec.jar -a 1 -c 5"
print('Testing command: ' + test10_command)
print('----')
test10_output, test10_error, test10_exit_status = run_command(test10_command)
print('Test Output: ' + str(test10_output))
print('Expected Test Output: ' + ' {"account":"1","vcc_amount":5.00,"vcc_file":"1_1.card"}')
print('----')
#print("Test 1 Error:")
#print(test1_error)
print('Test Exit Status: ' + str(test10_exit_status))
print('Expected Test Exit Status: 0')
print('-----------------------------------------------------')
print('-----------------------------------------------------')


print('-----------------------------------------------------')
print('-----------------------------------------------------')
# Test 11: Create an account 2 with 100 balance
test11_command = "java -jar mbec.jar -a 2 -n 100"
print('Testing command: ' + test11_command)
print('----')
test11_output, test11_error, test11_exit_status = run_command(test11_command)
print('Test Output: ' + test11_output)
print('Expected Test Output: ' + '{"account":"1","initial_balance":15.00}')
print('----')
#print("Test 1 Error:")
#print(test1_error)
print('Test Exit Status: ' + str(test11_exit_status))
print('Expected Test Exit Status: 0')
print('-----------------------------------------------------')
print('-----------------------------------------------------')