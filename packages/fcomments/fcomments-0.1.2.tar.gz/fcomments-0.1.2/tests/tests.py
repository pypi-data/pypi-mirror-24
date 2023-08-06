from unittest import TestCase
import os
# import subprocess

from fcomments.commenter import Commenter
from fcomments import create_parser

dir_path = os.path.dirname(os.path.abspath(__file__))
TEST_FILE_PATH = os.path.join(dir_path, 'ex_file.py')


def is_commented(line, comm_state=True, comment_symbol='#'):
    if line.startswith(comment_symbol):
        return comm_state
    else:
        return not comm_state


def file_check(lines, comm_state=True, path=TEST_FILE_PATH, strict=False):
    with open(path) as test_file:
        for i, line in enumerate(test_file):
            if i + 1 in lines:
                if not is_commented(line, comm_state):
                    return False
            elif strict:
                if is_commented(line, comm_state):
                    return False
    return True


class fCommentsTestCase(TestCase):

    def __init__(self, *args, **kwargs):
        super(fCommentsTestCase, self).__init__(*args, **kwargs)
        self.path = TEST_FILE_PATH
        self.def_dic = {'output': None, 'comment_symbol': '#', 'lines': None,
                        'comment': False, 'all_lines': False, 'uncomment': False,
                        'in_pattern': None, 'out_pattern': None}
        self.reverse = True
        self.cmnter = Commenter(path=self.path)

    def run_command(self, atrs, lines, assrt=True):
        newcm = Commenter(path=self.path)
        newcm.comment_file(**atrs)
        if assrt:
            self.assertTrue(file_check(lines=lines, path=newcm.path))
        else:
            self.assertFalse(file_check(lines=lines, path=newcm.path))

    def tearDown(self):
        atrs = {'uncomment': True, 'all_lines': True,
                'path': self.path, 'reverse': False}
        self.run_command(atrs, [3], assrt=False)
        atrs = {'comment': True, 'lines': [1],
                'path': self.path, 'reverse': False}
        self.run_command(atrs, [1], assrt=True)


class ScriptTest(fCommentsTestCase):

    def test_manual(self):
        # main()
        parser = create_parser()
        parser.parse_args('-l 1-5'.split())
        parser.parse_args('-l 1,2,5'.split())

        self.assertIsNotNone(parser)
        # subprocess.call(["python", "-m", "fcomments", TEST_FILE_PATH, "-l1"])

    def test_infile_usage(self):
        """Test usage with one Class instatiation and atribs manipulation."""
        lin = [*range(4, 11)]
        c = Commenter(path=TEST_FILE_PATH)
        c.comment_file(lines=lin, comment=True)
        self.assertTrue(file_check(lines=lin, comm_state=True))  # lines 4-11 are commented
        c.comment_file(lines=lin, uncomments=True)
        self.assertEqual(c.result, "")
        # lines 4-11 are still commented because original not updated
        self.assertFalse(file_check(lines=lin, comm_state=True))
        c.reverse = False
        c.comment_file(lines=[3, 4, 5])
        self.assertFalse(file_check(lines=lin, comm_state=True))  # nothing changed, -u

    def test_valid_usage(self):
        c = Commenter(path=TEST_FILE_PATH)
        c.comment_file(comment=True, lines=[4, 5, 6])
        self.assertTrue(file_check(lines=[4, 5, 6], comm_state=True))  # nothing changed, -u
        c.comment_file(uncomment=True, lines=[4, 5, 6])
        self.assertFalse(file_check(lines=[4, 5, 6], comm_state=True))
        self.assertTrue(file_check(lines=[4, 5, 6], comm_state=False))


class CommenterTests(fCommentsTestCase):

    def test_sanity(self):
        self.assertTrue(file_check(path=self.path, lines=[1]))
        self.assertFalse(file_check(path=self.path, lines=[1, 3, 4]))

    def test_handle_line(self):
        self.line_equal('    sth()', '#    sth()', True)
        self.line_equal('    sth()', '#    sth()', False)
        self.line_equal('#    sth()', '    sth()', False)
        self.line_equal('#    sth()', '    sth()', False)

        self.line_equal('    sth()', '    sth()', False, reverse=False)
        self.line_equal('    sth()', '#    sth()', True, reverse=False)
        self.line_equal('#    sth()', '#    sth()', True, reverse=False)

    def test_comment_file(self):

        # TODO
        self.cmnter.reverse = True
        self.cmnter.lines = [2, 4, 5]
        self.cmnter.comment_file(lines=[1, 2])
        # self.assertRaises(NotImplementedError, self.cmnter.comment_file)

    def test_old_comment_file(self):
        self.cmnter.lines = None

        self.cmnter.comment_file(in_pattern='\s+operations\s?=\s?\[', out_pattern='\s+\]')

        self.assertFalse(file_check(path=self.path, lines=[*range(13, 23)]))
        self.assertFalse(file_check(path=self.path, lines=[*range(13, 24)]))
        self.assertFalse(file_check(path=self.path, lines=[*range(15, 25)]))
        #
        self.assertTrue(file_check(path=self.path, lines=[*range(14, 23)]))
        self.assertTrue(file_check(path=self.path, lines=[*range(18, 20)]))

        atrs = {'lines': [1, 2, 4, 5], 'comment': True,
                'path': self.path, 'reverse': False}
        self.run_command(atrs, [1, 2, 4, 5])

    def test_pattern(self):
        pass

    def test_all_lines(self):
        atrs = {'all_lines': True, 'path': self.path,
                'reverse': False, 'comment': True}
        self.run_command(atrs, [13, 14, 7, 2, 21])
        atrs = {'all_lines': True, 'path': self.path,
                'reverse': False, 'uncomment': True}
        self.run_command(atrs, [])

    def line_equal(self, line_in, line_out, cmnt=False, reverse=True):
        line = self.cmnter.handle_line(line_in, cmnt, reverse)
        self.assertEqual(line, line_out)
