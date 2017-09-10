# tornado-console
Live Python interactive console within your Tornado application.

Example:

```python
import tornado.ioloop
from tornado_console import ConsoleServer

my_locals = {}

console_server = ConsoleServer(my_locals)

my_locals['server'] = console_server

if __name__ == '__main__':
    io_loop = tornado.ioloop.IOLoop.current()
    console_server.listen(1234)
    
    try:
        io_loop.start()
    except KeyboardInterrupt:
        pass
```

Now connect to ``localhost:1234`` using ``nc`` or ``telnet``:

```bash
$ nc localhost 1234
PyPy 2.7.13 (c925e73810367cd960a32592dd7f728f436c125c, Jun 09 2017, 01:01:49)
[PyPy 5.8.0 with GCC 4.2.1 Compatible Apple LLVM 8.1.0 (clang-802.0.42)] on Darwin-16.7.0-x86_64-i386-64bit (TornadoConsole)
>>> 
```

You can now run arbitrary Python commands in the running process. Type
``quit()`` (or kill the connection) to exit the interactive console.
