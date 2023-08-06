"""Script for commenting in/out lines in file."""
import logging
from optparse import OptionParser

from .commenter import Commenter

__version__ = '0.1.1'

log = logging.getLogger(__name__)

def main(reverse=False):
    """Script for commenting in/out lines in file."""
    def line_callback(option, opt, value, parser):
        if '-' in value:
            lin = [int(i) for i in value.split('-')]
            assert(len(lin) == 2)
            lin[1] += 1
            lines = [i for i in range(*lin)]
        else:
            lines = [int(n) for n in value.split(',')] if value else None
        parser.values.lines = lines

    usage = """usage: %prog [options] <path>

Examples:
       %prog -h                  --->  see help
       %prog -cl1,2 path/to/file  --->  comment out lines 1 and 2
       %prog -ul3-6 path/to/file  --->  uncomment lines 3 to 6 (inclusive)
       %prog -ac path/to/file     --->  comment out all file

       %prog --start-pattern='\s+operations\s?=\s?\[' --end-pattern='\s+\]' path/to/file
         --->  comment out everything inside the `operations` list:

         1| class Migration(...):
         2|
         3|     operations = [
         4| #       migrations(
         5| #           ...
         6| #       ),
         7|     ]
"""
    description = """  Comment or uncomment lines in a file. Default
behavior: do the oposite i.e. if a line is commented - uncomment it, and vice versa.
To make sure that the matched lines will be [un]commented out - run with -[u]c option.
If you don't specify an --output, the original file (<path>) will be overwritten.
"""
    parser = OptionParser(usage=usage, description=description)
    parser.add_option("-c", "--comment", action="store_true", dest="comment",
                      default=False, help="comment lines [default: False]")
    parser.add_option("-u", "--uncomment", action="store_true", dest="uncomment",
                      default=False, help="uncomment lines [default: False]")
    parser.add_option("-a", "--all", action="store_true",
                      dest="all_lines", default=False,
                      help="apply to all lines in file; suppresses -l option [default: False]")
    parser.add_option("-l", "--lines", action="callback", type="string",
                      dest="lines", default=None, callback=line_callback,
                      help="comma separeted string of line numbers [default: None]")
    parser.add_option("-s", "--start-pattern", action="store", type="string",
                      dest="in_pattern", default=None,
                      help="pattern to match against the line before commented section [default: None]")
    parser.add_option("-e", "--end-pattern", action="store", type="string",
                      dest="out_pattern", default=None,
                      help="pattern to match against the first line after commented section [default: None]")
    parser.add_option("-o", "--output", action="store", type="string",
                      dest="output", default=None,
                      help="specify a path to output file [default: None]")
    parser.add_option("--symbol", action="store", type="string",
                      dest="comment_symbol", default='#',
                      help="specify a string to use as comment [default: '#']")

    options, args = parser.parse_args()

    if len(args) != 1:
        parser.error("specify a path to file")
    if options.comment and options.uncomment:
        parser.error('cannot run with both -c and -u set to True')
    if not (options.in_pattern or options.out_pattern or options.lines or options.all_lines):
        parser.error('specify patterns or lines; see --help')
    if not (options.comment or options.uncomment):
        reverse = True
    try:
        commenter = Commenter(path=args[0], reverse=reverse, **options.__dict__)
        commenter.comment_file()
    except Exception as e:
        parser.error(e)
