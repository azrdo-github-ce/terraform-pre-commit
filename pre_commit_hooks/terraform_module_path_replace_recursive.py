import os
import sys
import re

def getTFServer():
    for directory in os.listdir("."):
        if directory != ".git":
            for directories in os.walk(directory):
                if ".terraform" not in directories[0]:
                    for fileName in directories[2]:
                        if fileName == "remote-backend.tf":
                            filePath = os.getcwd() + '\\' + directories[0] + '\\' + fileName

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

    dirs = []
    for directory in os.listdir("."):
        if directory != ".git":
            for directories in os.walk(directory):
                if ".terraform" not in directories[0]:
                    for filename in directories[2]:
                        fullpath = os.getcwd() + '\\' + directories[0] + '\\' + filename
                        if fullpath not in dirs and filename != 'remote-backend.tf' and \
                            (filename.endswith(".tf") or filename.endswith(".tfvars")):
                                dirs.append(fullpath)

    for dir in dirs:
        with open(dir, 'r') as file :              
            filedata = file.read()

        filedata = filedata.replace(serverName, 'localterraform.com')

        with open (dir, 'w') as file :
            file.write(filedata)

if __name__ == '__main__':
    sys.exit(main())