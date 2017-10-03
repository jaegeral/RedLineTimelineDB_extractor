#!/usr/bin/env python3
'''
author: Alexander Jaeger
email:
'''

import argparse
import sys
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
    try:
        import sqlite3
        conn = sqlite3.connect(f)
        c = conn.cursor()

        dataCopy = c.execute("select count(*) from TimelineItems LEFT JOIN ItemSummaries ON TimelineItems.ItemSummaryID = ItemSummaries.ID LIMIT 10")
        values = dataCopy.fetchone()
        logger.info("Number of rows: %s",values[0])
        conn.commit()
        limit = values[0]

        csvfilename = f+".csv"

        with open(csvfilename, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['EventTimestamp', 'EventType', 'AuditType', 'Summary1', 'Summary2',  'Summary3', 'UniqueUsername'])

            loopcount = limit
            i = 1
            step = 10000

            #loopcount = 500 #for testing you can limit the amount of entries to be processed
            while i < loopcount:
                logger.info("Processing %s-%s / %s",i,i+step,loopcount)
                for row in c.execute(
                        'Select EventTimestamp, EventType, AuditType, Summary1, Summary2,  Summary3, UniqueUsername from TimelineItems LEFT JOIN ItemSummaries ON TimelineItems.ItemSummaryID = ItemSummaries.ID LIMIT ? , ?',(i,step)):
                    # TODO check if it is possible to implement:  ORDER BY EventTimestamp DESC but that appear to take a lot of CPU power

                    new = row[0].replace('Z', '') #remove Z for Zulu time for further processing
                    tpl = (new,) + row[1:]
                    #logger.info(tpl) #print out the current line
                    spamwriter.writerow(tpl)


                i += step

            logger.info("Finished processing")

        conn.close()
    except:
        e = sys.exc_info()[0]
        print("<p>Error: %s</p>" % e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    inputg = parser.add_mutually_exclusive_group(required=True)

    inputg.add_argument("-f", "--file", help="The DB file to convert")
    #TODO
    #parser.add_argument('-o', '--outfile', help="The file to output to. Default is stdout.", default="stdout")
    parser.add_argument("-v", "--verbose", help="More output", default=False, action="store_true")

    args = parser.parse_args()

    logger.setLevel(logging.DEBUG if args.verbose else logging.INFO)

    logger.info("Redline Timeline DB <-> CSV Converter")

    if (args.file):

        logger.info("Converting file at %s", args.file)

        try:
            with open(args.file, "r") as f:
                logger.debug("will do something")
                read_sql(args.file)
        except:
            logger.error("Could not open {}".format(args.file))
            sys.exit()
