from django.core.files.uploadhandler import FileUploadHandler, StopUpload, UploadFileException
from django.core.files.uploadedfile import UploadedFile
from django.core.files.base import File
from django.conf import settings
from django.core.cache import cache
import dropbox

class DropboxFileUploadHandler(FileUploadHandler):
    def __init__(self, request):
        super(DropboxFileUploadHandler, self).__init__(request)
        self.dropbox = dropbox.Dropbox(settings.DROPBOX_UPLOAD_HANDLER['ACCESS_TOKEN'])
        self.progress_id = None
        self.cache_key = None


    def handle_raw_input(self, input_data, META, content_length, boundary, encoding=None):
        self.content_length = content_length
        if 'progress_id' in self.request.GET:
            self.progress_id = self.request.GET['progress_id']
        elif 'progress_id' in self.request.META:
            self.progress_id = self.request.META['progress_id']

        if self.progress_id:
            self.cache_key = "%s_%s" % (self.request.META['REMOTE_ADDR'], self.progress_id )
            cache.set(self.cache_key, {
                'length': self.content_length,
                'uploaded' : 0
            })

    def upload_complete(self):
        if self.cache_key:
            cache.delete(self.cache_key)

    def new_file(self, *args, **kwargs):
        super(DropboxFileUploadHandler, self).new_file(*args, **kwargs)
        upload_path = settings.DROPBOX_UPLOAD_HANDLER.get('UPLOAD_PATH', '/')
        if upload_path[0] != '/':
            upload_path = '/' + upload_path
        if upload_path[-1] != '/':
            upload_path = upload_path + '/'

        self.upload_path = upload_path + self.file_name
        self.count = 0

    def receive_data_chunk(self, raw_data, start):
        content_length = self.request.META.get('CONTENT_LENGTH',0) if self.content_length is None else self.content_length
        try:
            if self.count == 1:
                session_result = self.dropbox.files_upload_session_start(self.chunk)
                self.cursor = dropbox.files.UploadSessionCursor(session_result.session_id, offset=len(self.chunk))
            elif self.count > 1:
                self.dropbox.files_upload_session_append_v2(self.chunk, self.cursor)
                self.cursor.offset += len(self.chunk)
                if self.cache_key:
                    data = cache.get(self.cache_key)
                    data['uploaded'] += len(self.chunk)
                    cache.set(self.cache_key, data)
            self.chunk = raw_data
            self.count += 1
        except:
            raise StopUpload(True)

        return None

    def file_complete(self, file_size):
        if self.count == 1:
            self.metadata = self.dropbox.files_upload(self.chunk, self.upload_path, dropbox.files.WriteMode.overwrite, None, None, True)
        else:
            commit = dropbox.files.CommitInfo(self.upload_path, dropbox.files.WriteMode.overwrite, None, None, mute=True)
            self.metadata = self.dropbox.files_upload_session_finish(self.chunk, self.cursor, commit)
        if self.cache_key:
            data = cache.get(self.cache_key)
            data['uploaded'] += len(self.chunk)
            cache.set(self.cache_key, data)

        return DropboxFile(self.metadata, self.upload_path)

class DropboxFile(File):
    def __init__(self, file, upload_path):
        self.metadata = file
        self.upload_path = upload_path
        self._size = self.metadata.size
        super(DropboxFile, self).__init__(file, name=file.name)
