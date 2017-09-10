import code
import platform
import sys

from tornado import tcpserver
from tornado_console.compat import StringIO


__all__ = [
    'ConsoleServer',
]


class TornadoConsole(code.InteractiveConsole):
    def __init__(self, stream, locals, banner):
        code.InteractiveConsole.__init__(self, locals)

        self.stream = stream
        self.banner = banner

        self.ps1 = getattr(sys, 'ps1', '>>> ')
        self.ps2 = getattr(sys, 'ps2', '... ')

        self.write(self.get_banner())
        self.write(self.ps1)
        self.start()

    def start(self):
        self.stream.read_until('\n', self.process_line)

    def get_banner(self):
        if self.banner:
            return self.banner

        return '%s %s on %s (%s)\n' % (
            platform.python_implementation(),
            sys.version,
            platform.platform(),
            self.__class__.__name__
        )

    def process_line(self, line):
        line = line.rstrip('\n')

        self.push(line)
        self.stream.read_until('\n', self.process_line)

    def push(self, line):
        try:
            more = code.InteractiveConsole.push(self, line)
        except KeyboardInterrupt:
            self.write('\nKeyboardInterrupt\n')
            self.resetbuffer()

            more = False

        if more:
            self.write(self.ps2)
        else:
            self.write(self.ps1)

    def runcode(self, code_obj):
        fake_stdout = StringIO()

        sys.stdout = fake_stdout
        sys.stderr = fake_stdout

        try:
            code.InteractiveConsole.runcode(self, code_obj)
        finally:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

            self.write(fake_stdout.getvalue())

    def write(self, data):
        if not isinstance(data, bytes):
            data = data.encode('utf-8')

        self.stream.write(data)


class ConsoleServer(tcpserver.TCPServer):
    def __init__(self, locals, banner=None, **kwargs):
        super(ConsoleServer, self).__init__(**kwargs)

        self.locals = locals or {}
        self.banner = banner

        self.connections = []

    def get_locals(self):
        _locals = {
            '__doc__': None,
            '__name__': '__console__',
        }

        _locals.update(self.locals)

        return _locals

    def handle_stream(self, stream, address):
        console = TornadoConsole(stream, self.get_locals(), self.banner)

        # this is just to ensure that we maintain a reference to the stream
        # so it doesn't get reaped.
        stream.set_close_callback(lambda: self.connection_closed(console))

        self.connections.append(console)

    def connection_closed(self, connection):
        self.connections.remove(connection)
