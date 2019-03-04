import os, sys;
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."));

import mFileSystem2;

from fTestFileFunctions import fTestFileFunctions;
from fTestFolderFunctions import fTestFolderFunctions;
from fTestZipFileFunctions import fTestZipFileFunctions;

sTempFolderPath = os.environ["TEMP"];
assert mFileSystem2.fbIsFolder(sTempFolderPath), \
    "Cannot find %s" % sTempFolderPath;

fTestFileFunctions();
fTestFolderFunctions();
fTestZipFileFunctions();
