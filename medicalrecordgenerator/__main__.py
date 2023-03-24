import logging
import sys
import getopt

from app.app_operations import generate, show_help


OPTIONS = "hl:i:"
LONG_OPTIONS = ["help", "csv", "language=", "subject_id="]


def main(argv=None):
    app_language = 'en_US'
    subject_id = None

    load_csv = False

    try:
        opts, args = getopt.getopt(argv, OPTIONS, LONG_OPTIONS)
        for opt, arg in opts:
            if opt in "-h, --help":
                show_help()
                return
            if opt in "--csv":
                load_csv = True
            if opt in "-l, --language":
                app_language = arg
            if opt in "-i, --subject_id":
                subject_id = arg
    except getopt.GetoptError as err:
        logging.error(err)

    generate(app_language, load_csv, subject_id, )


if __name__ == '__main__':
    main(sys.argv[1:])
