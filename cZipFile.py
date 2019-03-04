import re, zipfile;

from .cFileSystemFile import cFileSystemFile;
from .iFolder import iFolder;

class cZipFile(cFileSystemFile, iFolder):
  bIsZipFileRoot = True;
  def __init__(oSelf, sPath, oParentFolder = None):
    cFileSystemFile.__init__(oSelf, sPath, oParentFolder);
    iFolder.__init__(oSelf);
    
    oSelf.__oPyZipFile = None;
    oSelf.__bWritable = False;
  
  def __del__(oSelf):
    try:
      oSelf.__oPyZipFile.close();
    except Exception:
      pass;
    cFileSystemFile.__del__(oSelf);
  
  def fbIsZipFile(oSelf):
    try:
      oSelf.__fOpen();
    except zipfile.BadZipFile, oException:
      return False;
    return True;
  
  def fCreate(oSelf):
    if oSelf.__oPyZipFile:
      oSelf.__oPyZipFile.close();
    if oSelf.fbIsFile():
      oSelf.fWrite("");
    elif not oSelf.oParentFolder.fbIsFolder():
      oSelf.oParentFolder.fCreate();
    oSelf.__oPyZipFile = zipfile.ZipFile(oSelf.sWindowsPath, "w", zipfile.ZIP_DEFLATED);
    oSelf.__bWritable = True;
    oSelf.fRemoveChildren();
  
  def __fOpen(oSelf, bWritable = False):
    if oSelf.__oPyZipFile:
      # File is already open
      if not bWritable or oSelf.__bWritable:
        # File is already open with correct access rights.
        return;
      # File is already open for read, but we need write access, so close and reopen
      oSelf.__oPyZipFile.close();
    oSelf.__oPyZipFile = zipfile.ZipFile(oSelf.sWindowsPath, "w" if bWritable else "r", zipfile.ZIP_DEFLATED);
    oSelf.__bWritable = bWritable;
  
  def foConstructChildFile(oSelf, sName):
    return cZipFileFile(sName, oSelf);
  
  def foConstructChildFolder(oSelf, sName):
    return cZipFileFolder(sName, oSelf);
  
  def fRefresh(oSelf):
    oSelf.__fOpen();
    for sFilePath in oSelf.__oPyZipFile.namelist():
      oSelf.foAddDescendantFile(sFilePath);
  
  def fsReadFile(oSelf, sFilePath):
    oSelf.__fOpen();
    oSelf.__oPyZipFile.read(sFilePath);
  
  def foWriteFile(oSelf, sFilePath, sFileContent):
    assert not oSelf.fo0GetDescendantFolder(sFilePath), \
        "Cannot write to file %s in zip; a folder with that name already exists in %s" % \
        (sFilePath, oSelf.sPath);
    oSelf.__fOpen(True);
    oSelf.__oPyZipFile.writestr(sFilePath, sFileContent);
    return oSelf.foGetOrAddDescendantFile(sFilePath);
  
  def fClose(oSelf):
    if oSelf.__oPyZipFile:
      oSelf.__oPyZipFile.close();
      oSelf.__oPyZipFile = None;
    cFileSystemFile.fClose(oSelf);

  def foAsZipFile(oSelf):
    raise NotImplemented();

from .cZipFileFolder import cZipFileFolder;
from .cZipFileFile import cZipFileFile;
