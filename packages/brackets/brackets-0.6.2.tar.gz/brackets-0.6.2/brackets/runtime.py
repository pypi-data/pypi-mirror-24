import sys
import regex as re
from brackets.helpers import eval

class BracketsTemplateCreator(object):
    """
    def {
        print({0} + {1});
        print({keyword});
    }
    """
    def __init__(self, callable, args):
        self.callable = callable
        self.args     = args

    def format(self, *args, **kwargs):
        format = {}
        for index, arg in enumerate(args):
            format['__{0}__'.format(index)] = arg
        format.update(kwargs)
        format = {f:format[f] for f in self.args}
        return BracketsTemplate(self.callable, format)

class BracketsTemplate(object):
    def __init__(self, callable, format):
        self.callable = callable
        self.format   = format

    def __call__(self):
        return self.callable(**self.format)

class RegexSubLiteral(object):
    def __init__(self, matcher, repl):
        self.matcher = matcher
        self.repl    = repl

    def sub(self, string):
        return self.matcher.sub(self.repl, string)

def FormatStringLiteral(string, globals, locals):
    matcher = re.compile('\{.*?\}')
    match   = matcher.search(string)
    while match:
        start, end = match.span()
        code = string[start:end]
        val  = eval(code[1:-1], globals, locals)
        string = string[:start] + str(val) + string[end:]
        match   = matcher.search(string)
    return string

def ConditionalFunctionCall(function, *args, **kwargs):
    if callable(function):
        return function(*args, **kwargs)
    return function
