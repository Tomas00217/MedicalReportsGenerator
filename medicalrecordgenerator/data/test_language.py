from data.language import Language
from utils.load_utils import load_language


def main():
    language = load_language("en_US")
    print(language)
    idk: Language = Language(**language)
    print(idk.onset.variants[0].condition.condition.conditions[0].value)


if __name__ == '__main__':
    main()
