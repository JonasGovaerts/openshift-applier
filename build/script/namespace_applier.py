#!/usr/bin/python

import sys
import os
import time
import subprocess
from datetime import datetime

def pause():
	try:
	  log("sleeping for " + timer + " seconds")
          sleep_timer = float(timer)
	  time.sleep(sleep_timer)
	except:
	  log("sleeping for 60 seconds")
	  time.sleep(60)

def gitDefinition():
	try:
	  log("Initializing git credentials")
	  command = "git config --global user.name 'test' && git config --global user.email 'test@test.com'"
	  output = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE)
          log("Initialized dummy git credentials")
	except:
	  log("Couldn't initialize dummy git credentials")
	  sys.exit()

def gitClone():
	try:
	  log("Cloning git repository "+repo+" into /resources/git")
	  if "github" not in repo:
  	    command = "git clone https://"+username+":"+password+"@"+repo+" --single-branch -b "+branch+" /resources/git"
	  else:
	    command = "git clone https://"+repo+" --single-branch -b "+branch+" /resources/git"
	  log(command)
	  output = subprocess.Popen([command], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
          time.sleep(5)
	  stdout,stderr = output.communicate()
	  if stderr.strip():
            log("Exiting: Could not clone git repository!")
	    sys.exit()
          else:
	    log("Cloned git repositry successfully in /resources/git")
	except:
	  sys.exit()

def gitPull():
	try:
	  log("Pulling new updates from git...")
	  command = "git --work-tree=/resources/git/ --git-dir=/resources/git/.git pull origin "+branch
	  output = subprocess.Popen([command], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	  stdout,stderr = output.communicate()
	  if "Already" in stdout:
	    log("No new changes were found")
	  else:
	    log("Pulled latest changes from the git repo "+repo)
	  command = "git --work-tree=/resources/git/ --git-dir=/resources/git/.git log --pretty=oneline | head -n 1 | awk '{print $1}'"
	  output = subprocess.Popen([command], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	  stdout,stderr = output.communicate()
	  log("Latest commit: "+stdout.strip())
	except:
	  log("Couldn't pull new updates from git")
	  sys.exit()

def ocApply():
	try:
	  findCMD = 'find -L /resources/git'+subdir+' -type f \( -name \*.json -o -name \*.yml -o -name \*.yaml \)'
	  out = subprocess.Popen(findCMD, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	  stdout,stderr = out.communicate()
	  filelist = stdout.decode().split()

	  for x in filelist:
	    command = 'oc apply -f '+x
	    output= subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	    stdout,stderr = output.communicate()
	    if not stderr.rstrip():
	      log(stdout.rstrip())
	    else:
	      log(stderr.rstrip())
	except:
	  log("Something went wrong, are there any objects available in /resources/git/"+subdir)
	  sys.exit()

def log(logMessage):
	now = datetime.now()
	dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
	print('{"timestamp"}:{"'+dt_string+'"}'+'{"message"}:{"'+logMessage+'"}')


#### Application Run time #####
log("openshift-applier is starting...")
time.sleep(5)
try:
  log("Initializing variables")
  username = os.environ['USERNAME']
  password = os.environ['PASSWORD']
  repo = os.environ['GITREPO'].split('https://')[1]
  branch = os.environ['BRANCH']
  timer = os.environ['TIMER']
  subdir = os.environ['DIR']
except:
  log("Couln't initialize needed variables, required variables are: USERNAME, PASSWORD, GITREPO, BRANCH, TIMER, DIR")
  sys.exit()

gitDefinition()
gitClone()

while True:
  gitPull()
  ocApply()
  pause()
  print("\n")
