#!/usr/bin/python

import os
import time
import subprocess
from datetime import datetime

sleep = float(os.environ['TIMER'])
repo = os.environ['GITREPO']
branch = os.environ['BRANCH']

def gitDefinition():
	try:
	  log("Initializing git credentials")
	  command = "git config --global user.name 'test' && git config --global user.email 'test@test.com'"
	  output = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE)
          log("Initialized dummy git credentials")
	except:
	  log("Couldn't initialize dummy git credentials")

def gitClone():
	try:
	  log("Cloning git repository "+repo+" into /resources/git")
  	  command = "echo $GITREPO | awk -F 'https://' -v a=$USERNAME -v b=$PASSWORD -v c='git clone https://' -v d=':' -v e='@'  -v f=' /resources/git -b ' -v g=$BRANCH '{print c a d b e $2 f g}'"
	  output = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE)
	  clone = output.stdout.read()
	  subprocess.call([clone], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	  log("Cloned git repositry successfully in /resources/git")
	except:
	  log("Something went wrong")
	  

def gitPull():
	try:
	  log("Pulling new updates from git...")
	  command = "git --work-tree=/resources/git/ --git-dir=/resources/git/.git pull origin"+branch
	  output = subprocess.Popen([command], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	  pullResult,stderr = output.communicate()
	  if "Already" in pullResult:
	    log("No new changes were found")
	  else:
	    log("Pulled latest changes from the git repo "+repo)
	except:
	  pullResult,stderr = output.communicate()
	  log("stderr")

def ocApply():
	try:
	  subdir = os.environ['DIR']
	  findCMD = 'find /resources/git/'+subdir+' -type f \( -name \*.json -o -name \*.yml -o -name \*.yaml \)'
	  out = subprocess.Popen(findCMD, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	  stdout,stderr = out.communicate()
	  filelist = stdout.decode().split()

	  for x in filelist:
	    command = 'oc apply -f '+x
	    subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	    log("applied object "+x)
	except:
	  log("Something went wrong, are there objects available in /resources/git/"+subdir)

def log(logMessage):
	now = datetime.now()
	dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
	print('{"timestamp"}:{"'+dt_string+'"}'+'{"message"}:{"'+logMessage+'"}')


#### Application Run time #####
log("openshift-applier is starting...")
time.sleep(3)
gitDefinition()
gitClone()

while True:
  gitPull()
  ocApply()
  
  try:
    log("sleeping for "+sleep+" seconds")
    time.sleep(sleep)
  except:
    log("sleeping for 60 seconds")
    time.sleep(60)
