import os;
import mFileSystem2;

def fTestFileFunctions():
  sTempFolderPath = os.environ["TEMP"];
  oTempFolder = mFileSystem2.foGetFolder(sTempFolderPath);
  sTestFilePath = os.path.join(sTempFolderPath, "mFileSystem2 test file");

  # Test file
  oTestFile = oTempFolder.foConstructChildFile("mFileSystem2 test file");
  if oTestFile.fbExists():
    oTestFile.fDelete();
  assert not mFileSystem2.fbIsFile(sTestFilePath), \
    "File %s should not exist" % sTestFilePath;
  assert mFileSystem2.fo0GetFile(sTestFilePath) is None, \
    "File %s should not exist" % sTestFilePath;
  try:
    mFileSystem2.foGetFile(sTestFilePath);
  except AssertionError:
    pass;
  else:
    raise AssertionError("File %s should not exist" % sTestFilePath);

  oTestFile.fCreate();
  assert mFileSystem2.fbIsFile(sTestFilePath), \
    "File %s should exist" % sTestFilePath;
  assert mFileSystem2.fo0GetFile(sTestFilePath) is not None, \
    "File %s should exist" % sTestFilePath;

  mFileSystem2.foGetFile(sTestFilePath);
  mFileSystem2.foGetOrCreateFile(sTestFilePath);

  sExpectedContent = "test"
  oTestFile.fWrite(sExpectedContent);
  sContent = oTestFile.fsRead();
  assert sContent == sExpectedContent, \
      "Cannot read file %s: %s instead of %s" % (sTestFilePath, repr(sContent), repr(sExpectedContent));

  oTestFile.fClose();
  oTestFile.fDelete();

  mFileSystem2.foGetOrCreateFile(sTestFilePath);
  assert mFileSystem2.fbIsFile(sTestFilePath), \
    "File %s should exist" % sTestFilePath;
  oTestFile.fDelete();
  mFileSystem2.foCreateFile(sTestFilePath);
  assert mFileSystem2.fbIsFile(sTestFilePath), \
    "File %s should exist" % sTestFilePath;
  oTestFile.fDelete();
