import os;

from .iFileSystemChild import iFileSystemChild;
from .iFolder import iFolder;

class cFileSystemFolder(iFileSystemChild, iFolder):
  def __init__(oSelf, sName, oParentFolder = None):
    iFileSystemChild.__init__(oSelf, sName, oParentFolder);
    iFolder.__init__(oSelf);
  
  def fRefresh(oSelf):
    asChildFileNames = [];
    asChildFolderNames = [];
    for sFileOrFolderName in os.listdir(oSelf.sWindowsPath):
      sFileOrFolderWindowsPath = os.path.join(oSelf.sWindowsPath, sFileOrFolderName);
      if os.path.isdir(sFileOrFolderWindowsPath):
        asChildFileNames.append(sFileOrFolderName);
      elif os.path.isfile(sFileOrFolderWindowsPath):
        asChildFolderNames.append(sFileOrFolderName);
    oSelf.fUpdateChildFolderAndFileNames(asChildFolderNames, asChildFileNames);
  
  def fCreate(oSelf):
    if not os.path.isdir(oSelf.sWindowsPath):
      os.makedirs(oSelf.sWindowsPath);
  
  def fSetCurrent(oSelf):
    # Try using the basic path
    os.chdir(oSelf.sPath);
    if os.getcwd() == oSelf.sPath: return;
    # Try using the windows path.
    os.chdir(oSelf.sWindowsPath);
    assert os.getcwd() == oSelf.sWindowsPath, \
      "Cannot set current working directory to %s" % oSelf.sWindowsPath;
    
  def fDeleteChildren(oSelf):
    if not oSelf.fbIsFolder():
      return;
    oSelf.fRefresh();
    for oFolder in oSelf.faoGetChildFolders():
      oFolder.fDelete();
    for oFile in oSelf.faoGetChildFiles():
      oFile.fDelete();
  
  def fDelete(oSelf):
    if not oSelf.fbIsFolder():
      return;
    oSelf.fDeleteChildren();
    os.rmdir(oSelf.sWindowsPath);
  
  def foConstructChildFile(oSelf, sName):
    cFile = cZipFile if (sName[-4:].lower() == ".zip") else cFileSystemFile;
    return cFile(sName, oSelf);
  
  def foConstructChildFolder(oSelf, sName):
    return cFileSystemFolder(sName, oSelf);

  def foGetOrCreateChildFolder(oSelf, sName):
    oChildFolder = oSelf.foConstructChildFolder(sName);
    oChildFolder.fCreate();
    return oChildFolder;

from .cFileSystemFile import cFileSystemFile;
from .cZipFile import cZipFile;
