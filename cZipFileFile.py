from .iZipFileChild import iZipFileChild;

class cZipFileFile(iZipFileChild):
  def fbIsFolder(oSelf):
    return False;
  
  def fbIsFile(oSelf):
    return True;

  def fsRead(oSelf):
    oSelf.oZipFileRoot.fsReadFile(oSelf.sZipFilePath);

  def fWrite(oSelf, sFileContent):
    oSelf.oZipFileRoot.foWriteFile(oSelf.sZipFilePath, sFileContent);
      