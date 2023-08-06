import json
import os

from abc import ABCMeta, abstractmethod, abstractproperty
import akagi
from akagi.log import logger

from concurrent.futures import ThreadPoolExecutor
import six


@six.add_metaclass(ABCMeta)
class DataSource(object):
    '''DataSource is an abstract base class of all data sources
    '''

    def save(self, force=False):
        paths = []
        paths.append(self._save_metadata())

        with ThreadPoolExecutor() as executor:
            paths = list(executor.map(self._save_data_file, self.bundle.data_files))

        return paths

    def _save_data_file(self, data_file):
        path = os.path.join(self._local_cache_dir, data_file.key)
        dirname = os.path.dirname(path)

        if not os.path.isdir(dirname):
            try:
                os.makedirs(dirname)
            except FileExistsError:
                pass

        if os.path.isfile(path) or os.path.isdir(path):
            logger.debug("Skipped %(key)s" % ({"key": data_file.key}))
        else:
            with open(path, 'wb') as f:
                f.write(data_file.raw_content)
                logger.debug("Saved %(key)s to %(path)s" % ({"key": data_file.key, "path": path}))

        return path

    def _save_metadata(self):
        path = self._local_cache_dir + '.json'

        metadata = {'iterator_class': self.bundle.iterator_class.__name__}

        with open(path, 'w') as f:
            json.dump(metadata, f)

        return path

    def exists_local(self):
        # TODO: Prone to error during self.save()
        return len(os.listdir(self._local_cache_dir)) > 0

    @property
    def _local_cache_dir(self):
        path = os.getenv('AKAGI_LOCAL_CACHE', akagi.home())
        if not os.path.isdir(path):
            os.makedirs(path, mode=0o755)

        cache_dir = os.path.join(path, 'cache', self._hex_hash)

        if not os.path.isdir(cache_dir):
            os.makedirs(cache_dir, mode=0o755)

        return cache_dir

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    @abstractmethod
    def __iter__(self):
        raise NotImplementedError

    @abstractproperty
    def _hex_hash(self):
        '''Returns hash value of the data source.

        It's utilized in its caching capability.
        '''
