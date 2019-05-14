import os

from django.urls import reverse
from django.core.files.base import File
from django.core.files.storage import default_storage
from django.core.serializers.json import DjangoJSONEncoder


class StreamFieldDataEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, StreamFieldFile):
            return {
                'name': o.name,
                'filename': o.filename,
            }
        return super().default(o)


class StreamFieldFile(File):
    def __init__(self, *args, filename=None, storage=default_storage, is_submission=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.storage = storage
        self.filename = filename or os.path.basename(self.name)
        self._committed = False
        self.is_submission = is_submission

    def __str__(self):
        return self.filename

    def __eq__(self, other):
        if isinstance(other, File):
            return self.filename == other.filename and self.size == other.size
        # Rely on the other object to know how to check equality
        # Could cause infinite loop if the other object is unsure how to compare
        return other.__eq__(self)

    def _get_file(self):
        if getattr(self, '_file', None) is None:
            self._file = self.storage.open(self.name, 'rb')
        return self._file

    def _set_file(self, file):
        self._file = file

    def _del_file(self):
        del self._file

    file = property(_get_file, _set_file, _del_file)

    def read(self, chunk_size=None):
        self.file.seek(0)
        if chunk_size:
            return super().read(chunk_size)
        else:
            return super().read()

    @property
    def path(self):
        return self.storage.path(self.name)

    @property
    def url(self):
        if self.is_submission:
            return reverse('apply:submissions:private_media_redirect', args=[self.name])
        return self.storage.url(self.name)

    @property
    def size(self):
        if not self._committed:
            return self.file.size
        return self.storage.size(self.name)

    def serialize(self):
        return {
            'url': self.url,
            'filename': self.filename,
        }

    def open(self, mode='rb'):
        if getattr(self, '_file', None) is None:
            self.file = self.storage.open(self.name, mode)
        else:
            self.file.open(mode)
        return self

    def save(self, folder):
        name = self.name
        if not name.startswith(folder):
            name = os.path.join(folder, name)
        name = self.storage.generate_filename(name)
        if not self._committed:
            self.name = self.storage.save(name, self.file)
        self._committed = True

    def delete(self, save=True):
        if not self:
            return
        # Only close the file if it's already open, which we know by the
        # presence of self._file
        if hasattr(self, '_file'):
            self.close()
            del self.file

        self.storage.delete(self.name)

        self.name = None
        self._committed = False

    @property
    def closed(self):
        file = getattr(self, '_file', None)
        return file is None or file.closed

    def close(self):
        file = getattr(self, '_file', None)
        if file is not None:
            file.close()
