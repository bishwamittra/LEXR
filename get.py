import os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--token", help="token of dir", default="", type=str)
args = parser.parse_args()
path="nscc:/home/projects/11000744/bishwa/xRNN" +args.token+"/" 
os.system("mkdir backup_output/xRNN"+args.token+"/")
os.system("rsync -vap "+path+"output/* backup_output/xRNN"+args.token+"/")
