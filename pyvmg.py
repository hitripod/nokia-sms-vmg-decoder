import re
import glob
import csv
import datetime

def escapexml(xmldata):
    xmldata = xmldata.replace('&', '&amp;')
    xmldata = xmldata.replace('<', '&lt;')
    xmldata = xmldata.replace('>', '&gt;')
    xmldata = xmldata.replace('"', '&quot;')
    return xmldata

class VMGReader:
    """Reader for a .vmg file to get back the telephone number, date, body"""
    def __init__(self):
        """Initialize with the required regexes"""
        self.telre = re.compile(r'TEL:(\+?\d+)')
        self.datere = re.compile(r'X-NOK-DT:([\dTZ]+)')
        self.bodyre = re.compile(r'BEGIN:VBODY\s*Date:[\d.: ]+\s*(.*)\s*END:VBODY', re.DOTALL)

    def read(self, filename):
        """Open a .vmg file and remove the NULL characters and store the text message"""
        self.filename = filename
        with open(filename, 'rb') as file:
            raw_data = file.read()

        # Decode using UTF-16 (similar to Encoding.Unicode in C#)
        self.message = raw_data.decode('utf-16').strip()

    def process(self):
        """Parse the message and return back a dictionary with telephone number, date and body of message"""
        data = {}
        telmatch = self.telre.search(self.message)
        if telmatch:
            data['telno'] = telmatch.group(1)
        else:
            data['telno'] = ''
        datematch = self.datere.search(self.message)
        if datematch:
            data['date'] = datematch.group(1)
            try:
                data['date'] = datetime.datetime.strptime(data['date'], '%Y%m%dT%H%M%SZ')
            except ValueError:
                print(f"Invalid date format in file {self.filename}, setting date to epoch")
                # Use Epoch as date if no date was available
                data['date'] = datetime.datetime.strptime('1970-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
        else:
            print(f"No date found in file {self.filename}, setting date to epoch")
            # Use Epoch as date if no date was available
            data['date'] = datetime.datetime.strptime('1970-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')

        bodymatch = self.bodyre.search(self.message)
        if bodymatch:
            data['body'] = escapexml(bodymatch.group(1))
        else:
            data['body'] = ''

        return data

class Writer:
    """Base class for a writer object to convert all VMG files to a single file"""
    def __init__(self, filename):
        """Create a file writer object with the filename specified"""
        self.filename = filename
        self.file = open(filename, 'w', encoding='utf-8')

    def processdir(self, dirpath):
        """Given a directory path, process all the .vmg files in it and store as a list"""
        files = glob.glob(f'{dirpath}/*.vmg')
        reader = VMGReader()
        self.messages = []
        for f in files:
            print(f"Processing file: {f}")
            reader.read(f)
            message_data = reader.process()
            print(f"Extracted data: {message_data}")
            self.messages.append(message_data)
        self.messages.sort(key=lambda msg: msg['date'])

class XMLWriter(Writer):
    """Writer object for XML file as output"""
    def write(self):
        """Read every message in the list and write to a XML file"""
        self.file.write('<messages>')
        tmpl = "<message><tel>{}</tel><date>{}</date><body>{}</body></message>"
        for msg in self.messages:
            xmlstr = tmpl.format(msg['telno'], msg['date'].strftime('%Y-%m-%d %H:%M:%S'), msg['body'])
            self.file.write(xmlstr)
        self.file.write('</messages>')
        self.file.close()

class CSVWriter(Writer):
    """Writer object for CSV file as output"""
    def write(self):
        """Read every message in the list and write to a CSV file"""
        csvwriter = csv.writer(self.file)
        outputlist = [('telno', 'date', 'body')]
        for msg in self.messages:
            outputlist.append((msg['telno'], msg['date'].strftime('%Y-%m-%d %H:%M:%S'), msg['body']))
        csvwriter.writerows(outputlist)
        self.file.close()

class TextWriter(Writer):
    """Writer object for text file as output

    Format is
    +919900123456 - 2008-05-26 12:42:32
    Message contents goes here

    +919900123456 - 2008-05-26 12:50:32
    Second message contents goes here

    Ignores empty messages
    """
    def write(self):
        """Read every message in the list and write to a text file"""
        tmpl = "{} - {}\n{}\n\n"
        for msg in self.messages:
            if msg['telno'] == '':
                continue
            txtstr = tmpl.format(msg['telno'], msg['date'].strftime('%Y-%m-%d %H:%M:%S'), msg['body'])
            self.file.write(txtstr)
        self.file.close()
