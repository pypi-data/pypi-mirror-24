from __future__ import unicode_literals

from collections import Counter
import getpass
import re
import sys

import clip
import six

from .writers import BUILTIN_WRITERS, write
from .parser import MessageHtmlParser
from .time import AmbiguousTimeZoneError, UnexpectedTimeFormatError
from .utils import (set_stream_color, set_all_color, green, bright, cyan, error,
                    reset_terminal_styling)
from .name_resolver import FacebookNameResolver

# Python 3 is supposed to be smart enough to not ever default to the 'ascii'
# encoder, but apparently on Windows that may not be the case.
if six.PY3:

    import io
    # Change the output streams to binary.
    sys.stderr = sys.stderr.detach()
    sys.stdout = sys.stdout.detach()

    # Wrap them in a safe UTF-8 encoders. PDB doesn't like it when
    # the streams are wrapped in StreamWriter.
    sys.stdout = io.TextIOWrapper(sys.stdout, encoding='UTF-8',
                                  errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr, encoding='UTF-8',
                                  errors='replace')

else:

    from encodings.utf_8 import StreamWriter
    # Wrap the raw Python 2 output streams in smart UTF-8 encoders.
    # Python 2 doesn't like it when the raw file handles are wrapped in
    # TextIOWrapper.
    sys.stderr = StreamWriter(sys.stderr)
    sys.stdout = StreamWriter(sys.stdout)

app = clip.App()


@app.main(description='A program for converting Facebook chat history to a '
                      'number of more usable formats')
@clip.opt('-f', '--format', default='text',
          help='Format to convert to (%s)' %
               ', '.join(BUILTIN_WRITERS + ('stats',)))
@clip.opt('-t', '--thread', default=None,
          help='Only include threads involving exactly the following '
               'comma-separated participants in output '
               '(-t \'Billy,Steve Jensson\')')
@clip.opt('-z', '--timezones',
          help='Timezone disambiguators (TZ=OFFSET,[TZ=OFFSET[...]])')
@clip.opt('-d', '--directory', default=None,
          help='Write all output as a file per thread into a directory '
               '(subdirectory will be created)')
@clip.flag('-u', '--utc', help='Use UTC timestamps in the output')
@clip.flag('-n', '--nocolor', help='Do not colorize output')
@clip.flag('-p', '--noprogress', help='Do not show progress output')
@clip.flag('-r', '--resolve',
           help='[BETA] Resolve profile IDs to names by connecting to Facebook')
@clip.arg('path', required=True,
          help='Path of the messages.htm file to parse')
def fbcap(path, thread, format, nocolor, timezones, utc, noprogress, resolve, directory):

    # Make stderr colorized unless explicitly disabled.
    set_stream_color(sys.stderr, disabled=nocolor or not sys.stderr.isatty())
    set_stream_color(sys.stdout, disabled=nocolor or not sys.stdout.isatty())

    if format not in BUILTIN_WRITERS + ('stats',):
        error("\"%s\" is not a valid output format.\n" % format)
        sys.exit(1)

    timezone_hints = {}
    if timezones:
        try:
            for tz in timezones.split(','):
                name, offset_raw = tz.split('=')
                # Solely for validating the timezone early on.
                neg = -1 if offset_raw[0] == '-' else 1
                offset = (neg * int(offset_raw[1:3]),
                          neg * int(offset_raw[3:]))
                timezone_hints[name] = offset
        except Exception:
            error("Invalid timezone string: %s\n" % timezones)
            sys.exit(1)

    # Filter duplicate spaces in thread filters.
    if thread:
        thread = re.sub("\s+", " ", thread)
        thread = tuple(friend.strip() for friend in thread.split(","))

    # Collect Facebook credentials if we should resolve profile IDs
    # via Facebook.
    name_resolver = None
    if resolve:
        sys.stderr.write("Facebook username/email: ")
        sys.stderr.flush()
        email = six.moves.input()
        # The Windows implementation of getpass.getpass(...) is stupid and
        # ignores the `stream` argument for unknown reasons. Let's manually
        # handle the password prompt to stderr in this case, which should
        # work on all operating systems.
        sys.stderr.write("Facebook password: ")
        sys.stderr.flush()
        password = getpass.getpass("")
        name_resolver = FacebookNameResolver(email, password)
        # Clear the content of the previous line.
        sys.stderr.write("\033[1A\r%s\r" % (" " * len("Facebook password: ")))
        # Clear the line before that as well.
        sys.stderr.write("\r\033[1A")
        sys.stderr.write(
            "%s\r" % (" " * (len("Facebook username/email: ") + len(email)))
        )
        sys.stderr.flush()
    exit_code = 0
    try:
        parser = MessageHtmlParser(path=path, filter=thread,
                                   timezone_hints=timezone_hints,
                                   progress_output=not noprogress,
                                   use_utc=utc, name_resolver=name_resolver)
        fbch = parser.parse()
        if format == 'stats':
            generate_stats(fbch, sys.stdout)
        else:
            if directory:
                set_all_color(enabled=False)
            write(format, fbch, directory or sys.stdout)

    except AmbiguousTimeZoneError as atze:
        error("\nAmbiguous timezone offset found [%s]. Please re-run the "
              "parser with the -z TZ=OFFSET[,TZ=OFFSET2[,...]] flag."
              "(e.g. -z PST=-0800,PDT=-0700). Your options are as "
              "follows:\n" % atze.tz_name)
        for k, v in atze.tz_options.items():
            regions = ', '.join(list(v)[:3])
            error(" -> [%s] for regions like %s\n" % (k[-1], regions))
        exit_code = 1
    except UnexpectedTimeFormatError as utfe:
        error("\nUnexpected time format in \"%s\". If you downloaded your "
              "Facebook data in a language other than English, then it's "
              "possible support may need to be added to this tool.\n\n"
              "Please report this as a bug on the associated GitHub page "
              "and it will be fixed promptly.\n"
              % utfe.time_string)
        exit_code = 1
    except KeyboardInterrupt:
        error("\nInterrupted prematurely by keyboard\n")
        exit_code = 1
    finally:
        reset_terminal_styling()
    sys.exit(exit_code)


# TODO: Convert this into a writer implementation.
def generate_stats(fbch, stream):

    text_string = '---------------' + \
                  ('-' * len(fbch.user)) + '--' + '\n'
    stream.write(bright(text_string))
    stream.write(bright(' Statistics for %s\n' % fbch.user))
    stream.write(bright(text_string))
    stream.write('\n')

    threads = tuple(fbch.threads[k] for k in fbch.threads.keys())
    stream.write('Top 10 longest threads:\n\n')
    ordered_threads = sorted(threads, key=lambda t: len(t))
    ordered_threads.reverse()
    for i, t in enumerate(ordered_threads[0:10], 1):
        stream.write("  " + cyan('[' + str(i) + '] ') +
                     bright(", ".join(t.participants) +
                     cyan(" (" + str(len(t.messages)) + ")" + "\n")))
        p_count = Counter()
        for m in t.messages:
            p_count[m.sender] += 1
        total = sum(p_count.values())
        for s, c in p_count.most_common():
            stream.write("      - " + s +
                         green(" [%d|%.2f%%]\n" % (c, (c * 100) / total)))
        stream.write('\n')


def main():
    try:
        app.run()
    except clip.ClipExit:
        pass

if __name__ == '__main__':
    main()
