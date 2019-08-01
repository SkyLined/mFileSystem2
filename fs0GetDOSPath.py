from fsGetWindowsPath import fsGetWindowsPath;

from mWindowsSDK import *;

def fs0GetDOSPath(sPath):
  oKernel32 = foLoadKernel32DLL();
  sWindowsPath = fsGetWindowsPath(sPath);
  if not os.path.exists(sWindowsPath):
    return None;
  opsWindowsPath = LPCWSTR(foCreateBuffer(sWindowsPath), bCast = True);
  odwRequiredBufferSizeInChars = oKernel32.GetShortPathNameW(
    opsWindowsPath,
    NULL,
    0
  );
  assert odwRequiredBufferSizeInChars.value != 0, \
        "GetShortPathNameW('...', NULL, 0) => Error 0x%08X" % oKernel32.GetLastError();
  oBuffer = foCreateBuffer(odwRequiredBufferSizeInChars.value);
  dwUsedBufferSizeInChars = oKernel32.GetShortPathNameW(
    opsWindowsPath,
    PWSTR(oBuffer, bCast = True),
    odwRequiredBufferSizeInChars
  );
  assert dwUsedBufferSizeInChars.value != 0, \
      "GetShortPathNameW('...', 0x%08X, 0x%X) => Error 0x%08X" % \
      (pBuffer, odwRequiredBufferSizeInChars.value, oKernel32.GetLastError());
  sDOSPath = fsGetBufferString(oBuffer);
  if sDOSPath.startswith("\\\\?\\"):
    sDOSPath = sDOSPath[len("\\\\?\\"):];
    if sDOSPath.startswith("UNC\\"):
      sDOSPath = "\\" + sDOSPath[len("UNC"):];
  return sDOSPath;
