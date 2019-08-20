import os, re;

def ftsGetAncestorFolderNameAndRemainingPath(sPath):
  return re.match(r"^(?:(.+?)[\\\/])?(.+)$", sPath.strip("/").strip("\\")).groups();

class iFolder(object):
  cChildFolder = None;
  cChildFile = None;
  
  def __init__(oSelf):
    oSelf.__doChildFolder_by_sLowerName = {};
    oSelf.__doChildFile_by_sLowerName = {};
    oSelf.__bChildrenRead = False;
    
  def fbIsFolder(oSelf):
    return True;
  
  def fbIsFile(oSelf):
    return False;
  
  def fReadChildren(oSelf):
    if not oSelf.__bChildrenRead:
      oSelf.__bChildrenRead = True;
      oSelf.fRefresh();
  
  def fRefresh(oSelf):
    raise NotImplemented();
  
  def fUpdateChildFolderAndFileNames(oSelf, asFileNames, asFolderNames):
    oSelf.__doChildFolder_by_sLowerName = dict([
      (sName.lower(), oSelf.foConstructChildFolder(sName))
      for sName in asFolderNames
    ]);
    oSelf.__doChildFile_by_sLowerName = dict([
      (sName.lower(), oSelf.foConstructChildFile(sName))
      for sName in asFileNames
    ]);
  
  # foAddChild(File|Folder)
  def foAddChildFile(oSelf, sName):
    oChildFile = oSelf.foConstructChildFile(sName);
    sChildLowerName = oChildFile.sName.lower();
    assert sChildLowerName not in oSelf.__doChildFile_by_sLowerName, \
        "Cannot add two files with the same name %s" % repr(oChildFile.sName);
    assert sChildLowerName not in oSelf.__doChildFolder_by_sLowerName, \
        "Cannot add a file and a folder with the same name %s" % repr(oChildFile.sName);
    oSelf.__doChildFile_by_sLowerName[sChildLowerName] = oChildFile;
    return oChildFile;
  
  def foAddChildFolder(oSelf, sName):
    oChildFolder = oSelf.foConstructChildFolder(sName);
    sFolderLowerName = oChildFolder.sName.lower();
    assert sFolderLowerName not in oSelf.__doChildFolder_by_sLowerName, \
        "Cannot add two folders with the same name %s" % repr(oChildFolder.sName);
    assert sFolderLowerName not in oSelf.__doChildFile_by_sLowerName, \
        "Cannot add a folder and a file with the same name %s" % repr(oChildFolder.sName);
    oSelf.__doChildFolder_by_sLowerName[sFolderLowerName] = oChildFolder;
    return oChildFolder;
  
  # fRemoveChild(File|Folder)
  def fRemoveChildFile(oSelf, oChildFile):
    oSelf.fReadChildren();
    sChildLowerName = oChildFile.sName.lower();
    if sChildLowerName in oSelf.__doChildFile_by_sLowerName:
      del oSelf.__doChildFile_by_sLowerName[sChildLowerName];
  def fRemoveChildFolder(oSelf, oChildFolder):
    oSelf.fReadChildren();
    sFolderLowerName = oChildFolder.sName.lower();
    if oChildFolder.sName in oSelf.__doChildFolder_by_sLowerName:
      del oSelf.__doChildFolder_by_sLowerName[sFolderLowerName];
  def fRemoveChild(oSelf, oChild):
    oSelf.fReadChildren();
    oSelf.fRemoveChildFolder(oChild) and oSelf.fRemoveChildFile(oChild);

  def fRemoveChildren(oSelf):
    oSelf.__doChildFolder_by_sLowerName = {};
    oSelf.__doChildFile_by_sLowerName = {};
  
  # faoGetChild(File|Folder)s
  def faoGetChildFiles(oSelf):
    oSelf.fReadChildren();
    return [
      oSelf.__doChildFile_by_sLowerName[sLowerName]
      for sLowerName in sorted(oSelf.__doChildFile_by_sLowerName.keys())
    ];
  def faoGetChildFolders(oSelf):
    oSelf.fReadChildren();
    return [
      oSelf.__doChildFolder_by_sLowerName[sLowerName]
      for sLowerName in sorted(oSelf.__doChildFolder_by_sLowerName.keys())
    ];
  def faoGetChildren(oSelf):
    return oSelf.faoGetChildFolders() + oSelf.faoGetChildFiles();
  
  # faoGetDescendant(File|Folder)s
  def faoGetDescendantFiles(oSelf):
    aoDescendantFiles = oSelf.faoGetChildFiles();
    for oChildFolder in oSelf.faoGetChildFolders():
      aoDescendantFiles.extend(oChildFolder.faoGetDescendantFiles());
    return aoDescendantFiles;
  def faoGetDescendantFolders(oSelf):
    aoDescendantFolders = [];
    for oChildFolder in oSelf.faoGetChildFolders():
      aoDescendantFolders.append(oChildFolder);
      aoDescendantFolders.extend(oChildFolder.faoGetDescendantFolders());
    return aoDescendantFolders;
  def faoGetDescendants(oSelf):
    aoDescendants = [];
    for oChildFolder in oSelf.faoGetChildFolders():
      aoDescendants.append(oChildFolder);
      aoDescendants.extend(oChildFolder.faoGetDescendants());
    aoDescendants.extend(oSelf.faoGetChildFiles());
    return aoDescendants;
  
  # fo0GetChild(File|Folder)
  def fo0GetChildFile(oSelf, sName):
    oSelf.fReadChildren();
    return oSelf.__doChildFile_by_sLowerName.get(sName.lower());
  def fo0GetChildFolder(oSelf, sName):
    oSelf.fReadChildren();
    return oSelf.__doChildFolder_by_sLowerName.get(sName.lower());
  def fo0GetChild(oSelf, sName):
    return oSelf.fo0GetChildFile(sName) or oSelf.fo0GetChildFolder(sName);
  
  # fo0GetDescendant(File|Folder)
  def fo0GetDescendantFile(oSelf, sPath):
    sAncestorFolderName, sRemainingPath = ftsGetAncestorFolderNameAndRemainingPath(sPath);
    if sAncestorFolderName is None:
      return oSelf.fo0GetChildFile(sRemainingPath);
    oAncestorFolder = oSelf.fo0GetChildFolder(sAncestorFolderName);
    if oAncestorFolder is None:
      return None;
    return oAncestorFolder.fo0GetDescendantFile(sRemainingPath);
  def fo0GetDescendantFolder(oSelf, sPath):
    sAncestorFolderName, sRemainingPath = ftsGetAncestorFolderNameAndRemainingPath(sPath);
    if sAncestorFolderName is None:
      return oSelf.fo0GetChildFolder(sRemainingPath);
    oAncestorFolder = oSelf.fo0GetChildFolder(sAncestorFolderName);
    if oAncestorFolder is None:
      return None;
    return oAncestorFolder.fo0GetDescendantFolder(sRemainingPath);
  def fo0GetDescendant(oSelf, sPath):
    return oSelf.fo0GetDescendantFile(sPath) or oSelf.fo0GetDescendantFolder(sPath);
  
  # foGetChild(File|Folder)
  def foGetChildFile(oSelf, sName):
    oChildFile = oSelf.fo0GetChildFile(sName);
    assert oChildFile, \
        "Child file %s of %s not found" % (sName, oSelf.sPath);
    return oChildFile;
  def foGetChildFolder(oSelf, sName):
    oChildFolder = oSelf.fo0GetChildFolder(sName);
    assert oChildFolder, \
        "Child folder %s of %s not found" % (sName, oSelf.sPath);
    return oChildFolder;
  def foGetChild(oSelf, sName):
    oChild = oSelf.fo0GetChildFile(sName) or oSelf.fo0GetChildFolder(sName);
    assert oChild, \
        "Child file or folder %s of %s not found" % (sName, oSelf.sPath);
    return oChild;
  
  # foGetOrAddChild(File|Folder)
  def foGetOrAddChildFile(oSelf, sName):
    return oSelf.fo0GetChildFile(sName) or oSelf.foAddChildFile(sName);
  def foGetOrAddChildFolder(oSelf, sName):
    return oSelf.fo0GetChildFolder(sName) or oSelf.foAddChildFolder(sName);
  
  # fbHasChild(File|Folder)
  def fbHasChildFile(oSelf, sPath):
    return oSelf.fo0GetChildFile(sPath) is not None;
  def fbHasChildFolder(oSelf, sPath):
    return oSelf.fo0GetChildFolder(sPath) is not None;
  def fbHasChild(oSelf, sPath):
    return oSelf.fbHasChildFile(sPath) or oSelf.fbHasChildFolder(sPath);
  
  # fbHasDescendant(File|Folder)
  def fbHasDescendantFolder(oSelf, sPath):
    return oSelf.fo0GetDescendantFolder(sPath) is not None;
  def fbHasDescendantFile(oSelf, sPath):
    return oSelf.fo0GetDescendantFile(sPath) is not None;
  def fbHasDescendant(oSelf, sPath):
    return oSelf.fbHasDescendantFile(sPath) or oSelf.fbHasDescendantFolder(sPath);
  
  # foGetDescendant(File|Folder)
  def foGetDescendantFile(oSelf, sPath):
    oDescendantFile = oSelf.fo0GetDescendantFile(sPath);
    assert oDescendantFile, \
        "Descendant file %s of %s not found" % (sPath, oSelf);
    return oDescendantFile;
  def foGetDescendantFolder(oSelf, sPath):
    oDescendantFolder = oSelf.fo0GetDescendantFolder(sPath);
    assert oDescendantFolder, \
        "Descendant folder %s of %s not found" % (sPath, oSelf);
    return oDescendantFolder;
  def fo0GetDescendant(oSelf, sPath):
    oDescendant = oSelf.fo0GetDescendantFile(sPath) or oSelf.fo0GetDescendantFolder(sPath);
    assert oDescendant, \
        "Descendant file or folder %s of %s not found" % (sPath, oSelf);
    return oDescendant;
  
  # foAddDescendant(File|Folder)
  def foAddDescendantFile(oSelf, sPath):
    sAncestorFolderName, sRemainingPath = ftsGetAncestorFolderNameAndRemainingPath(sPath);
    if sAncestorFolderName is None:
      return oSelf.foAddChildFile(sRemainingPath);
    oAncestorFolder = oSelf.foGetOrAddChildFolder(sAncestorFolderName);
    return oAncestorFolder.foAddDescendantFile(sRemainingPath);
  def foAddDescendantFolder(oSelf, sPath):
    sAncestorFolderName, sRemainingPath = ftsGetAncestorFolderNameAndRemainingPath(sPath);
    if sAncestorFolderName is None:
      return oSelf.foAddChildFolder(sRemainingPath);
    oAncestorFolder = oSelf.foGetOrAddChildFolder(sAncestorFolderName);
    return oAncestorFolder.foAddDescendantFolder(sRemainingPath);
  
  # foGetOrAddDescendant(File|Folder)
  def foGetOrAddDescendantFolder(oSelf, sPath):
    return oSelf.fo0GetDescendantFolder(sPath) or oSelf.foAddDescendantFolder(sPath);
  def foGetOrAddDescendantFile(oSelf, sPath):
    return oSelf.fo0GetDescendantFile(sPath) or oSelf.foAddDescendantFile(sPath);
  
    