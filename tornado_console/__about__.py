__all__ = [
    'description',
    'maintainer',
    'maintainer_email',
    'url',
    'version_info',
    'version',
]

version_info = (1, 0, 0)
version = '.'.join(map(bytes, version_info))

maintainer = 'Nick Joyce'
maintainer_email = 'nick.joyce@realkinetic.com'

description = """
Python interactive console running alongside your Tornado application - very
useful for debugging purposes or tracking down memory leaks.
""".strip()

url = 'https://github.com/RealKinetic/tornado_console'
