import configparser
from datetime import datetime
from pathlib import Path

# Get config file
CONFIG_FILE = Path("config.ini")

# Load config
def load_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config

# Get Files list
def list_files(directory: Path):
    if not directory.exists():
        raise FileNotFoundError(f"Directory does not exist: {directory}")

    if not directory.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory}")

    return [f for f in directory.iterdir() if f.is_file()]

# Ensure log directory exists
def ensure_log_directory(log_dir: Path):
    log_dir.mkdir(parents=True, exist_ok=True)

# Get file log path
def get_log_file_path(log_dir: Path):
    timestamp = datetime.now().strftime("%Y-%m-%d")
    return log_dir / f"directory-cleaner_{timestamp}.log"

# Write log
def write_log(log_file: Path, files: list[Path]):
    with log_file.open("w", encoding="utf-8") as f:
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        f.write(f"Found {len(files)} file(s)\n")

        for file in files:
            f.write(f"- {file.name}\n")

# Find keyword
def find_keyword_matches(files: list[Path], keyword: str):
    return [f for f in files if keyword in f.name]

# Main function
def main():
    # Setup
    config = load_config()
    target_dir = Path(config["general"]["target_directory"]).resolve()
    log_dir = Path(config["general"]["log_directory"]).resolve()
    files = list_files(target_dir)

    # Log generation
    ensure_log_directory(log_dir)
    write_log(get_log_file_path(log_dir), files)

    # Alert if needed
    keyword = config["general"]["keyword"]
    matches = find_keyword_matches(files, keyword)
    if matches:
        print(f"Keyword '{keyword}' found in {len(matches)} file(s):")
        for f in matches:
            print(" -", f.name)
    else:
        print(f"No file contains keyword '{keyword}'")

if __name__ == "__main__":
    main()
