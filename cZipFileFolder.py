import re;

from .iZipFileChild import iZipFileChild;
from .iFolder import iFolder;

class cZipFileFolder(iZipFileChild, iFolder):
  def __init__(oSelf, sName, oParentFolder = None):
    iZipFileChild.__init__(oSelf, sName, oParentFolder);
    iFolder.__init__(oSelf);

  def fReadChildren(oSelf):
    # children are created once when the zip file is opened, so fReadChildren is not required.
    return;
  
  def fRefresh(oSelf):
    # This makes little sense.
    raise NotImplemented();

  def foConstructChildFile(oSelf, sName):
    return cZipFileFile(sName, oSelf);
  
  def foConstructChildFolder(oSelf, sName):
    return cZipFileFolder(sName, oSelf);
  
from .cZipFileFile import cZipFileFile;