import os, re, sys;

# Augment the search path: look in main folder, parent folder or "modules" child folder, in that order.
sMainFolderPath = os.path.dirname(os.path.abspath(__file__));
sParentFolderPath = os.path.normpath(os.path.join(sMainFolderPath, ".."));
sModulesFolderPath = os.path.join(sMainFolderPath, "modules");
asOriginalSysPath = sys.path[:];
sys.path = [sMainFolderPath, sParentFolderPath, sModulesFolderPath] + sys.path;

# Load external dependecies to make sure they are available and shown an error
# if any one fails to load. This error explains where the missing component
# can be downloaded to fix the error.
for (sModuleName, sDownloadURL) in [
  ("mWindowsAPI", "https://github.com/SkyLined/mWindowsAPI/"),
]:
  try:
    __import__(sModuleName, globals(), locals(), [], -1);
  except ImportError as oError:
    if oError.message == "No module named %s" % sModuleName:
      print "*" * 80;
      print "mFileSystem2 depends on %s which you can download at:" % sModuleName;
      print "    %s" % sDownloadURL;
      print "After downloading, please save the code in this folder:";
      print "    %s" % os.path.join(sModulesFolderPath, sModuleName);
      print " - or -";
      print "    %s" % os.path.join(sParentFolderPath, sModuleName);
      print "Once you have completed these steps, please try again.";
      print "*" * 80;
    raise;

# Restore the search path
sys.path = asOriginalSysPath;

from .cFileSystemFile import cFileSystemFile;
from .cFileSystemFolder import cFileSystemFolder;
from .cZipFile import cZipFile;
from fsGetValidName import fsGetValidName;

# Files
def fbIsFile(sPath):
  return cFileSystemFile(sPath).fbIsFile();

def fo0GetFile(sPath):
  oFile = cFileSystemFile(sPath);
  return oFile if oFile.fbIsFile() else None;

def foGetFile(sPath):
  oFile = fo0GetFile(sPath);
  assert oFile, \
      "File %s not found!" % sPath;
  return oFile;

def foGetOrCreateFile(sPath):
  oFile = cFileSystemFile(sPath);
  if not oFile.fbIsFile():
    oFile.fCreate();
  return oFile;

def foCreateFile(sPath, sData = ""):
  oFile = cFileSystemFile(sPath);
  oFile.fWrite(sData);
  return oFile;

# Folders
def fbIsFolder(sPath):
  return cFileSystemFolder(sPath).fbIsFolder();

def fo0GetFolder(sPath):
  oFolder = cFileSystemFolder(sPath);
  return oFolder if oFolder.fbIsFolder() else None;

def foGetFolder(sPath):
  oFolder = fo0GetFolder(sPath);
  assert oFolder, \
      "Folder %s not found!" % sPath;
  return oFolder;

def foGetOrCreateFolder(sPath):
  oFolder = cFileSystemFolder(sPath);
  if not oFolder.fbIsFolder():
    oFolder.fCreate();
  return oFolder;

def foCreateFolder(sPath):
  oFolder = cFileSystemFolder(sPath);
  assert not oFolder.fbIsFolder(), \
      "Folder %s already exists" % sPath;
  oFolder.fCreate();
  return oFolder;

# Zip Files
def fbIsZipFile(sPath):
  return cZipFile(sPath).fbIsZipFile();

def fo0GetZipFile(sPath):
  oZipFile = cZipFile(sPath);
  return oZipFile if oZipFile.fbIsZipFile() else None;

def foGetZipFile(sPath):
  oFile = fo0GetFile(sPath);
  assert oFile, \
      "File %s not found!" % sPath;
  oZipFile = oFile.foAsZipFile();
  assert oZipFile.fbIsZipFile(), \
      "File %s is not a valid zip file!" % sPath;
  return oZipFile;

def foGetOrCreateZipFile(sPath):
  oZipFile = cZipFile(sPath);
  if not oZipFile.fbIsZipFile():
    oZipFile.fCreate();
  return oZipFile;

def foCreateZipFile(sPath):
  oZipFile = cZipFile(sPath);
  oZipFile.fCreate();
  return oZipFile;
