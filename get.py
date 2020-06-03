import os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--token", help="token of dir", default="", type=str)
parser.add_argument("--mpi", action='store_true')
args = parser.parse_args()


if(args.mpi):
    path="bghosh@contact.mpi-sws.org:/home/bghosh/Desktop/" 
    os.system("rm backup_output/mpi" +args.token+"/")
    os.system("mkdir backup_output/mpi" +args.token+"/" )
    os.system("rsync -vaP "+path+"output.tar.gz backup_output/mpi" +args.token+"/")
    os.system("tar -xvf backup_output/mpi" +args.token+"/output.tar.gz -C backup_output/mpi" +args.token+"/")
    # os.system("mv backup_output/mpi" +args.token+"/output/* backup_output/mpi" +args.token+"/")
    pass

else:
    path="nscc:/home/projects/11000744/bishwa/xRNN" +args.token+"/" 
    os.system("mkdir backup_output/xRNN"+args.token+"/")
    os.system("rsync -vaP "+path+"output/output.tar.gz backup_output/xRNN"+args.token+"/")
    os.system("tar -xvf backup_output/xRNN"+args.token+"/output.tar.gz -C backup_output/xRNN"+args.token+"/")


