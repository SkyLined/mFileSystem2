import os;
import mFileSystem2;

def fTestFolderFunctions():
  sTempFolderPath = os.environ["TEMP"];
  oTempFolder = mFileSystem2.foGetFolder(sTempFolderPath);
  sTestFolderPath = os.path.join(sTempFolderPath, "mFileSystem2 test folder");
  oTestFolder = oTempFolder.foConstructChildFolder("mFileSystem2 test folder");
  if oTestFolder.fbExists():
    oTestFolder.fDelete();
  assert not mFileSystem2.fbIsFolder(sTestFolderPath), \
    "Folder %s should not exist" % sTestFolderPath;
  assert mFileSystem2.fo0GetFolder(sTestFolderPath) is None, \
    "Folder %s should not exist" % sTestFolderPath;
  try:
    mFileSystem2.foGetFolder(sTestFolderPath);
  except AssertionError:
    pass;
  else:
    raise AssertionError("Folder %s should not exist" % sTestFolderPath);

  oTestFolder.fCreate();
  assert mFileSystem2.fbIsFolder(sTestFolderPath), \
    "Folder %s should exist" % sTestFolderPath;
  assert mFileSystem2.fo0GetFolder(sTestFolderPath) is not None, \
    "Folder %s should exist" % sTestFolderPath;

  mFileSystem2.foGetFolder(sTestFolderPath);
  mFileSystem2.foGetOrCreateFolder(sTestFolderPath);

  oTestFolder.fDelete();

  mFileSystem2.foGetOrCreateFolder(sTestFolderPath);
  assert mFileSystem2.fbIsFolder(sTestFolderPath), \
    "Folder %s should exist" % sTestFolderPath;
  oTestFolder.fDelete();
  mFileSystem2.foCreateFolder(sTestFolderPath);
  assert mFileSystem2.fbIsFolder(sTestFolderPath), \
    "Folder %s should exist" % sTestFolderPath;
  oTestFolder.fDelete();
