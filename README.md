# RedLineTimelineDB_extractor
Extracts the Timeline of a Redline parsed sqlite database so it can be used e.g. in an ELK stack.

## Redline

[Redline](https://www.fireeye.com/services/freeware/redline.html) is a tool developed by Mandiant / Fireeye to do live forensics / Incident response.

The RedLineTimelineDB_extractor is NOT made to replace Redline.

# Usage

* Process the Live response file in redline, to create a SQLlite out of the XML files.
* Locate the SQLite database file *e.g. SystemXYZ.mans*
* `python3 -f SystemXYZ.mans` 
* wait till the script finishes
* locate the SystemXYZ.mans.csv
* continue your analysis with the generated CSV file
* if you passed a **folder + filename** as an argument, the CSV will be created in the **same folder**

# Notes

## Timestamps

As Redline writes every timestamp with a Z for Zulu at the end of the timeline, but most tools cannot deal with it, it will be **removed in every line**.
Every timestamp is **UTC**.

## Performance

The script was tested on a regular notebook with a SQLite database **1,1 GB** with  1920738 enties in timetable and it took
around **3 minutes** to create the CSV file with a size of **485 MB**.

The amount of lines per CSV write can be adjusted, so finetuning is possible to rate IO of the SQLite against IO to write the CSV file.

