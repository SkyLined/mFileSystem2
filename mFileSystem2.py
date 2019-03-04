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

def fsAbsoluteCleanPath(sPath):
  return re.match(r"^" r"(" r"\\\\\?\\" r"(?:UNC\\)?" r")?" r"(.+)" r"$", os.path.abspath(sPath)).group(2);

# Files
def fbIsFile(sPath):
  return cFileSystemFile(fsAbsoluteCleanPath(sPath)).fbIsFile();

def fo0GetFile(sPath):
  oFile = cFileSystemFile(fsAbsoluteCleanPath(sPath));
  return oFile if oFile.fbIsFile() else None;

def foGetFile(sPath):
  oFile = fo0GetFile(sPath);
  assert oFile, \
      "File %s not found!" % sPath;
  return oFile;

def foGetOrCreateFile(sPath):
  oFile = cFileSystemFile(fsAbsoluteCleanPath(sPath));
  if not oFile.fbIsFile():
    oFile.fCreate();
  return oFile;

def foCreateFile(sPath, sData = ""):
  oFile = cFileSystemFile(fsAbsoluteCleanPath(sPath));
  oFile.fWrite(sData);
  return oFile;

# Folders
def fbIsFolder(sPath):
  return cFileSystemFolder(fsAbsoluteCleanPath(sPath)).fbIsFolder();

def fo0GetFolder(sPath):
  oFolder = cFileSystemFolder(fsAbsoluteCleanPath(sPath));
  return oFolder if oFolder.fbIsFolder() else None;

def foGetFolder(sPath):
  oFolder = fo0GetFolder(sPath);
  assert oFolder, \
      "Folder %s not found!" % sPath;
  return oFolder;

def foGetOrCreateFolder(sPath):
  oFolder = cFileSystemFolder(fsAbsoluteCleanPath(sPath));
  if not oFolder.fbIsFolder():
    oFolder.fCreate();
  return oFolder;

def foCreateFolder(sPath):
  oFolder = cFileSystemFolder(fsAbsoluteCleanPath(sPath));
  assert not oFolder.fbIsFolder(), \
      "Folder %s already exists" % sPath;
  oFolder.fCreate();
  return oFolder;

# Zip Files
def fbIsZipFile(sPath):
  return cZipFile(fsAbsoluteCleanPath(sPath)).fbIsZipFile();

def fo0GetZipFile(sPath):
  oZipFile = cZipFile(fsAbsoluteCleanPath(sPath));
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
  oZipFile = cZipFile(fsAbsoluteCleanPath(sPath));
  if not oZipFile.fbIsZipFile():
    oZipFile.fCreate();
  return oZipFile;

def foCreateZipFile(sPath):
  oZipFile = cZipFile(fsAbsoluteCleanPath(sPath));
  oZipFile.fCreate();
  return oZipFile;
