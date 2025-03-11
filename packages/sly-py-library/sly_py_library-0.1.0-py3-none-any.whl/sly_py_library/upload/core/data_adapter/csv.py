import csv
import tempfile

from sly_py_library.upload.core.data_adapter.base import BaseDataAdapter


class CSVDataAdapter(BaseDataAdapter):
    @classmethod
    def parse_data(cls, data):
        with tempfile.NamedTemporaryFile(
            delete=False, mode="w", newline="", encoding="utf8"
        ) as temp_file:
            writer = csv.writer(temp_file)
            writer.writerows(data)

            temp_file_path = temp_file.name
            temp_file.seek(0)

        return open(temp_file_path, "rb")
