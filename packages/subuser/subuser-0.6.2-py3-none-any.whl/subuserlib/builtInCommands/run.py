#!/usr/bin/python3
# -*- coding: utf-8 -*-
#external imports
import sys
import optparse
import os
#internal imports
from subuserlib.classes.user import User
import subuserlib.commandLineArguments
import subuserlib.profile

##############################################################
def parseCliArgs(sysargs):
  usage = "usage: subuser run [arguments-for-run-command] SUBUSER-NAME [arguments-for-subuser]"
  description = """Run the given subuser.

For example:

    $ subuser run iceweasel

Will launch the subuser named iceweasel

To launch the subuser with another executable than it's default use the ``--entrypoint`` option.

If the SUBUSER_EXTRA_DOCKER_ARGS environment variable is set. Those arguments will be passed to Docker.
"""
  parser=optparse.OptionParser(usage=usage,description=description,formatter=subuserlib.commandLineArguments.HelpFormatterThatDoesntReformatDescription())
  parser.add_option("--entrypoint", dest="entrypoint",default=None,help="Override the default executable for this subuser.")
  parser.add_option("--dry", dest="dry",action="store_true",default=False,help="Dry run, only display what commands would be called by subuser, don't actually run anything.")
  parser.add_option("--dry-one-arg-per-line", dest="dry_one_arg_per_line",action="store_true",default=False,help="Dry run, only display what commands would be called by subuser, don't actually run anything. Displays one argument per line when displaying the commands that would be calleed by subuser, in order to improve the ability for the test suit to detect changes to the command using a line based diff.")
  return parser.parse_args(args=sysargs)

class ArgParser():
  def __init__(self):
    self.preArgs = []
    self.subuserName = None
    self.subuserArgs = []
    self.consumedSubuserName = False

  def readArg(self,arg):
    if not self.consumedSubuserName:
      if arg.startswith("-"):
        self.preArgs.append(arg)
      else:
        self.subuserName = arg
        self.consumedSubuserName = True
    else:
      self.subuserArgs.append(arg)

#################################################################################################

@subuserlib.profile.do_cprofile
def runCommand(args):
  preArgs = []
  argParser = ArgParser()
  for arg in args:
    argParser.readArg(arg)

  if not argParser.consumedSubuserName:
    print("Subuser name not listed.")
    parseCliArgs(["--help"])

  options,_ = parseCliArgs(argParser.preArgs)

  user = User()
  if not "SUBUSER_VERBOSITY" in os.environ:
    user.registry.logOutputVerbosity = 0
  if argParser.subuserName in user.registry.subusers:
    try:
      extraDockerFlags = os.environ["SUBUSER_EXTRA_DOCKER_ARGS"].split(" ")
    except KeyError:
      extraDockerFlags = []
    try:
      subuser = user.registry.subusers[argParser.subuserName]
      runtime = subuser.getRuntime(os.environ,extraDockerFlags=extraDockerFlags,entrypoint=options.entrypoint)
      if runtime:
        if options.dry or options.dry_one_arg_per_line:
          if subuser.imageId:
            print("The image will be prepared using the Dockerfile:")
            print(subuser.getRunReadyImage().generateImagePreparationDockerfile())
            print("The command to launch the image is:")
            if options.dry:
              print(runtime.getPrettyCommand(argParser.subuserArgs))
            elif options.dry_one_arg_per_line:
              print("docker \\")
              print("  `"+"` \\\n  `".join(runtime.getCommand(argParser.subuserArgs))+"`")
          else:
            sys.exit("There is no installed image for this subuser. Cannot run.")
        else:
          runtime.run(argParser.subuserArgs)
      else:
        sys.exit("The subuser's image failed to build. Please use the subuser registry log and subuser repair commands for more information.")
    except (subuserlib.classes.subuser.SubuserHasNoPermissionsException,subuserlib.classes.subuserSubmodules.run.runtimeCache.NoRuntimeCacheForSubusersWhichDontHaveExistantImagesException) as e:
      sys.exit(str(e))
  else:
    sys.exit("Subuser "+argParser.subuserName + " not found.\nUse --help for help.")
