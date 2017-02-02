# chat_export.py
A python script to export Facebook Messenger and iMessage data into a CSV with only names and timestamps.

## Usage

`python chat_export.py [-f <facebook root> -n <facebook name>] [-m] -o <outputfile>`

#### Options

- `-f`: Optional. Specify the location of the root of the Facebook data folder.
- `-n`: Required if you want to include Facebook data in the export. Your name as it appears on Facebook.
- `-m`: Optional. Use if you want to include iMessage data in your export (Mac only).
- `-o`: The location of the output file. Preferably a csv file.