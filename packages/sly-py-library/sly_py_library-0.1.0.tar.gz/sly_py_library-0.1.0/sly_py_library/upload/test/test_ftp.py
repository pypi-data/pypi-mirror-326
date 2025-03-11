import unittest

from sly_py_library.upload.api.service import upload
from sly_py_library.upload.types.client import UploadType, UploadData
from sly_py_library.upload.types.ftp import FTPData, FTPFileType


class FTPTest(unittest.TestCase):
    def test_ftp_upload(self):
        ftp_config = {
            "host": "10.1.31.181",  # 测试host
            "username": "solax",
            "password": "sly402",
            "remote_path": "/xixi",
        }
        upload(
            upload_type=UploadType.FTP,
            configuration=ftp_config,
            upload_data=UploadData(
                ftp_data=FTPData(
                    file_type=FTPFileType.CSV,
                    file_name="new_file.csv",
                    data=[["curry", 37, "男"], ["james", 40, "男"], ["lily", 16, "女"]],
                ),
            ),
        )
