import argparse
import os
import subprocess
import sys
import re

def main(argv=None):
    parser = argparse.ArgumentParser(
        description="""Run terraform-docs on a set of files. Follows the standard convention of
                       pulling the documentation from main.tf in order to replace the entire
                       README.md file each time."""
    )
    parser.add_argument(
        '--dest', dest='dest', default='README.md',
    )
    parser.add_argument(
        '--sort-inputs-by-required', dest='sort', action='store_true',
    )
    parser.add_argument(
        '--with-aggregate-type-defaults', dest='aggregate', action='store_true',
    )
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)

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

    retval = 0

    for dir in dirs:
        try:
            procArgs = []
            procArgs.append('terraform-docs')
            if args.sort:
                procArgs.append('--sort-inputs-by-required')
            if args.aggregate:
                procArgs.append('--with-aggregate-type-defaults')
            procArgs.append('md')
            procArgs.append("./{dir}".format(dir=dir))
            procArgs.append('>')
            procArgs.append("./{dir}/{dest}".format(dir=dir,dest=args.dest))
            subprocess.check_call(" ".join(procArgs), shell=True)

            content = ''
            with open("./{dir}/{dest}".format(dir=dir,dest=args.dest), 'r') as theFile:
                content=theFile.read()
            content = re.sub(r"^\s*$^\s*$","", content, 0, re.MULTILINE)
            with open("./{dir}/{dest}".format(dir=dir,dest=args.dest), 'w') as theFile:
                theFile.write(content)
        except subprocess.CalledProcessError as e:
            print(e)
            retval = 1
    return retval


if __name__ == '__main__':
    sys.exit(main())
