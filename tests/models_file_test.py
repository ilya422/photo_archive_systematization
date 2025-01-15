import pytest

from datetime import datetime

from models import File, FileException


class TestModelsFile:
    CORRECT_FILEPATH = './source_dir/photo 1.jpg'

    @pytest.mark.parametrize("filepath, result", [
        (CORRECT_FILEPATH, True),
        ('', FileException),
        (0, FileException),
        (True, FileException),
        (None, FileException),
    ])
    def test_init(self, filepath, result):
        try:
            f = File(filepath=filepath)
            assert True == result
            assert f.filepath == filepath
            assert f.filename == filepath.replace('\\', '/').split('/')[-1]
        except Exception as ex:
            assert isinstance(ex, result)

    @pytest.mark.parametrize("filepath, result", [
        (CORRECT_FILEPATH, datetime(2025, 1, 15)),
        ('', FileException),
        (0, FileException),
        (True, FileException),
        (None, FileException),
    ])
    def test_created_at(self, mocker, filepath, result):
        mocker.patch('os.path.getctime', return_value=1736881200)

        try:
            f = File(filepath=filepath)
            assert f.created_at == result
        except Exception as ex:
            assert isinstance(ex, result)

    @pytest.mark.parametrize("filepath, result", [
        (CORRECT_FILEPATH, True),
        ('', FileException),
        (0, FileException),
        (True, FileException),
        (None, FileException),
    ])
    def test_copy_file(self, mocker, filepath, result):
        mocker.patch('aiofiles.threadpool.binary.AsyncBufferedIOBase.write')

        try:
            f = File(filepath=filepath)
            f.copy_file('./test.img')
            assert result
        except Exception as ex:
            assert isinstance(ex, result)