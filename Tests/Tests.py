import os, sys;

# Augment the search path to make cBugId a package and have access to its modules folder.
sTestsFolderPath = os.path.dirname(os.path.abspath(__file__));
sMainFolderPath = os.path.dirname(sTestsFolderPath);
sParentFolderPath = os.path.dirname(sMainFolderPath);
sModulesFolderPath = os.path.join(sMainFolderPath, "modules");
asOriginalSysPath = sys.path[:];
sys.path = [sParentFolderPath, sModulesFolderPath] + asOriginalSysPath;
# Save the list of names of loaded modules:
asOriginalModuleNames = sys.modules.keys();

import mFileSystem2;

# Sub-packages should load all modules relative, or they will end up in the global namespace, which means they may get
# loaded by the script importing it if it tries to load a differnt module with the same name. Obviously, that script
# will probably not function when the wrong module is loaded, so we need to check that we did this correctly.
asUnexpectedModules = list(set([
  sModuleName.lstrip("_").split(".", 1)[0] for sModuleName in sys.modules.keys()
  if not (
    sModuleName in asOriginalModuleNames # This was loaded before
    or sModuleName.lstrip("_").split(".", 1)[0] in [
      "mFileSystem2",
      # These packages are loaded by mFileSystem2:
      "mWindowsSDK",
      # These built-in modules are loaded by these packages:
      "binascii", "bz2", "cStringIO", "collections", "ctypes", "fnmatch", "gc",
      "heapq", "io", "itertools", "keyword", "msvcrt", "platform", "shutil",
      "string", "strop", "struct", "subprocess", "thread", "threading", "time", 
      "zipfile", "zlib"
    ]
  )
]));
assert len(asUnexpectedModules) == 0, \
      "Module(s) %s was/were unexpectedly loaded!" % ", ".join(sorted(asUnexpectedModules));

from fTestFileFunctions import fTestFileFunctions;
from fTestFolderFunctions import fTestFolderFunctions;
from fTestZipFileFunctions import fTestZipFileFunctions;

sTempFolderPath = os.environ["TEMP"];
assert mFileSystem2.fbIsFolder(sTempFolderPath), \
    "Cannot find %s" % sTempFolderPath;

print "* Running tests...";
fTestFileFunctions();
fTestFolderFunctions();
fTestZipFileFunctions();
print "+ Done.";
