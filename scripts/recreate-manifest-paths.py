#!/usr/bin/env python3
##
## Filename:    recreate-manifest-paths.py
##
## Author:      Phazor/Cascade 1733
##
## Created:     2024-03-31
##
## Modified:    None.
##

import sqlite3
import shutil
import os
import argparse
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

##====================================
## 
## Parse arguments from commandline
##
##====================================
def parseArguments():

    parser = argparse.ArgumentParser(description='recreate-manifest-paths.py - recreate filesystem from device backup',
                                     usage='recreate-manifest-paths.py [-h] [OPTIONS]',
                                     epilog='Epilog: thanks for using my program!')
    ##
    ## ARGUMENTS
    ##

    # manifest
    parser.add_argument('-m', '--manifest', dest='manifest', action="store", type=str, metavar="FILENAME", default="Manifest.db",
                        help='path to Manifest.db [Default: %(default)s]')  
    # source
    parser.add_argument('-s', '--source', dest='source', action="store", type=str, metavar="SOURCE", default=False,
                        help='sourch path with device backup [Default: %(default)s]')  
    # target
    parser.add_argument('-t', '--target', dest='target', action="store", type=str, metavar="TARGET", default=False,
                        help='target path where to recreate manifest paths [Default: %(default)s]')  
    # verbose
    parser.add_argument('-v','--verbose', dest='verbose', action="store_true", default=False,
                        help='verbose mode [Default: %(default)s]')
    
    ##
    ## PARSE ARGUMENTS
    ##

    options = parser.parse_args()

    ##
    ## Set Verbose if Debug
    ##
    if options.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Setting level to debug")
    ##
    ## Error Check
    ##

    if not options.source:
        logging.error("no source is set: --source")
        exit(0)

    if not options.target:
        logging.error("no target is set: --target")
        exit(0)

    options.source=options.source.rstrip('/')
    options.target=options.target.rstrip('/')

    if not os.path.exists(options.source):
        logging.error("path %s does'nt exist" % options.source)
        exit(0)

    if not os.path.exists(options.target):
        logging.error("path %s does'nt exist" % options.target)
        exit(0)
    
    if not os.path.exists(options.manifest):
        options.manifest=options.source+"/"+options.manifest
        if not os.path.exists(options.manifest):
            logging.error("path %s does'nt exist" % options.manifest)
            exit(0)

    return options

##=================================
## 
## Yield paths from Manifest.db
##
##=================================
def yieldPaths(db):
    for row in con.execute("SELECT fileID, domain, relativePath, flags from Files"):
        yield row
    return None

##================================
## 
## Main
##
##================================
if __name__ == "__main__":
    options = parseArguments()

    ##
    ## Connect to Manifest.db
    ##
    logging.info("connecting to sqlite database: %s" % options.manifest)
    try:
        con = sqlite3.connect(options.manifest)
        cur = con.cursor()
    except Exception as error:
        logging.error("%" % error)
        exit(0)

    ##
    ## Loop through paths from Manifest.db
    ##
    FILES=0
    logging.info("parsing information from database")
    for fid, domain, path, flags in yieldPaths(cur):
        fileExists=False
        if len(fid)==40:
            prefix=fid[0:2]
            SOURCE=options.source+"/"+prefix+"/"+fid
            if os.path.exists(SOURCE)==False: continue
            logging.debug("fid: %s dest: %s dir: %s flags: %s" % (fid,domain, path, flags))
            TARGET=options.target+"/"+domain+"/"+path
            TARGETDIR=os.path.dirname(TARGET)
            if os.path.exists(TARGETDIR):
                logging.debug("directory exists: %s" % TARGETDIR)
            else:
                logging.debug("creating directory: %s" % TARGETDIR)
                os.makedirs(TARGETDIR)
            logging.debug("creating file: %s" % TARGET)
            shutil.copy(SOURCE, TARGET)
            FILES+=1
    ##
    ## Close connection to database
    ##
    con.close()
    ##
    ## DONE
    ##
    logging.info("recreated %s files at %s" % (FILES, options.target))
##
## EOF
##
