import os;

def fsGetWindowsPath(sPath):
  sPath = unicode(sPath);
  if sPath[:2] != u"\\\\": # Absolute or relative path to local drive
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
    return u"\\\\?\\" + sDrive + os.path.normpath(sPath).rstrip("\\");
  if sPath[2] != "?": # UNC path to remote drive "\\..." => "\\?\UNC\..."
    return u"\\\\?\\UNC\\" + os.path.normpath(sPath[2:]).rstrip("\\")
  # The provided path already is a Windows Path; normalize it:
  return u"\\\\?\\" + os.path.normpath(sPath[4:]).rstrip("\\");
