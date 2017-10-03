#!/usr/bin/env python3
'''
author: Alexander Jaeger
email:
'''

import argparse
import time
import sys
import os
import logging
import csv

# create logger with 'rltldb'
logger = logging.getLogger('rltldb_application')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('converter.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


def read_sql(f):
    # this method reads the file
    # Query:
    # Select EventTimestamp, EventType, AuditType, Summary1, Summary2,  Summary3, UniqueUsername from TimelineItems LEFT JOIN ItemSummaries ON TimelineItems.ItemSummaryID = ItemSummaries.ID LIMIT 10
    import sqlite3
    conn = sqlite3.connect(f)
    c = conn.cursor()

    dataCopy = c.execute("select count(*) from TimelineItems")
    values = dataCopy.fetchone()
    logger.info("Number of rows: %s",values[0])

    with open('output.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(['ID','EventTimestamp', 'EventType', 'AuditType', 'Summary1', 'Summary2','Summary3', 'UniqueUsernameColumn 1', 'Column 2'])
        for row in c.execute('SELECT * FROM TimelineItems ORDER BY ItemSummaryID'):
            print row
        #    writer.writerows(row)

        # this will be used to extract it to CSV


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    inputg = parser.add_mutually_exclusive_group(required=True)

    inputg.add_argument("-f", "--file", help="The DB file to convert")
    parser.add_argument('-o', '--outfile', help="The file to output to. Default is stdout.", default="stdout")
    parser.add_argument("-v", "--verbose", help="More output", default=False, action="store_true")
    parser.add_argument("-l", "--logfile", help="Where to send the log to", default="converter.log")

    args = parser.parse_args()

    logger.setLevel(logging.DEBUG if args.verbose else logging.INFO)

    logger.info("Redline Timeline DB <-> CSV Converter")

    if (args.file):

        logger.debug("Converting file at %s", args.file)

        # This is just a file conversion
        # Relatively quick and easy
        # Create a non-connected misp instance
        try:
            with open(args.file, "r") as f:
                #jsondata = f.read()
                logger.debug("will do something")
                read_sql(args.file)
        except:
            print("Could not open {}".format(args.file))
            sys.exit()
