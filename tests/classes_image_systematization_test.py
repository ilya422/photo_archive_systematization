import pytest

from classes.image_systematization import ImageSystematization, ImageSystematizationException


class TestClassesImageSystematization:
    CORRECT_FILEPATH = './source_dir'

    @pytest.mark.parametrize("source_dir, result", [
        (CORRECT_FILEPATH, 7),
        ('', 0),
        (True, ImageSystematizationException),
        (1, ImageSystematizationException),
        (None, ImageSystematizationException),
    ])
    def test_get_photo_files_info(self, source_dir, result):
        try:
            photos = ImageSystematization._ImageSystematization__get_photo_files_info(source_dir=source_dir)
            assert len(photos) == result
        except Exception as ex:
            assert isinstance(ex, result)
