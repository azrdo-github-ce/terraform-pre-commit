import os
import sys

def main():
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
        
        filedata = filedata.replace('dev.dc04.ptfe.cnb.com', 'localterraform.com')
        filedata = filedata.replace('prod.dc04.ptfe.cnb.com', 'localterraform.com')

        with open (dir, 'w') as file :
            file.write(filedata)

if __name__ == '__main__':
    sys.exit(main())