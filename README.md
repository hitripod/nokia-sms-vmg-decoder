# VMG SMS Decoder

## Introduction

VMG is a file format used by Nokia phones to store SMS messages. These files often contain important text messages that users may want to retrieve and convert into more accessible formats. The VMG files store SMS messages using the UTF-16 encoding format.

This script is designed to decode VMG files and extract the stored SMS messages, converting them into XML, CSV, and plain text formats.

## Inspiration

This project was inspired by the work of [cnu](https://github.com/cnu/pyvmg), whose initial implementation provided the foundation for this script.

## Requirements

This script requires Python 3.9.4 and the following Python packages:

- `re`
- `glob`
- `csv`
- `datetime`

## Usage

To use this script, place your VMG files in the same directory as the script and run the `main.py` file. The script will process all VMG files in the directory and convert them to XML, CSV, and plain text formats.

### Example

Run the following command to convert all VMG files in the current directory:

```bash
python main.py
```

This will generate the following output files:
- `output.xml`
- `output.csv`
- `output.txt`

## Compatibility

This script has been successfully tested with Traditional Chinese SMS backups from Nokia 2006 models.

## Acknowledgments

Special thanks to [cnu](https://github.com/cnu/pyvmg) for the inspiration and initial implementation of the VMG parsing logic.
