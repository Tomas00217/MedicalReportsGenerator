import locale

from medicalrecordgenerator.utils import load_utils
from medicalrecordgenerator.generator import generator


def main():
    app_language = 'en_US'
    locale.setlocale(locale.LC_ALL, app_language)

    language = load_utils.load_language(app_language)

    data = load_utils.load_csv("data/anonymized_data.csv")

    for idx, row in enumerate(data):
        # print(row)
        report = generator.generate_medical_record(language, row)
        print(report)
        """
        with open(f"med_record{idx+1}.txt", "w") as file:
            file.write(report + "\n")
        """


if __name__ == '__main__':
    main()
