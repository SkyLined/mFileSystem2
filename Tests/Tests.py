from fTestDependencies import fTestDependencies;
fTestDependencies();

try:
  import mDebugOutput;
except:
  mDebugOutput = None;
try:
  try:
    from oConsole import oConsole;
  except:
    import sys, threading;
    oConsoleLock = threading.Lock();
    class oConsole(object):
      @staticmethod
      def fOutput(*txArguments, **dxArguments):
        sOutput = "";
        for x in txArguments:
          if isinstance(x, (str, unicode)):
            sOutput += x;
        sPadding = dxArguments.get("sPadding");
        if sPadding:
          sOutput.ljust(120, sPadding);
        oConsoleLock.acquire();
        print sOutput;
        sys.stdout.flush();
        oConsoleLock.release();
      fPrint = fOutput;
      @staticmethod
      def fStatus(*txArguments, **dxArguments):
        pass;
  
  import os;
  
  import mFileSystem2;
  from fTestFileFunctions import fTestFileFunctions;
  from fTestFolderFunctions import fTestFolderFunctions;
  from fTestZipFileFunctions import fTestZipFileFunctions;
  
  sTempFolderPath = os.environ["TEMP"];
  assert mFileSystem2.fbIsFolder(sTempFolderPath), \
      "Cannot find %s" % sTempFolderPath;
  
  print "* Running tests...";
  fTestFileFunctions();
  fTestFolderFunctions();
  fTestZipFileFunctions();
  print "+ Done.";
  
except Exception as oException:
  if mDebugOutput:
    mDebugOutput.fTerminateWithException(oException, bShowStacksForAllThread = True);
  raise;
