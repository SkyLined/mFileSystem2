import os, re;

from .iChild import iChild;

class iFileSystemChild(iChild):
  def __init__(oSelf, sPath, oParentFolder):
    iChild.__init__(oSelf, sPath, oParentFolder);
    
    oSelf.__sWindowsPath = None;
    oSelf.__sDOSPath = None;
  
  def fbExists(oSelf):
    return os.path.exists(oSelf.sWindowsPath);
  
  def fbIsFolder(oSelf):
    return os.path.isdir(oSelf.sWindowsPath);
  
  def fbIsFile(oSelf):
    return os.path.isfile(oSelf.sWindowsPath);
  
  def fSetParentFolderForPath(oSelf, sPath):
    from .cFileSystemFolder import cFileSystemFolder;
    oSelf.oParentFolder = cFileSystemFolder(sPath, None);
  
  # http://msdn.microsoft.com/en-us/library/aa365247.aspx
  @property
  def sWindowsPath(oSelf):
    if oSelf.__sWindowsPath is None:
      oSelf.__sWindowsPath = fsGetWindowsPath(oSelf.sPath);
    return oSelf.__sWindowsPath;
  
  @property
  def s0DOSPath(oSelf):
    if not oSelf.__sDOSPath:
      oSelf.__sDOSPath = fs0GetDOSPath(oSelf.sPath);
    return oSelf.__sDOSPath;

from .fsGetWindowsPath import fsGetWindowsPath;
from .fs0GetDOSPath import fs0GetDOSPath;

