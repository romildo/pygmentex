#! /usr/bin/env python2
# -*- coding: utf-8 -*-

"""
    PygmenTeX
    ~~~~~~~~~

    PygmenTeX is a converter that do syntax highlighting of snippets of
    source code extracted from a LaTeX file.

    :copyright: Copyright 2014 by José Romildo Malaquias
    :license: BSD, see LICENSE for details
"""

__version__ = '0.7'
__docformat__ = 'restructuredtext'

import sys
import getopt
import re
from os.path import splitext

from pygments import highlight, format
from pygments.styles import get_style_by_name
from pygments.lexers import get_lexer_by_name
from pygments.formatters.latex import LatexEmbeddedLexer, LatexFormatter
from pygments.util import get_bool_opt, get_int_opt


GENERIC_DEFINITIONS_1 = r'''% -*- mode: latex -*-

\makeatletter

\newdimen\LineNumberWidth
'''

GENERIC_DEFINITIONS_2 = r'''
\makeatother
'''


INLINE_SNIPPET_TEMPLATE = r'''
\expandafter\def\csname pygmented@snippet@%(number)s\endcsname{%%
  \pygmented@snippet@inlined{%%
%(body)s%%
}}
'''

DISPLAY_SNIPPET_TEMPLATE = r'''
\expandafter\def\csname pygmented@snippet@%(number)s\endcsname{%%
  \begin{pygmented@snippet@framed}%%
%(body)s%%
  \end{pygmented@snippet@framed}%%
}
'''

DISPLAY_LINENOS_SNIPPET_TEMPLATE = r'''
\expandafter\def\csname pygmented@snippet@%(number)s\endcsname{%%
  \begingroup
    \def\pygmented@alllinenos{(%(linenumbers)s)}%%
    \begin{pygmented@snippet@framed}%%
%(body)s%%
    \end{pygmented@snippet@framed}%%
  \endgroup
}
'''


def pyg(outfile, n, opts, extra_opts, text, usedstyles, inline_delim = ''):
    try:
        lexer = get_lexer_by_name(opts['lang'])
    except ClassNotFound as err:
        sys.stderr.write('Error: ')
        sys.stderr.write(str(err))
        return ""

    # global _fmter
    _fmter = LatexFormatter()

    escapeinside = opts.get('escapeinside', '')
    if len(escapeinside) == 2:
        left = escapeinside[0]
        right = escapeinside[1]
        _fmter.escapeinside = escapeinside
        _fmter.left = left
        _fmter.right = right
        lexer = LatexEmbeddedLexer(left, right, lexer)

    gobble = abs(get_int_opt(opts, 'gobble', 0))
    if gobble:
        lexer.add_filter('gobble', n=gobble)

    tabsize = abs(get_int_opt(opts, 'tabsize', 0))
    if tabsize:
        lexer.tabsize = tabsize

    encoding = opts['encoding']
    if encoding == 'guess':
        try:
            import chardet
        except ImportError:
            try:
                text = text.decode('utf-8')
                if text.startswith(u'\ufeff'):
                    text = text[len(u'\ufeff'):]
                    encoding = 'utf-8'
            except UnicodeDecodeError:
                text = text.decode('latin1')
                encoding = 'latin1'
        else:
            encoding = chardet.detect(text)['encoding']
            text = text.decode(encoding)
    else:
        text = text.decode(encoding)

    lexer.encoding = ''
    _fmter.encoding = encoding

    stylename = opts['sty']

    _fmter.style = get_style_by_name(stylename)
    _fmter._create_stylesheet()

    _fmter.texcomments = get_bool_opt(opts, 'texcomments', False)
    _fmter.mathescape = get_bool_opt(opts, 'mathescape', False)

    if stylename not in usedstyles:
        styledefs = _fmter.get_style_defs() \
            .replace('#', '##') \
            .replace(r'\##', r'\#') \
            .replace(r'\makeatletter', '') \
            .replace(r'\makeatother', '') \
            .replace('\n', '%\n')
        outfile.write(
            '\\def\\PYstyle{0}{{%\n{1}%\n}}%\n'.format(stylename, styledefs))
        usedstyles.append(stylename)

    x = highlight(text, lexer, _fmter)

    m = re.match(r'\\begin\{Verbatim}(.*)\n([\s\S]*?)\n\\end\{Verbatim}(\s*)\Z',
                 x)
    if m:
        linenos = get_bool_opt(opts, 'linenos', False)
        linenostart = abs(get_int_opt(opts, 'linenostart', 1))
        linenostep = abs(get_int_opt(opts, 'linenostep', 1))
        lines0 = m.group(2).split('\n')
        numbers = []
        lines = []
        counter = linenostart
        for line in lines0:
            line = re.sub(r'^ ', r'\\makebox[0pt]{\\phantom{Xy}} ', line)
            line = re.sub(r' ', '~', line)
            if linenos:
                if (counter - linenostart) % linenostep == 0:
                    line = r'\pygmented@lineno@do{' + str(counter) + '}' + line
                    numbers.append(str(counter))
                counter = counter + 1
            lines.append(line)
        if inline_delim:
            outfile.write(INLINE_SNIPPET_TEMPLATE %
                dict(number    = n,
                     style     = stylename,
                     options   = extra_opts,
                     body      = '\\newline\n'.join(lines)))
        else:
            if linenos:
                template = DISPLAY_LINENOS_SNIPPET_TEMPLATE
            else:
                template = DISPLAY_SNIPPET_TEMPLATE
            outfile.write(template %
                dict(number      = n,
                     style       = stylename,
                     options     = extra_opts,
                     linenosep   = opts['linenosep'],
                     linenumbers = ','.join(numbers),
                     body        = '\\newline\n'.join(lines)))



