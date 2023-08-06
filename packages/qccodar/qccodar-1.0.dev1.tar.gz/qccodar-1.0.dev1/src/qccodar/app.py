"""Quality control CODAR (qccodar) RadialMetric data. 

Usage:
  qccodar (auto | catchup | manual) [options]
  qccodar --help | --version

Options:
  -d DIR --datadir DIR      Data directory to process [default: /Codar/SeaSonde/Data]
  -p PAT --pattern PAT      Pattern type [default: IdealPattern]
  -h --help                 Show this help message and exit
  --version                 Show version
  
"""

import os
import re
import glob

from pkg_resources import get_distribution

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .qcutils import do_qc, recursive_glob
from .codarutils import run_LLUVMerger

__version__ = get_distribution("qccodar").version

debug = 1

def manual(datadir, pattern):
    """ Manual mode runs qc and merge on all files in datadir """

    # get file listing of datadir
    fns = recursive_glob(os.path.join(datadir, 'RadialMetric', pattern), 'RDL*.ruv')

    # handle if no files to process
    if not fns:
        print "Warn: qccodar manual --datadir %s --pattern %s" % (datadir, pattern)
        print "No files RDL*.ruv found in %s" % fulldatadir
        return

    print 'qccodar (manual) -- qc step ...'
    
    # do qc for each file in the datadir --> output to RadialShorts_qcd
    for fullfn in fns:
        print '... input: %s' % fullfn
        fn = os.path.basename(fullfn)
        ofn = do_qc(datadir, fn, pattern)
        print '... output: %s' % ofn

    # get file list of RadialShorts
    # depending on system and desired time span for merge, change the target time for file search
    fns = recursive_glob(os.path.join(datadir, 'RadialShorts_qcd', pattern), 'RDL*00.ruv')

    print 'qccodar (manual) -- merge step: ...'

    # run LLUVMerger for each
    for fullfn in fns:
        print '... input: %s' % fullfn
        fn = os.path.basename(fullfn)
        ofn = run_LLUVMerger(datadir, fn, pattern)
        print '... output: %s' % ofn

def auto(datadir, pattern, fullfn):
    """ Auto mode runs qc and merge for each fullfn """

    numfiles = 3
    
    # get file listing of RadialMetric folder in datadir
    indir = os.path.join(datadir, 'RadialMetric', pattern)
    fns = recursive_glob(indir, 'RDL*.ruv')

    try:
        idx = fns.index(fullfn)
    except ValueError, e:
        idx = None

    if idx == None:
        print "qccodar (auto): Expecting RadialMetric file. "
        print "    File %s does not match 'RDL*.ruv'" % fullfn
        return
    
    if numfiles == 1 and len(fns)>=1:
        fullfn = fns[idx]
    elif numfiles == 3 and len(fns)>=2 and idx>=1:
        fullfn = fns[idx-1]
    elif numfiles == 5 and len(fns)>=3 and idx>=2:
        fullfn = fns[idx-2]
    else:
        print "... Nothing processed. Need more files to run qc"
        return

    try:
        print '... qc input: %s' % fullfn
        fn = os.path.basename(fullfn)
        rsdfn = do_qc(datadir, fn, pattern)
        print '... qc output: %s' % rsdfn
    except EOFError, e:
        print 'Encountered empty file in qc process ... wait for next file event to process'
        return

    # get file listing of RadialShorts_qcd folder in datadir
    indir = os.path.join(datadir, 'RadialShorts_qcd', pattern)
    fns = recursive_glob(indir, 'RDL*00.ruv')

    try:
        idx = fns.index(rsdfn)
    except ValueError, e:
        idx = None

    if idx != None:
        fullfn = fns[idx]
        print '... merge input: %s' % fullfn        
        fn = os.path.basename(fullfn)
        ofn = run_LLUVMerger(datadir, fn, pattern)
        print '... merge output: %s' % ofn

