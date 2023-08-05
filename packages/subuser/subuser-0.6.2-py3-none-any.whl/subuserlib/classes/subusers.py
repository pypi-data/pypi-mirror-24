# -*- coding: utf-8 -*-

"""
This is the list of subusers controlled by a given user.
"""

#external imports
import os
import json
import collections
import sys
#internal imports
from subuserlib.classes.fileBackedObject import FileBackedObject
from subuserlib.classes.userOwnedObject import UserOwnedObject
from subuserlib.classes.subuser import Subuser
import subuserlib.classes.imageSource

class Subusers(dict,UserOwnedObject,FileBackedObject):
  """
  A subusers object stores the set of all subusers owned by a given user.
  """
  def __init__(self,user):
    UserOwnedObject.__init__(self,user)
    registryFileStructure = self.user.registry.gitRepository.getFileStructureAtCommit(self.user.registry.gitReadHash)
    if self.user.registry.initialized and "subusers.json" in registryFileStructure.lsFiles("./"):
      serializedUnlockedSubusersDict = json.loads(registryFileStructure.read("subusers.json"), object_pairs_hook=collections.OrderedDict)
      self._loadSerializedSubusersDict(serializedUnlockedSubusersDict,locked=False)
    if (not self.user.registry.ignoreVersionLocks) and os.path.exists(self.user.config["locked-subusers-path"]):
      with open(self.user.config["locked-subusers-path"],"r") as fileHandle:
        self._loadSerializedSubusersDict(json.load(fileHandle, object_pairs_hook=collections.OrderedDict),locked=True)

  def serializeToDict(self):
    serializedDict=collections.OrderedDict()
    serializedDict["locked"]=collections.OrderedDict()
    serializedDict["unlocked"]=collections.OrderedDict()
    for subuser in self.getSortedList():
      serializedSubuser = collections.OrderedDict()
      serializedSubuser["source-repo"] = subuser.sourceRepoName
      serializedSubuser["image-source"] = subuser.imageSourceName
      serializedSubuser["executable-shortcut-installed"] = subuser.executableShortcutInstalled
      serializedSubuser["entrypoints-exposed"] = subuser.entryPointsExposed
      serializedSubuser["docker-image"] = subuser.imageId
      serializedSubuser["service-subusers"] = subuser.serviceSubuserNames
      serializedSubuser["non-default-home-dir"] = subuser.nonDefaultHomeDir
      if subuser.locked:
        serializedDict["locked"][subuser.name] = serializedSubuser
      else:
        serializedDict["unlocked"][subuser.name] = serializedSubuser
    return serializedDict

  def save(self):
    """
    Save the list of subusers to disk.
    """
    serializedDict = self.serializeToDict()
    with self.user.endUser.get_file(os.path.join(self.user.config["registry-dir"],"subusers.json"), 'w') as file_f:
      json.dump(serializedDict["unlocked"], file_f, indent=1, separators=(',', ': '))
    with self.user.endUser.get_file(os.path.join(self.user.config["locked-subusers-path"]), 'w') as file_f:
      json.dump(serializedDict["locked"], file_f, indent=1, separators=(',', ': '))

  def _loadSerializedSubusersDict(self,serializedSubusersDict,locked):
    """
    Load the serialized subusers json file into memory.
    """
    for subuserName, subuserAttributes in serializedSubusersDict.items():
      def retrieveAttribute(name,default):
        if name in subuserAttributes:
          return subuserAttributes[name]
        else:
          return default
      repoName = subuserAttributes["source-repo"]
      imageSourceName = subuserAttributes["image-source"]
      imageId = retrieveAttribute("docker-image",None)
      serviceSubuserNames = retrieveAttribute("service-subusers",[])
      executableShortcutInstalled = retrieveAttribute("executable-shortcut-installed",False)
      entrypointsExposed = retrieveAttribute("entrypoints-exposed",False)
      nonDefaultHomeDir = retrieveAttribute("non-default-home-dir",None)
      self[subuserName] = Subuser(self.user,subuserName,imageSourceName=imageSourceName,repoName=repoName,imageId=imageId,executableShortcutInstalled=executableShortcutInstalled,locked=locked,serviceSubuserNames=serviceSubuserNames,entrypointsExposed=entrypointsExposed,nonDefaultHomeDir=nonDefaultHomeDir)

  def getSortedList(self):
    """
    Return a list of subusers sorted by name.
    """
    return list(sorted(self.values(),key=lambda subuser:subuser.name))
