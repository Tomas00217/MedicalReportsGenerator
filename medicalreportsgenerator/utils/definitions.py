from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
LOCALE_PATH = PROJECT_ROOT / "src" / "report" / "stroke_discharge" / "locale"
DEFAULT_LOCALE = LOCALE_PATH / "en_US.json"
DEFAULT_TEMPLATE_PATH = PROJECT_ROOT / "src" / "report" / "stroke_discharge" / "main.txt"
DEFAULT_CSV_PATH = PROJECT_ROOT / "src" / "data" / "data.csv"
DEFAULT_STORE_PATH = PROJECT_ROOT / "medical_report.txt"
