from fsGetWindowsPath import fsGetWindowsPath;

from mWindowsAPI.mDLLs import KERNEL32;
from mWindowsAPI.mDefines import NULL;
from mWindowsAPI.mFunctions import WSTR;

def fs0GetDOSPath(sPath):
  sWindowsPath = fsGetWindowsPath(sPath);
  if not os.path.exists(sWindowsPath):
    return None;
  dwRequiredBufferSizeInChars = KERNEL32.GetShortPathNameW(sWindowsPath, NULL, 0);
  assert dwRequiredBufferSizeInChars.value != 0, \
        "GetShortPathNameW('...', NULL, 0) => Error 0x%08X" % KERNEL32.GetLastError();
  sBuffer = WSTR(dwRequiredBufferSizeInChars.value);
  dwUsedBufferSizeInChars = KERNEL32.GetShortPathNameW(sWindowsPath, sBuffer, dwRequiredBufferSizeInChars.value);
  assert dwUsedBufferSizeInChars.value != 0, \
      "GetShortPathNameW('...', 0x%08X, %d/0x%X) => Error 0x%08X" % \
      (pBuffer, dwRequiredBufferSizeInChars.value, dwRequiredBufferSizeInChars.value, KERNEL32.GetLastError());
  sDOSPath = str(sBuffer.value);
  if sDOSPath.startswith("\\\\?\\"):
    sDOSPath = sDOSPath[len("\\\\?\\"):];
    if sDOSPath.startswith("UNC\\"):
      sDOSPath = "\\" + sDOSPath[len("UNC"):];
  return sDOSPath;
