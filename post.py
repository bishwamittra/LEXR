import os
path="nscc:/home/projects/11000744/bishwa/xRNN/"

# choose files/folder to copy to cluster
# os.system("rsync -vap lstar_extraction/ "+path+"lstar_extraction/")
os.system("./clean.sh")
os.system("rsync -vap ltlf2dfa/ "+path+"ltlf2dfa/")
os.system("rsync -vap RNN2DFA/ "+path+"RNN2DFA/")
os.system("rsync -vap PACTeacher/ "+path+"PACTeacher/")
os.system("rsync -vap samples2ltl/ "+path+"samples2ltl/")
os.system("rsync -vap *.py "+path)
os.system("rsync -vap *.sh "+path)
os.system("rsync -vap *.ipynb "+path)
os.system("rsync -vap *.pbs "+path)



