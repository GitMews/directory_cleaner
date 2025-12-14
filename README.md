# directory_cleaner
Simple Python automation script to periodically clean a directory, log deleted files, and send email alerts when specific conditions are met.

Designed as a lightweight, configurable tool for recurring maintenance tasks.

---

## Context

Given a folder in which files are frequently dumped, like the following one:

<img width="227" height="186" alt="image" src="https://github.com/user-attachments/assets/f6c6c067-fa2c-4879-930b-d48b84ec01c8" />


The aim of this project is to:
- Clean the chosen folder on execution
- Log every deleted file in a dedicated log file
  
<img width="287" height="204" alt="image" src="https://github.com/user-attachments/assets/59418ba9-424e-403e-ac0c-837f1b5669ee" />

- Send a warning email for every deleted file containing a specific keyword
  
<img width="415" height="145" alt="image" src="https://github.com/user-attachments/assets/7ffbfb65-3b29-4495-8180-21e5b49a6702" />

- Be designed to run as a systemd service

---

## Script description

- `cleaner.py` – main script responsible for directory cleanup, logging and alerts
- `config.ini` – runtime configuration and user-defined parameters

---

## How to run it

To use the script locally, clone the repository using the `git clone` command, then set up a virtual environment:

```bash
python3 -m venv env
source env/bin/activate
```

Once done, configure the application:
* Rename `config.ini.empty` to `config.ini`
* Fill the file with your own parameters (email settings, directory paths, keyword)

You can then test the script with:
```bash
python cleaner.py
```

After execution, you will be able to check:

* the cleaned directory
* the generated business log file
* the technical log file (in root folder)
* the alert email received (if applicable)

You should now have everything needed to run the script on a local computer.
If you want to learn how to deploy it on an Ubuntu server using systemd, feel free to contact me directly (see GitMews on GitHub).
