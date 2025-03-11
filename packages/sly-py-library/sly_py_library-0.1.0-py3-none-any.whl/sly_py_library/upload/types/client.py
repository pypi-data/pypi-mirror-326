from enum import Enum
from pydantic import BaseModel
from typing import Optional

from sly_py_library.upload.types.ftp import FTPData


class UploadType(str, Enum):
    FTP = "FTP"


class UploadData(BaseModel):
    ftp_data: Optional[FTPData]
