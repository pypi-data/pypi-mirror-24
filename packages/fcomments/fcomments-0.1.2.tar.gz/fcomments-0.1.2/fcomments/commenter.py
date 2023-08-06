import re


class Commenter:
    """Comment or uncomment lines in file."""

    def __init__(self, **kwargs):
        self.result = ''
        self.path = None
        self.output = None
        self.all_lines = False
        self.uncomment = False
        self.comment = False
        self.reverse = False
        self.in_pattern = None
        self.out_pattern = None
        self.lines = None
        self.comment_symbol = '#'

        for key in kwargs:
            setattr(self, key, kwargs[key])
        with open(self.path, "r") as f:
            self.original = [l for l in f]
        self._update_reverse()
        if self.all_lines:
            self.lines = [i for i in range(len(self.original) + 1)]

    def comment_file(self, commit=True, **kwargs):
        all_lines = kwargs.get('all_lines', None)
        original = kwargs.get('original', self.original)
        if all_lines:
            lines = [i for i in range(len(original) + 1)]
            kwargs.update({'lines': lines})

        # self._check(**kwargs)
        if kwargs.get('lines', None):
            self.line_based(**kwargs)
        else:
            # raise NotImplementedError('pattern based: {}'.format(kwargs))
            self.pattern_based(**kwargs)
        if commit:
            self.save_file()

    def _update_reverse(self):
        if not (self.comment or self.uncomment):
            self.reverse = True

    # @staticmethod
    # def _check(self, **kwargs):
        # if self.comment and self.uncomment:
        #     raise RuntimeError('both -cu')
        # if not (self.in_pattern or
        #         self.out_pattern or
        #         self.lines or
        #         self.all_lines):
        #     print('no pattern specified')
        #     raise RuntimeError('no pattern specified')

    @staticmethod
    def _get_updates():
        return {'output': None, 'comment_symbol': '#', 'lines': None,
                'comment': False, 'all_lines': False, 'uncomment': False,
                'in_pattern': None, 'out_pattern': None, 'reverse': True}

    def handle_line(self, line, comment, reverse=True):
        is_comment = re.match('\s*' + self.comment_symbol, line) is not None
        if reverse:
            comment = False if is_comment else True
        elif not (comment or is_comment):
            return line

        if comment:
            if is_comment:
                print('Warning: line already commented')
                return line
            else:
                return self.comment_symbol + line
        else:
            assert is_comment
            return line[1:]

    def line_based(self, lines=None, original=None,
                   comment=False, reverse=True, update=False, **kwargs):
        res_file = []
        if not original:
            original = self.original
        assert lines
        for i, line in enumerate(original):
            if i + 1 in lines:
                line = self.handle_line(line, comment, reverse)
            res_file.append(line)
        # print('line based:', ''.join(res_file))
        self.result = ''.join(res_file)
        if update:
            pass

    def pattern_based(self, in_pattern=None, out_pattern=None, original=None,
                      comment=False, reverse=True, update=False, **kwargs):
        start_pattern = False
        end_pattern = False
        res_file = []
        if not original:
            original = self.original
        for line in original:
            if start_pattern and re.match(out_pattern, line):
                end_pattern = True
                start_pattern = False
            if start_pattern:
                line = self.handle_line(line, comment, reverse)
            res_file.append(line)
            if end_pattern:
                continue
            if re.match(in_pattern, line):
                start_pattern = True

        self.result = ''.join(res_file)

    def save_file(self):
        path = self.output if self.output else self.path
        with open(path, "w") as f:
            f.write(self.result)
        with open(self.path, "r") as f:
            self.original = [l for l in f]
        self.result = ''
