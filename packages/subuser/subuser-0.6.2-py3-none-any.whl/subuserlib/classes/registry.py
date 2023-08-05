# -*- coding: utf-8 -*-

"""
Each user's settings are stored in a "registry". This is a git repository with a set of json files which store the state of the subuser installation.
"""

#external imports
import os
import errno
import sys
from contextlib import contextmanager
import json
#internal imports
from subuserlib.classes import repositories
from subuserlib.classes import subusers
from subuserlib.classes import userOwnedObject
from subuserlib.classes.gitRepository import GitRepository
import subuserlib.print
import subuserlib.executablePath

class Registry(userOwnedObject.UserOwnedObject):
  def __init__(self,user,gitReadHash="master", ignoreVersionLocks=False, initialized = False):
    self.__subusers = None
    self.__changeLog = u""
    self.commit_message = None
    self.__changed = False
    self.logOutputVerbosity = 2
    self.initialized = initialized
    self.lastVerbosityLevel = None
    self.ignoreVersionLocks = ignoreVersionLocks
    if "SUBUSER_VERBOSITY" in os.environ:
      try:
        self.logOutputVerbosity = int(os.environ["SUBUSER_VERBOSITY"])
      except ValueError:
        subuserlib.print.printWithoutCrashing("Invalid verbosity setting! Verbosity may be set to any integer.")
    self.__repositories = None
    self.gitRepository = None
    self.gitReadHash = gitReadHash
    userOwnedObject.UserOwnedObject.__init__(self,user)
    self.registryDir = self.user.config["registry-dir"]
    self.logFilePath = os.path.join(self.registryDir,"commit_log")
    self.gitRepository = GitRepository(self.user,self.registryDir)

  @property
  def subusers(self):
    if self.__subusers is None:
      self.__subusers = subusers.Subusers(self.user)
    return self.__subusers

  @property
  def repositories(self):
    if not self.__repositories:
      self.__repositories = repositories.Repositories(self.user)
    return self.__repositories

  def ensureGitRepoInitialized(self):
    if not os.path.exists(os.path.join(self.user.config["registry-dir"],".git")):
      self.initialized = False
      # Ensure git is setup before we start to make changes.
      self.gitRepository.assertGitSetup()
      self.user.endUser.makedirs(self.user.config["registry-dir"])
      self.gitRepository.run(["init"])
      self.logChange("Initial commit.")
      self.commit("Initial commit.",_no_lock_needed = True)
    self.initialized = True

  def log(self,message,verbosityLevel=1,notify=False):
    """
    If the current verbosity level is equal to or greater than verbosityLevel, print the message to the screen.
    If the current verbosity level is equal to or greater than verbosityLevel minus one, add the message to the log.
    Do not mark the registry as changed.
    The notify option will create a popup dialog with the message if the notify-send command exists.
    """
    message = message.rstrip()
    if (verbosityLevel-1) <= self.logOutputVerbosity:
      self.__changeLog = self.__changeLog + message + u"\n"
    if self.lastVerbosityLevel == 2 and self.logOutputVerbosity == 2 and sys.stdout.isatty():
      CURSOR_UP_ONE = '\x1b[1A'
      ERASE_LINE = '\x1b[2K'
      print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
    if verbosityLevel <= self.logOutputVerbosity:
      subuserlib.print.printWithoutCrashing(message)
      if notify and subuserlib.executablePath.which("notify-send"):
        self.user.endUser.call(["notify-send",message])
    self.lastVerbosityLevel = verbosityLevel

  def logChange(self,message,verbosityLevel=1):
    """
    Add a log message to the registry's change log, and mark the registry as changed.
    """
    self.log(message,verbosityLevel=verbosityLevel)
    self.__changed = True

  def setChanged(self,changed=True):
    self.__changed = changed

  def logRenameCommit(self, message):
    """
    Add a new message to the top of the log.
    """
    self.__changeLog = message + u"\n" + self.__changeLog

  def commit(self,message=None,_no_lock_needed=False):
    """
    Git commit the changes to the registry files, installed-miages.json and subusers.json.
    """
    if (not self.user._has_lock) and (not _no_lock_needed):
      sys.exit("Programmer error. Committing to registry without first aquiring lock! Please report this incident to: https://github.com/subuser-security/subuser/issues")
    if self.__changed:
      self.repositories.save()
      self.subusers.save()
      with self.user.endUser.get_file(self.logFilePath) as fd:
        fd.write(self.__changeLog)
      self.gitRepository.run(["add","."])
      if message is None:
        if self.commit_message is not None:
          message = self.commit_message
        else:
          message = self.__changeLog
      self.gitRepository.commit(message)
      # Log to live log
      announcement = {}
      announcement["commit"] = self.gitRepository.getHashOfRef("master")
      self.logToLiveLog(announcement)
      self.__changed = False
      self.__changeLog = u""

  def logToLiveLog(self,announcement):
    announcementJson = json.dumps(announcement)
    liveLogDir=os.path.join(self.user.endUser.homeDir,".subuser/registry-live-log")
    if os.path.isdir(liveLogDir):
      for liveLogPid in os.listdir(liveLogDir):
        liveLogPath = os.path.join(liveLogDir,liveLogPid)
        try:
          liveLog = os.open(liveLogPath,os.O_WRONLY|os.O_NONBLOCK)
          os.write(liveLog,announcementJson)
        except OSError:
          pass
        # TODO Note: We don't close the file descriptors, because doing so makes the pipe close on the other end too. This would be a file descriptor leak if this method was used in any long running process(which it is not).

  def cleanOutOldPermissions(self):
    for permissions_folder_name in self.gitRepository.getFileStructureAtCommit(self.gitReadHash).lsFolders("permissions"):
      exists = os.path.exists(os.path.join(self.registryDir,"permissions",permissions_folder_name))
      if exists and permissions_folder_name not in self.subusers:
        self.logChange("Removing left over permissions for no-longer extant subuser %s"%permissions_folder_name,2)
        try:
          self.gitRepository.run(["rm","-r",os.path.join("permissions",permissions_folder_name)])
        except subuserlib.classes.gitRepository.GitException as e:
          self.log(" %s"%str(e))
