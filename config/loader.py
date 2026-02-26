import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROMPTS_PATH = BASE_DIR / "config" / "prompts.yaml"

def load_prompts():
    with open(PROMPTS_PATH, "r") as f:
        return yaml.safe_load(f)