def catchup(datadir, pattern):
    """ Process any new RadialMetric files not processed yet in datadir """

    numfiles = 3

    if pattern=='IdealPattern':
        lluvtype = 'v'
    elif pattern=='MeasPattern':
        lluvtype = 'w'

    # find what is new in RadialMetric folder -- that does not have corresponding RadialShort
    fns = recursive_glob(os.path.join(datadir, 'RadialMetric', pattern), 'RDL*.ruv')
    fns = [os.path.basename(fn) for fn in fns]
    # print fns
    rsfns = recursive_glob(os.path.join(datadir, 'RadialShorts_qcd', pattern), 'RDL*.ruv')
    rsfns = [os.path.basename(fn) for fn in rsfns]
    # print rsfns
    # replace RDL[xy] in radialshort names to compare with radialmetric names
    for idx, fn in enumerate(rsfns):
        rsfns[idx] = re.sub(r'RDL[xy]', 'RDL'+lluvtype, fn)
    # print rsfns

    # use dict-list to identify what is new
    fns = dict([(fn,None) for fn in fns])
    rsfns = dict([(fn,None) for fn in rsfns])
    newfns = [fn for fn in fns if not fn in rsfns]
    newfns.sort()

    if numfiles == 3:
        newfns = newfns[1:]
    elif numfiles == 5:
        newfns = newfns[2:]
    print "Files to process ..." 
    print newfns

    for fn in newfns:
        fullfn = os.path.join(datadir, 'RadialMetric', pattern, fn)
        auto(datadir, pattern, fullfn)

# Watcher() and Handler() classes based on
# https://www.michaelcho.me/article/using-pythons-watchdog-to-monitor-changes-to-a-directory
# and http://ginstrom.com/scribbles/2012/05/10/continuous-integration-in-python-using-watchdog/
#
# Perform any actions, using any triggers that you choose.
#

class Watcher:
    """ Watch for changes in directory and trigger an event handler """

    def __init__(self):
        self.observer = Observer()
        print 'Starting thread %s ...' % self.observer.name

    def run(self, datadir, pattern):
        event_handler = Handler(datadir, pattern)
        fulldatadir = os.path.join(datadir, 'RadialMetric', pattern)
        self.observer.schedule(event_handler, fulldatadir, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
                # throw the expection in worker thread in this main thread if not handled yet
                if event_handler.exc_info:
                    raise event_handler.exc_info[1], None, event_handler.exc_info[2]
        except:
            raise
            self.observer.stop()
            print '... qccodar auto-mode stopped'

        self.observer.join()


class Handler(FileSystemEventHandler):
    """
    Specifically, handle doing qc and merge when a file is created in watched directory
    """

    def __init__(self, datadir, pattern):
        self.datadir = datadir
        self.pattern = pattern
        # attribute to add any expection
        self.exc_info = None

    def on_any_event(self, event):
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            print "File created - %s." % event.src_path
            try:
                catchup(self.datadir, self.pattern)
            except Exception, e:
                # catch and store exception thrown in this worker thread
                # e.g. IOError or KeyBoardInterrupt
                import sys
                self.exc_info = sys.exc_info()
        # elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            # print "File modified - %s." % event.src_path


def main():
    """Run qccodar from the command line."""
    from docopt import docopt

    arguments = docopt(__doc__, version="qccodar %s" % __version__)
    # print arguments

    datadir, pattern = arguments['--datadir'], arguments['--pattern']
    if arguments['manual']:
        runarg = 'manual'
    elif arguments['auto']:
        runarg = 'auto'
    else:
        runarg = ''

    indatadir = os.path.join(datadir, 'RadialMetric', pattern)
    if not os.path.isdir(indatadir):
        print "Error: qccodar %s --datadir %s --pattern %s" % (runarg, datadir, pattern)
        print "Directory does not exist: %s " % indatadir
        return

    outdir1 = os.path.join(datadir, 'RadialShorts_qcd', pattern)
    if not os.path.exists(outdir1):
        os.makedirs(outdir1)

    outdir2 = os.path.join(datadir, 'Radials_qcd', pattern)
    if not os.path.isdir(outdir2):
        os.makedirs(outdir2)
 
    # run modes (manual | catchup | auto)
    if arguments['manual']:
        # manual-mode 
        manual(datadir, pattern)
        return
    elif arguments['catchup']:
        # catchup once
        catchup(datadir, pattern)
        return
    elif arguments['auto']:
        # catchup and then create watchdog to monitor datadir
        catchup(datadir, pattern)
        w = Watcher()
        print 'Starting qccodar auto-mode (Press cntrl-C to exit)...'
        w.run(datadir, pattern)
        return

if __name__ == "__main__":
    main()
