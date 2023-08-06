```bash
Usage: commenter.py [options] <path>

Examples:
       commenter.py -h                  --->  see help
       commenter.py -cl1,2 path/to/file  --->  comment out lines 1 and 2
       commenter.py -ul3-6 path/to/file  --->  uncomment lines 3 to 6
       commenter.py -ac path/to/file     --->  comment out all file

       commenter.py --start-pattern='\s+operations\s?=\s?\[' --end-pattern='\s+\]' path/to/file
         --->  comment out everything inside the `operations` list:

         1| class Migration(...):
         2|
         3|     operations = [
         4| #       migrations(
         5| #           ...
         6| #       ),
         7|     ]


  Comment or uncomment lines in a file. Default behavior: do the oposite i.e.
if a line is commented - uncomment it, and vice versa. To make sure that the
matched lines will be [un]commented out - run with -[u]c option. If you don't
specify an --output, the original file (<path>) will be overwritten.

Options:
  -h, --help            show this help message and exit
  -c, --comment         comment lines [default: False]
  -u, --uncomment       uncomment lines [default: False]
  -a, --all             apply to all lines in file; suppresses -l option
                        [default: False]
  -l LINES, --lines=LINES
                        comma separeted string of line numbers [default: None]
  -s IN_PATTERN, --start-pattern=IN_PATTERN
                        pattern to match against the line before commented
                        section [default: None]
  -e OUT_PATTERN, --end-pattern=OUT_PATTERN
                        pattern to match against the first line after
                        commented section [default: None]
  -o OUTPUT, --output=OUTPUT
                        specify a path to output file [default: None]
  --symbol=COMMENT_SYMBOL
                        specify a string to use as comment [default: '#']
```
