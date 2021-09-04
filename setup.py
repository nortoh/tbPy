from distutils.core import setup
setup(
    name='tbPy',
    version='1.0',
    description='Python Twitch Bot Library',
    author='nortoh',
    author_email='christian@christianhorton.me',
    packages=['Events', 'websockets', 'requests', 'jaraco.util']
)