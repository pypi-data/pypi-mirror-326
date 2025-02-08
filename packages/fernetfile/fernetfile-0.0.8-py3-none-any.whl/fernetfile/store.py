# -*- encoding: utf-8 -*-
""" Store your files in a ztsd/tar based archive.

Interface "compatible" with tar :

- open :
    - decrompress and extract crypted files in a temporary directory

=> need to be thread safe (flush can be called from another thread)

"""
__license__ = """
    All rights reserved by Labo-Online
"""
__copyright__ = "Copyright ©2024-2025 "
__author__ = 'bibi21000 aka Sébastien GALLET'
__email__ = 'bibi21000@gmail.com'

import os
import sys
import struct
import builtins
from contextlib import contextmanager
import tarfile
import io
import logging
from cryptography.fernet import Fernet


import tarfile

# when using read mode (decompression), the level_or_option parameter
# can only be a dict object, that represents decompression option. It
# doesn't support int type compression level in this case.

class ZstdTarFile(tarfile.TarFile):
    def __init__(self, name, mode='r', *, level_or_option=None, zstd_dict=None, **kwargs):
        self.zstd_file = ZstdFile(name, mode,
                                  level_or_option=level_or_option,
                                  zstd_dict=zstd_dict)
        try:
            super().__init__(fileobj=self.zstd_file, mode=mode, **kwargs)
        except:
            self.zstd_file.close()
            raise

    def close(self):
        try:
            super().close()
        finally:
            self.zstd_file.close()

    def __repr__(self):
        s = repr(self.zstd_file)
        return '<ZstdTarFile ' + s[1:-1] + ' ' + hex(id(self)) + '>'


class FernetStore():
    """

    """

    def __init__(self, filename=None, mode=None, fernet_key=None, **kwargs):
        """Constructor for the FernetFile class.

        At least one of fileobj and filename must be given a
        non-trivial value.

        The new class instance is based on fileobj, which can be a regular
        file, an io.BytesIO object, or any other object which simulates a file.
        It defaults to None, in which case filename is opened to provide
        a file object.

        When fileobj is not None, the filename argument is only used to be
        included in the gzip file header, which may include the original
        filename of the uncompressed file.  It defaults to the filename of
        fileobj, if discernible; otherwise, it defaults to the empty string,
        and in this case the original filename is not included in the header.

        The mode argument can be any of 'r', 'rb', 'a', 'ab', 'w', 'wb', 'x', or
        'xb' depending on whether the file will be read or written.  The default
        is the mode of fileobj if discernible; otherwise, the default is 'rb'.
        A mode of 'r' is equivalent to one of 'rb', and similarly for 'w' and
        'wb', 'a' and 'ab', and 'x' and 'xb'.

        The fernet_key argument is the Fernet key used to crypt/decrypt data.

        Encryption is done by chunks to reduce memory footprint. The default
        chunk_size is 64KB.
        """
        if fernet_key is None:
            raise ValueError("Invalid fernet key: {!r}".format(fernet_key))
        self.fernet_key = fernet_key
        self.mode = mode
        self.level_or_option = kwargs.pop('level_or_option', None)
        self.zstd_dict = kwargs.pop('zstd_dict', None)
        self.chunk_size = kwargs.pop('chunk_size', CHUNK_SIZE)
        self.write_buffer_size = kwargs.pop('write_buffer_size', WRITE_BUFFER_SIZE)
        if self.chunk_size != CHUNK_SIZE and write_buffer_size == WRITE_BUFFER_SIZE:
            self.write_buffer_size = 5 * self.chunk_size

        self.dirobj = None
        self.zstdtar = ZstdTarFile(filename, mode=self.mode, level_or_option=self.level_or_option, zstd_dict=self.zstd_dict, **kwargs)

    def __repr__(self):
        s = repr(self.zstdtar)
        return '<FernetStore ' + s[1:-1] + ' ' + hex(id(self)) + '>'

    def _check_not_closed(self):
        if self.closed:
            raise ValueError("I/O operation on closed file")

    def _check_can_read(self):
        if not self.readable():
            raise io.UnsupportedOperation("File not open for reading")

    def _check_can_write(self):
        if not self.writable():
            raise io.UnsupportedOperation("File not open for writing")

    def __enter__(self):
        return self.open()

    def __exit__(self, type, value, traceback):
        self.close()

    def open(self):
        pass

    def close(self):
        pass

    def flush(self):
        pass

    @contextmanager
    def file(self, arcname=None ):
        try:
            f = open(filename, mode)
            yield f
        except Exception as e:
            print(e)
        finally:
            f.close()

    def write(self, data, arcname=None ):
        pass

    def delete(self, arcname):
        pass

    def read(self, arcname=None):
        pass

    def readline(self, arcname=None):
        """
        """
        self._check_not_closed()
        return self._buffer.readline(size)

    def writelines(self, lines, arcname=None):
        """
        """
        self._check_not_closed()
        return self._buffer.readline(size)

    @property
    def mtime(self):
        """Last modification time read from stream, or None"""
        return None

    @property
    def closed(self):
        """True if this file is closed."""
        return self.fileobj is None

    def fileno(self):
        """Invoke the underlying file object's fileno() method.

        This will raise AttributeError if the underlying file object
        doesn't support fileno().
        """
        self._check_not_closed()
        return self.fileobj.fileno()

    def readable(self):
        """Return whether the file was opened for reading."""
        self._check_not_closed()
        return self.mode == READ

    def writable(self):
        """Return whether the file was opened for writing."""
        self._check_not_closed()
        return self.mode == WRITE

