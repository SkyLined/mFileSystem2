import os, re;

class iChild(object):
  def __init__(oSelf, sPath, oParentFolder):
    try:
      sPath = str(sPath, encoding = "ascii");
    except:
      pass;
    asPath = [s for s in re.split(r"\\|/", sPath) if s];
    oSelf.sName = asPath.pop();
    if oParentFolder:
      assert len(asPath) == 0, \
          "Cannot provide a path %s and a parent folder %s" % (repr(sPath), oParentFolder);
      oSelf.oParentFolder = oParentFolder;
    elif len(asPath) == 0:
      oSelf.oParentFolder = None;
    else:
      sParentFolderPath = os.path.sep.join(asPath);
      oSelf.fSetParentFolderForPath(sParentFolderPath);
    
    oSelf.oRoot = oSelf if oSelf.oParentFolder is None else oSelf.oParentFolder.oRoot;
    
  @property
  def sPath(oSelf):
    if not oSelf.oParentFolder:
      return oSelf.sName;
    return oSelf.oParentFolder.sPath + os.sep + oSelf.sName;
  
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