def parse_opts(basedic, opts):
    dic = basedic.copy()
    for opt in re.split(r'\s*,\s*', opts):
        x = re.split(r'\s*=\s*', opt)
        if len(x) == 2 and x[0] and x[1]:
            dic[x[0]] = x[1]
        elif len(x) == 1 and x[0]:
            dic[x[0]] = True
    return dic



_re_display = re.compile(
    r'^<@@pygmented@display@(\d+)\n(.*)\n([\s\S]*?)\n>@@pygmented@display@\1$',
    re.MULTILINE)

_re_inline = re.compile(
    r'^<@@pygmented@inline@(\d+)\n(.*)\n([\s\S]*?)\n>@@pygmented@inline@\1$',
    re.MULTILINE)

_re_input = re.compile(
    r'^<@@pygmented@input@(\d+)\n(.*)\n([\s\S]*?)\n>@@pygmented@input@\1$',
    re.MULTILINE)

def convert(code, outfile):
    """
    Convert ``code``
    """
    outfile.write(GENERIC_DEFINITIONS_1)

    opts = { 'lang'      : 'c',
             'sty'       : 'default',
             'linenosep' : '0pt',
             'tabsize'   : '8',
             'encoding'  : 'guess',
           }

    usedstyles = [ ]
    styledefs = ''

    pos = 0

    while pos < len(code):
        if code[pos].isspace():
            pos = pos + 1
            continue

        m = _re_inline.match(code, pos)
        if m:
            pyg(outfile,
                m.group(1),
                parse_opts(opts.copy(), m.group(2)),
                '',
                m.group(3),
                usedstyles,
                True)
            pos = m.end()
            continue

        m = _re_display.match(code, pos)
        if m:
            pyg(outfile,
                m.group(1),
                parse_opts(opts.copy(), m.group(2)),
                '',
                m.group(3),
                usedstyles)
            pos = m.end()
            continue

        m = _re_input.match(code, pos)
        if m:
            try:
                filecontents = open(m.group(3), 'rb').read()
            except Exception as err:
                sys.stderr.write('Error: cannot read input file: ')
                sys.stderr.write(str(err))
            else:
                pyg(outfile,
                    m.group(1),
                    parse_opts(opts, m.group(2)),
                    "",
                    filecontents,
                    usedstyles)
            pos = m.end()
            continue

        sys.stderr.write('Error: invalid input file contents: ignoring')
        break

    outfile.write(GENERIC_DEFINITIONS_2)



USAGE = """\
Usage: %s [-o <output file name>] <input file name>
       %s -h | -V

The input file should consist of a sequence of source code snippets, as
produced by the `pygmentex` LaTeX package. Each code snippet is
highlighted using Pygments, and a LaTeX command that expands to the
highlighted code snippet is written to the output file.

It also writes to the output file a set of LaTeX macro definitions the
Pygments styles that are used in the code snippets.

If no output file name is given, use `<input file name>.pygmented`.

The -e option enables escaping to LaTex. Text delimited by the <left>
and <right> characters is read as LaTeX code and typeset accordingly. It
has no effect in string literals. It has no effect in comments if
`texcomments` or `mathescape` is set.

The -h option prints this help.

The -V option prints the package version.
"""


def main(args = sys.argv):
    """
    Main command line entry point.
    """
    usage = USAGE % ((args[0],) * 2)

    try:
        popts, args = getopt.getopt(args[1:], 'e:o:hV')
    except getopt.GetoptError as err:
        sys.stderr.write(usage)
        return 2
    opts = {}
    for opt, arg in popts:
        opts[opt] = arg

    if not opts and not args:
        print(usage)
        return 0

    if opts.pop('-h', None) is not None:
        print(usage)
        return 0

    if opts.pop('-V', None) is not None:
        print('PygmenTeX version %s, (c) 2010 by José Romildo.' % __version__)
        return 0
 
    if len(args) != 1:
        sys.stderr.write(usage)
        return 2
    infn = args[0]
    try:
        code = open(infn, 'rb').read()
    except Exception as err:
        sys.stderr.write('Error: cannot read input file: ')
        sys.stderr.write(str(err))
        return 1

    outfn = opts.pop('-o', None)
    if not outfn:
        root, ext = splitext(infn)
        outfn = root + '.pygmented'
    try:
        outfile = open(outfn, 'w')
    except Exception as err:
        sys.stderr.write('Error: cannot open output file: ')
        sys.stderr.write(str(err))
        return 1

    convert(code, outfile)

    return 0


if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv))
    except KeyboardInterrupt:
        sys.exit(1)
