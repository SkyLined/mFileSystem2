import os;
import mFileSystem2;

def fTestZipFileFunctions():
  sTempFolderPath = os.environ["TEMP"];
  oTempFolder = mFileSystem2.foGetFolder(sTempFolderPath);
  sTestZipFilePath = os.path.join(sTempFolderPath, "mFileSystem2 test file.zip");

  # Test file
  oTestZipFile = oTempFolder.foConstructChildFile("mFileSystem2 test file.zip");
  if oTestZipFile.fbExists():
    oTestZipFile.fDelete();
  assert not mFileSystem2.fbIsFile(sTestZipFilePath), \
    "File %s should not exist" % sTestZipFilePath;
  assert mFileSystem2.fo0GetFile(sTestZipFilePath) is None, \
    "File %s should not exist" % sTestZipFilePath;
  try:
    mFileSystem2.foGetZipFile(sTestZipFilePath);
  except AssertionError:
    pass;
  else:
    raise AssertionError("File %s should not exist" % sTestZipFilePath);
  
  oTestZipFile.fCreate();
  assert mFileSystem2.fbIsZipFile(sTestZipFilePath), \
    "File %s should exist" % sTestZipFilePath;
  assert mFileSystem2.fo0GetZipFile(sTestZipFilePath) is not None, \
    "File %s should exist" % sTestZipFilePath;
  
  mFileSystem2.foGetZipFile(sTestZipFilePath);
  mFileSystem2.foGetOrCreateZipFile(sTestZipFilePath);

  sExpectedContent = "test"
  oTestZippedFile = oTestZipFile.foWriteFile("mFileSystem2 test zipped file", sExpectedContent);
  
  sContent = oTestZippedFile.fsRead();
  assert sContent == sExpectedContent, \
      "Cannot read file %s: %s instead of %s" % (oTestZippedFile, repr(sContent), repr(sExpectedContent));
  sContent = oTestZipFile.fsReadFile("mFileSystem2 test zipped file");
  assert sContent == sExpectedContent, \
      "Cannot read file %s: %s instead of %s" % (oTestZippedFile, repr(sContent), repr(sExpectedContent));
  
  oTestZipFile.fClose();
  oTestZipFile.fDelete();
  
  mFileSystem2.foGetOrCreateZipFile(sTestZipFilePath);
  assert mFileSystem2.fbIsZipFile(sTestZipFilePath), \
    "File %s should exist" % sTestZipFilePath;
  oTestZipFile.fDelete();
  mFileSystem2.foCreateZipFile(sTestZipFilePath);
  assert mFileSystem2.fbIsZipFile(sTestZipFilePath), \
    "File %s should exist" % sTestZipFilePath;
  oTestZipFile.fDelete();
