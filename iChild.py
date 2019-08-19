import os, re;
from .fsGetNormalizedPath import fsGetNormalizedPath;

class iChild(object):
  def __init__(oSelf, sPath, oParentFolder):
    oSelf.sPath = fsGetNormalizedPath(sPath, oParentFolder.sPath if oParentFolder else None);
    oSelf.sName = os.path.basename(oSelf.sPath);
    sParentFolderPath = fsGetNormalizedPath(oSelf.sPath + os.sep + u"..");
    if oParentFolder:
      assert sParentFolderPath == oParentFolder.sPath, \
          "Cannot create a child (path = %s, normalized = %s, parent = %s) for the given parent folder (path %s)" % \
          (repr(sPath), repr(oSelf.sPath), repr(sParentFolderPath), repr(oParentFolder.sPath));
      oSelf.oParentFolder = oParentFolder;
    elif sParentFolderPath == oSelf.sPath:
      oSelf.oParentFolder = None;
    else:
      oSelf.fSetParentFolderForPath(sParentFolderPath);
    oSelf.oRoot = oSelf if oSelf.oParentFolder is None else oSelf.oParentFolder.oRoot;
    
  def fsGetRelativePath(oSelf, sBase):
    return os.path.relpath(oSelf.sPath, sBase);
  
  def fbExists(oSelf):
    raise NotImplemented();
  
  def fbIsFolder(oSelf):
    raise NotImplemented();
  
  def fbIsFile(oSelf):
    raise NotImplemented();
  
  def __str__(oSelf):
    return "%s(%s)" % (oSelf.__class__.__name__, oSelf.sPath);