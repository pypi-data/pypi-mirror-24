from abc import ABCMeta, abstractmethod
from akagi.iterators import CSVIterator, BinaryIterator
import six


class FileFormat(object):
    CSV = 1
    BINARY = 2


@six.add_metaclass(ABCMeta)
class Iterator(object):
    @classmethod
    def open_file(self, path):
        raise NotImplementedError

    @abstractmethod
    def decode(self, content):
        '''Return decoded content.'''

    @classmethod
    def get_iterator_class(cls, file_format):
        if file_format in [FileFormat.CSV, 'csv']:
            return CSVIterator
        elif file_format in [FileFormat.BINARY, 'binary']:
            return BinaryIterator
        else:
            raise Exception("Unsupported file format %(file_format)s." % locals())
