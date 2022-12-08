from medicalrecordgenerator.data.parser import parse
from medicalrecordgenerator.utils import load_utils

dictionary = load_utils.load_language_file("..\\locales\\test.json")


def test_and():
    data = {"test_and": True, "test_or": False, "first": True, "second": False, "third": True}

    assert parse(dictionary, data) == "tft"

    data = {"test_and": True, "test_or": False, "first": False, "second": False, "third": True}

    assert parse(dictionary, data) == "fft"

    data = {"test_and": True, "test_or": False, "first": True, "second": True, "third": False}

    assert parse(dictionary, data) == "ttf"


def test_or():
    data = {"test_and": False, "test_or": True, "first": True, "second": True, "third": True}

    assert parse(dictionary, data) == "fftttf"


if __name__ == "__main__":
    print("Testing diagnosis AND")
    test_and()
    print("PASSED")

    print("Testing diagnosis OR")
    test_or()
    print("PASSED")

    print("Everything passed")
