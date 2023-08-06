from distutils.core import setup, Extension
setup(name="mimircache", version="1.0",
      ext_modules=[Extension("mimircache", ["readerType.c"])])