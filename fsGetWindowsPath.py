import os;

from fsGetNormalizedPath import fsGetNormalizedPath;

def fsGetWindowsPath(sPath):
  sNormalizedPath = fsGetNormalizedPath(sPath);
  if not sNormalizedPath.startswith(r"\\"):
    sDrive, sPath = os.path.splitdrive(sPath);
    if not sDrive:
      # No drive provided: use global CWD
      sDrive, sCWDPath = os.path.splitdrive(os.getcwdu());
    else:
      # Drive provided: use CWD for the specified drive
      sCWDPath = os.path.abspath(sDrive)[2:];
    if sPath[0] != u"\\":
      # Path is relative to CWD path
      sPath = os.path.join(sCWDPath, sPath);
    return u"\\\\?\\" + sDrive + os.path.normpath(sPath);
  return u"\\\\?\\UNC\\" + os.path.normpath(sPath[2:]);
