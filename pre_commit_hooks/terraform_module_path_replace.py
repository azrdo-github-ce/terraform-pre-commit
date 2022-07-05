import os
import sys
import re

def getTFServer():
    for fileName in os.listdir("."):
        if fileName == "remote-backend.tf":
            filePath = os.path.join(os.getcwd(), fileName)

            with open(filePath, 'r') as file:
                toParse = file.read()
            
            parsed = toParse.split('\n')
            for line in parsed:
                if re.search('hostname', line):
                    hostname = line.split('=')
                    hostname = hostname[1].replace('"','')
                    hostname = hostname.strip()

                    return hostname
    
    hostname = 'localterraform.com'
    return hostname

def main():
    serverName = getTFServer()

    files = []
    for fileName in os.listdir("."):
        fullpath = os.path.join(os.getcwd(), fileName)
        if fullpath not in files and fileName != 'remote-backend.tf' and \
            (fileName.endswith(".tf") or fileName.endswith(".tfvars")):
                files.append(fullpath)

    for fileName in files:
        with open(fileName, 'r') as file :
            filedata = file.read()

        filedata = filedata.replace(serverName, 'localterraform.com')

        with open (fileName, 'w') as file :
            file.write(filedata)

if __name__ == '__main__':
    sys.exit(main())