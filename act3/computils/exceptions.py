

class CompileException(Exception):
    def __init__(self, parser, msg):
        self.parser = parser
        self.msg = msg;

    def get_msg(self):
        return f"lineno {self.parser.num_line}: {self.msg}"