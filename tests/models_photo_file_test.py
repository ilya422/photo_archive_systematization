import pytest

from datetime import datetime

from models import PhotoFile, PhotoFileException, FileException


class TestModelsPhotoFile:
    CORRECT_FILEPATH = './source_dir/photo 1.jpg'
    CORRECT_FILEPATH_WITHOUT_DATE = './source_dir/no date photo.jpg'

    @pytest.mark.parametrize("filepath, result", [
        (CORRECT_FILEPATH, True),
        ('', PhotoFileException),
        (0, PhotoFileException),
        (True, PhotoFileException),
        (None, PhotoFileException),
    ])
    def test_init(self, filepath, result):
        try:
            f = PhotoFile(filepath=filepath)
            assert True == result
            assert f.filepath == filepath
            assert f.filename == filepath.replace('\\', '/').split('/')[-1]
        except Exception as ex:
            assert isinstance(ex, result)

    @pytest.mark.parametrize("filepath, result", [
        (CORRECT_FILEPATH, datetime(2024, 12, 27, 12, 43, 59)),
        (CORRECT_FILEPATH_WITHOUT_DATE, datetime(2025, 1, 15)),
        ('', FileException),
        (0, FileException),
        (True, FileException),
        (None, FileException),
    ])
    def test_created_at(self, mocker, filepath, result):
        mocker.patch('os.path.getctime', return_value=1736881200)

        try:
            f = PhotoFile(filepath=filepath)
            assert f.created_at == result
        except Exception as ex:
            assert isinstance(ex, result)