import os

def update_modules_path():
    dirs = []
    for filename in os.listdir("."):
        if (os.path.realpath(filename) not in dirs and \
                filename != 'remote-backend.tf' and \
                    (filename.endswith(".tf") or filename.endswith(".tfvars"))):           
            dirs.append(os.path.realpath(filename))
    
    for dir in dirs:
        with open(dir, 'r') as file :
            filedata = file.read()
        
        filedata = filedata.replace('dev.dc04.ptfe.cnb.com', 'localterraform.com')
        filedata = filedata.replace('prod.dc04.ptfe.cnb.com', 'localterraform.com')

        with open (dir, 'w') as file :
            file.write(filedata)

update_modules_path()