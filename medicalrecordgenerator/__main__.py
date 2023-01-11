import locale
import sys
import getopt

from app.generator import MedicalRecordsGenerator
from utils import load_utils

OPTIONS = "l:"
LONG_OPTIONS = ["language="]


def main(argv=None):
    app_language = 'en_US'

    try:
        opts, args = getopt.getopt(argv, OPTIONS, LONG_OPTIONS)
        for opt, arg in opts:
            if opt in "-l, --language":
                app_language = arg
    except getopt.GetoptError as err:
        print(err)

    generate(app_language)


def generate(app_language: str) -> None:
    locale.setlocale(locale.LC_ALL, app_language)

    language = load_utils.load_language(app_language)

    data = load_utils.load_csv("data/anonymized_data.csv")

    for idx, row in enumerate(data):

        generator = MedicalRecordsGenerator(language, row)
        report = generator.generate_medical_record()
        print(report)
        """
        with open(f"med_record{idx+1}.txt", "w") as file:
            file.write(report + "\n")
        """


if __name__ == '__main__':
    main(sys.argv[1:])
