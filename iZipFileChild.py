import os;

from .iChild import iChild;

class iZipFileChild(iChild):
  bIsZipFileRoot = False;
  def __init__(oSelf, sName, oParentFolder):
    iChild.__init__(oSelf, sName, oParentFolder);
    
    oSelf.oZipFileRoot = oSelf.oParentFolder if oSelf.oParentFolder.bIsZipFileRoot else oSelf.oParentFolder.oZipFileRoot;
    oSelf.__sZipFilePath = None;
    oSelf.__sWindowsPath = None;
  
  def fSetParentFolder(oSelf, oParentFolder):
    raise NotImplemented();
  
  def fbExists(oSelf):
    return True;
  
  def fbIsFolder(oSelf):
    raise NotImplemented();
  
  def fbIsFile(oSelf):
    raise NotImplemented();
  
  @property
  # http://msdn.microsoft.com/en-us/library/aa365247.aspx
  def sZipFilePath(oSelf):
    if oSelf.__sZipFilePath is None:
      oSelf.__sZipFilePath = oSelf.fsGetRelativePath(oSelf.oZipFileRoot.sPath);
    return oSelf.__sZipFilePath;
  
  @property
  # http://msdn.microsoft.com/en-us/library/aa365247.aspx
  def sWindowsPath(oSelf):
    if oSelf.__sWindowsPath is None:
      oSelf.__sWindowsPath = oSelf.oZipFileRoot.sWindowsPath + os.sep + oSelf.sZipFilePath;
    return oSelf.__sWindowsPath;
  
  @property
  def s0DosPath(oSelf):
    raise NotImplemented();
