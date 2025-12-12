import configparser
from datetime import datetime
from pathlib import Path
import smtplib
from email.message import EmailMessage
import logging
from logging import Logger

# Logger
LOGGER = logging.getLogger("directory_cleaner")

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
        f.write(f"Deleted {len(files)} file(s)\n")

        for file in files:
            f.write(f"- {file.name}\n")

# Find keyword
def find_keyword_matches(files: list[Path], keyword: str):
    return [f for f in files if keyword in f.name]

# Delete files
def delete_files(files: list[Path]):
    for file in files:
        try:
            file.unlink()
            LOGGER.info(f"Deleted: {file.name}")
        except Exception as e:
            LOGGER.error(f"Failed to delete {file.name}: {e}")

# Send mail
def send_alert_email(config, matched_file: Path):
    str_name = str(matched_file.name)

    msg = EmailMessage()
    msg["Subject"] = "Directory cleaner alert: WARNING file " +  str_name + " deleted"
    msg["From"] = config["email"]["smtp_user"]
    msg["To"] = config["email"]["target"]

    body = "The following file containing WARNING has been deleted:\n\n"
    body += str(matched_file.name)

    msg.set_content(body)

    with smtplib.SMTP(config["email"]["smtp_host"], int(config["email"]["smtp_port"])) as server:
        server.starttls()
        server.login(
            config["email"]["smtp_user"],
            config["email"]["smtp_password"]
        )
        server.send_message(msg)

# Setup logger
def setup_logger():
    logging.basicConfig(
        filename="directory_cleaner.log",
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        encoding="utf-8",
        filemode="w")

# Main function
def main():
    # Run logs
    setup_logger()
    LOGGER.info("Directory cleaner started")

    # Setup
    config = load_config()
    target_dir = Path(config["general"]["target_directory"]).resolve()
    log_dir = Path(config["general"]["log_directory"]).resolve()
    files = list_files(target_dir)

    # Log generation
    ensure_log_directory(log_dir)
    write_log(get_log_file_path(log_dir), files)

    # Get relevant files
    keyword = config["general"]["keyword"]
    matches = find_keyword_matches(files, keyword)
    if matches:
        LOGGER.info(f"Keyword '{keyword}' found in {len(matches)} file(s):")
        for f in matches:
            LOGGER.info(f.name)
    else:
        LOGGER.info(f"No file contains keyword '{keyword}'")

    # Delete files if needed
    if files:
        delete_files(files)
    else:
        LOGGER.info("No files to delete")

    # Send email if needed
    if matches and config["email"].getboolean("enabled"):
        for f in matches :
            try:
                send_alert_email(config, f)
                LOGGER.info(f"Alert email sent for : {f.name}")
            except Exception as e:
                LOGGER.error(f"Failed to send alert email: {e}")

# Run
if __name__ == "__main__":
    main()
