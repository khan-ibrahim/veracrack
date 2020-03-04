import os
import subprocess
import sys
import csv
import time
import configparser

configFilePath = '''veracrack_config.txt'''

#Attemts to decrypt and mount given encrypted container file with given password
#using sha-512 hash
#Returns true if successfull, returns false if unsuccessful.
def decrypt(targetFilePath, password):
    cmd = veracryptExePath + r''' /v ''' + targetFilePath + r''' /l ''' \
    + driveLetter + ''' /p "''' + password \
    + r'''" /e /h n /a /s /nowaitdlg /hash sha-512 /q'''

    subprocess.run(cmd)

    #check success
    decryptedPath = driveLetter + ''':\\'''
    return os.path.exists(decryptedPath)

#given an array of passwords, attempts each password on a target veracrypt
#encrypted file container until password is found or passwords are exhausted.
#Returns true if successfull, returns false if unsuccessful.
def tryPasswords(targetFilePath, passwordArray):
    print('Encrypted Target: {}'.format(targetFilePath))
    startTime = time.perf_counter()
    passwordsAttempted = 0
    for password in passwordArray:
        passwordsAttempted += 1
        if decrypt(targetFilePath, password):
            endTime = time.perf_counter()
            print('''\n------SUCCESS-----\n{}\n'''.format(password))
            print('''Seconds Elapsed:{}s'''.format(endTime-startTime))
            print('''Passwords Attempted:{}'''.format(passwordsAttempted))
            print('''Seconds per Password Attempt:{}s/p'''.format((endTime-startTime)/passwordsAttempted))
            return True
        elif verboseMode:
            print('''Failed:{}'''.format(password))
    print('FAILED. All passwords exhausted')
    return False

def importConfig(configFilePath):
    if(not os.path.exists(configFilePath)):
        print('ERROR: Config not found at configFilePath: {}'\
        .format(os.path.abspath(configFilePath)))
        print('Generate Sample Config: python veracrack.py --configGen')
        exit(1)

    config = configparser.ConfigParser()
    config.read(configFilePath)

    global veracryptExePath
    global driveLetter
    global verboseMode
    veracryptExePath = config['CONFIGURATION']['veracryptExePath']
    driveLetter = config['CONFIGURATION']['driveLetter']
    verboseMode = config['CONFIGURATION']['verboseMode'] == 'True'

    if(not os.path.exists(veracryptExePath)):
        print('ERROR: No file found at: {}'.format(veracryptExePath))
        print('''Correct the 'veracryptexepath' field in config file at: {}'''\
        .format(os.path.abspath(configFilePath)))
        print('See README.md for further details')
        exit(1)
    if verboseMode:
        print('config imported')

    return

def generateSampleConfig(configFilePath):
    config = configparser.ConfigParser()
    config['CONFIGURATION'] = {'veracryptExePath':r'C:/REPLACE_WITH_YOUR_EXE_PATH' \
    + '/VeraCrypt-x64.exe', 'driveLetter':'A', 'verboseMode':'False'}
    with open(configFilePath, 'w') as configFile:
        config.write(configFile)
    print('Sample config generated at {}.'.format(os.path.abspath(configFilePath)))
    print(''''veracryptexepath' field must be set before using application''')
    return

def main(targetFilePath, passwordCSV):
    print('Starting VeraCrack v1.0\n')
    importConfig(configFilePath)
    passwordArray = []
    with open(passwordCSV, 'r', encoding='utf-8-sig') as f:
        for line in f:
            passwordArray.append(str.strip(line))
    return tryPasswords(targetFilePath, passwordArray)

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1]=='--configGen':
        generateSampleConfig(configFilePath)
    elif len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print('''USAGE: python veracrack.py <targetFilePath> <passwords.csv>''')
        print('''\nMANDATORY before first use: python veracrack.py --configGen''')
        print('''Use elevated command prompt to avoid repeated reminders''')
        print('''SEE README.md for further details''')
