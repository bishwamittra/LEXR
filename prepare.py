import os

# on the server end
os.system("tar -xvf file_to_send.tar.gz")
os.system("rm file_to_send.tar.gz")

#when to send files to mac
os.system("tar -czvf output/output.tar.gz output/*")