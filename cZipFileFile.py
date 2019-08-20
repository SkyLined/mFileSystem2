from .iZipFileChild import iZipFileChild;

class cZipFileFile(iZipFileChild):
  def fbIsFolder(oSelf):
    return False;
  
  def fbIsFile(oSelf):
    return True;

  def fsRead(oSelf):
    return oSelf.oZipFileRoot.fsReadFile(oSelf.sZipFilePath);

  def fWrite(oSelf, sFileContent):
    return oSelf.oZipFileRoot.foWriteFile(oSelf.sZipFilePath, sFileContent);
  
  def fClose(oSelf):
    return; # NOP