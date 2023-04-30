import argparse
import logging

from app.app_operations import generate, list_ids
from utils.definitions import DEFAULT_CSV_PATH, DEFAULT_TEMPLATE_PATH, DEFAULT_STORE_PATH


def main():
    load_csv = False
    csv_file = DEFAULT_CSV_PATH
    app_language = 'en_US'
    subject_id = None
    definition_template_path = DEFAULT_TEMPLATE_PATH
    store_to_file = False
    store_path = DEFAULT_STORE_PATH

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--csv", help="Specify whether to load data from CSV instead of the database. The value "
                                            "supplied with this option specifies the CSV file. When omitted, "
                                            "default CSV is used",
                        required=False, nargs="?", const=DEFAULT_CSV_PATH)
    parser.add_argument("-l", "--language", help="Specify the language which to use for the generation "
                                                 "process. en_US by default",
                        required=False, default="en_US")
    parser.add_argument("-i", "--subject_id", help="Specify the id of the subject for which to generate the "
                                                   "report. None by default, resulting in generation for every "
                                                   "subject",
                        required=False, default=None, type=int)
    parser.add_argument("-t", "--template", help="Specify the path to report definition template for use",
                        required=False, default=DEFAULT_TEMPLATE_PATH)
    parser.add_argument("--list", help="Lists the available subject ids and exits",
                        required=False, action="store_true")
    parser.add_argument("-s", "--store", help="Specify whether to store the result to a txt file. By default, "
                                              "the result is printed to the console. The value supplied with this "
                                              "option specifies the file path. When omitted, the result is stored in "
                                              "the project root",
                        required=False, nargs="?", const=DEFAULT_STORE_PATH)

    argument = parser.parse_args()

    if argument.csv:
        load_csv = True
        csv_file = argument.csv
        print(f"Using csv file: {csv_file}")
    if argument.list:
        print(f"Listing all available subject ids: ")
        print(list_ids(load_csv, csv_file))
        return
    if argument.language:
        app_language = argument.language
        print(f"Using language: {app_language}")
    if argument.subject_id:
        subject_id = argument.subject_id
        if subject_id:
            print(f"Generating for subject id: {subject_id}")
        else:
            print(f"Generating for all subjects")
    if argument.template:
        definition_template_path = argument.template
        print(f"Generating with template from file: {definition_template_path}")
    if argument.store:
        store_to_file = True
        store_path = argument.store

    try:
        report = generate(app_language, subject_id, load_csv, csv_file, definition_template_path)
    except Exception as error:
        logging.error(f"Generation failed: {error}")
        return

    if store_to_file:
        print(f"Storing results to file: {store_path}")
        with open(store_path, "w") as file:
            file.write(report)
    else:
        print(f"Printing results to console:")
        print(report)


if __name__ == '__main__':
    main()
