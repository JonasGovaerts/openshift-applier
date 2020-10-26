import git
import sys
import os
import time
import subprocess
from datetime import datetime

def log(logMessage):
  now = datetime.now()
  dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
  print('{"timestamp":"'+dt_string+'","message":"'+logMessage+'"}')

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
    with git_repo.config_writer() as git_config:
      git_config.set_value('user','email', 'test@test.com')
      git_config.set_value('user','name', 'test')
    log("Initialized dummy git credentials")
  except Exception as exception:
    error = str(exception).replace('\n', ' ').replace('\r', '')
    log("Something went wrong: "+error)
    sys.exit()

def gitClone():
  try:
    repo_dir = "/resources/git"
    log("Cloning git repository "+repo+" into "+repo_dir)
    if "github" not in repo:
       git_url = "https://"+username+":"+password+"@"+repo
       git.Repo.clone_from(git_url, repo_dir)
    else:
       git_url = "https://"+repo
       git.Repo.clone_from(git_url, repo_dir)
  except Exception as exception:
    error = str(exception).replace('\n', ' ').replace('\r', '')
    log("Something went wrong: "+error)
    sys.exit()

def gitPull():
  try:
    log("Pulling new updates from git...")
    current_commit_id = git_repo.head.commit.hexsha
    git_repo.remotes.origin.pull()
    new_commit_id = git_repo.head.commit.hexsha
    if new_commit_id == current_commit_id:
        log("No new changes were found")
        log("Latest commit: "+current_commit_id)
    else:
        log("Pulled latest changes from git")
        log("Latest commit: "+new_commit_id)
  except Exception as exception:
    error = str(exception).replace('\n', ' ').replace('\r', '')
    log("Something went wrong: "+error)
    sys.exit()

def selectBranch():
  try:
    log("Switching to branch "+branch)
    git_repo.git.checkout(branch)
  except Exception as exception:
    error = str(exception).replace('\n', ' ').replace('\r', '')
    log("Something went wrong: "+error)
    sys.exit()

def ocApply():
  try:
    findCMD = 'find -L /resources/git/'+subdir+' -type f \( -name \*.json -o -name \*.yml -o -name \*.yaml \)'
    out = subprocess.Popen(findCMD, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout,stderr = out.communicate()
    filelist = stdout.decode().split()
  
    for x in filelist:
      command = 'oc apply -f '+x
      output= subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      stdout,stderr = output.communicate()
      if not stderr.rstrip():
        log(str(stdout.decode().rstrip()))
      else:
        log(str(stderr.decode().rstrip()))
  except Exception as exception:
    error = str(exception).replace('\n', ' ').replace('\r', '')
    log("Something went wrong: "+error)
    sys.exit()

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

gitClone() # Clone the git repo to the location /resources/git
git_repo = git.Repo('/resources/git') # initialize the git_repo variable to globally use it
selectBranch()
gitDefinition()

while True:
    gitPull()
    ocApply()
    pause()
