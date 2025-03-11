import ftplib
import os

from .base import BaseUploadService
from sly_py_library.upload.types.client import UploadType, UploadData
from sly_py_library.upload.core.data_adapter import CSVDataAdapter
from sly_py_library.upload.types.ftp import FTPServiceConfig, FTPFileType, FTPData, FTPParsedData
from sly_py_library.upload.errors.upload_error import SendDataError, ConnectError, ConfigurationError


class FTPUploadService(BaseUploadService):
    upload_type = UploadType.FTP

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        config = self._init_config(**kwargs)
        self.host = config.host
        self.username = config.username
        self.password = config.password
        self.remote_path = config.remote_path

    def _init_config(self, **kwargs):
        try:
            return FTPServiceConfig(**kwargs)
        except Exception as e:
            print(e)
            raise ConfigurationError

    def connect(self):
        if self._client is not None:
            self.close()
        try:
            self._client = ftplib.FTP(self.host)
            self._client.login(self.username, self.password)
            print(f"Connected to {self.host}")
            self._is_connect = True
        except Exception as e:
            print(e)
            raise ConnectError

    def close(self):
        if self._client:
            self._client.quit()
            self._client = None
            self._is_connect = False
            print("Connection closed.")

    def _parse(self, upload_data: UploadData) -> FTPParsedData:
        data: FTPData = upload_data.ftp_data
        if data.file_type == FTPFileType.CSV:
            parsed_data = CSVDataAdapter.parse_data(data.data)
        else:
            raise NotImplementedError
        return FTPParsedData(
            file_name=data.build_full_path(self.remote_path), data=parsed_data
        )

    def _upload(self, data: FTPParsedData):
        try:
            if not self._is_connect:
                raise ConnectError(message="not connect yet")
            self._client.storbinary(
                f"STOR {self._build_remote_file(data.file_name)}", data.data
            )
            print(f"Successfully uploaded to {data.file_name}")
        except Exception as e:
            print(e)
            raise SendDataError

    def _build_remote_file(self, file_name):
        return os.path.join(self.remote_path, file_name)
