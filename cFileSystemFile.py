import os;

from .iFileSystemChild import iFileSystemChild;

class cFileSystemFile(iFileSystemChild):
  def __init__(oSelf, sPath, oParentFolder = None):
    iFileSystemChild.__init__(oSelf, sPath, oParentFolder);
    
    uDotIndex = oSelf.sName.rfind(".");
    oSelf.sExtension = None if uDotIndex == -1 else oSelf.sName[uDotIndex + 1:];
    
    oSelf.__oFile = None;
    oSelf.__bWritable = False;
  
  def __del__(oSelf):
    try:
      oSelf.__oFile.close();
    except Exception:
      pass;
  
  def fCreate(oSelf):
    if not oSelf.oParentFolder.fbIsFolder():
      oSelf.oParentFolder.fCreate();
    oSelf.fWrite("");
    
  def __fOpen(oSelf, bWritable = False):
    if oSelf.__oFile:
      # File is already open
      if not bWritable or oSelf.__bWritable:
        # File is already open with correct access rights.
        return;
      # File is already open for read, but we need write access, so close and reopen
      oSelf.__oFile.close();
    oSelf.__oFile = open(oSelf.sWindowsPath, "wb" if bWritable else "rb");
    oSelf.__bWritable = bWritable;
  
  def fsRead(oSelf):
    oSelf.__fOpen();
    return oSelf.__oFile.read();
  
  def fWrite(oSelf, sContent):
    oSelf.__fOpen(True);
    oSelf.__oFile.write(sContent);
  
  def fClose(oSelf):
    if oSelf.__oFile:
      oSelf.__oFile.close();
      oSelf.__oFile = None;
  
  def foAsZipFile(oSelf):
    return cZipFile(oSelf.sPath, oSelf.oParentFolder);
  
  def fDelete(oSelf):
    if not oSelf.fbIsFile():
      return;
    os.remove(oSelf.sWindowsPath);

from .cZipFile import cZipFile;
