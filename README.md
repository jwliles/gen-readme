# **README Generator Script**

## **Overview**

This project automates the process of generating `README.md` files for a directory and its subdirectories. It scans all directories, identifies changes in files, and creates or updates `README.md` files in each folder to provide an overview of the directory structure. It is designed to handle large file systems efficiently, with built-in logging, database tracking, and support for skipping hidden files.

## **Features**
- **Efficient Scanning**: Uses parallel processing to quickly scan large directories.
- **Change Detection**: Tracks file changes using file hashes stored in a SQLite database.
- **README Creation/Update**: Automatically creates or updates `README.md` files in directories.
- **Customizable Logging**: Logs events and errors to both the terminal and a log file, while storing important data in a database.
- **Metrics and Reporting**: Tracks and reports the number of files scanned, skipped files, README files created/updated, and total execution time.

## **Project Structure**

The project is organized into modules for easy maintenance and scalability:

```
.
├── db
│   ├── file_hashes.db          # SQLite database for storing file hashes
│   ├── hash_db.py              # Functions to interact with the database
│   └── schema_manager.py       # Handles database schema creation/verification
├── detection
│   ├── change_detector.py      # Detects changes in files based on hashes
│   └── change_handler.py       # Handles file change detection logic
├── generate-readme.py          # Main script for running the README generation process
├── hashing
│   ├── hash_computer.py        # Computes file hashes
│   ├── hash_verifier.py        # Verifies hashes for detecting changes
├── logs
│   ├── event_logger.py         # Logs events like file changes and creation of README files
│   ├── log_config.py           # Logging configuration
│   └── skipped_file_logger.py  # Logs skipped files
├── metrics
│   └── scan_metrics.py         # Tracks scan statistics (files scanned, time taken, etc.)
├── output
│   ├── readme_manager.py       # Handles the creation and updating of README files
│   └── terminal_output.py      # Prints metrics and updates to the terminal
├── scanning
│   ├── directory_scanner.py    # Scans directories for files
│   ├── file_scanner.py         # Scans files within directories
│   └── scan_manager.py         # Manages the scanning process and integrates other modules
└── README.md                   # This file
```

## **Dependencies**

- Python 3.10+
- SQLite (bundled with Python)
- **Python Libraries**:
  - `concurrent.futures` (for parallel processing)
  - `logging` (for logging events and errors)
  - `argparse` (for argument parsing)
  - `os` and `time` (for file management and timing)

## **Setup and Installation**

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd gen-readme
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies** (if any):
   ```bash
   pip install -r requirements.txt  # if using external libraries (currently not required)
   ```

4. **Add the script to your PATH** (optional):
   - To make the script globally accessible, you can add the project directory to your system’s `$PATH`.

## **Usage**

Run the script to generate `README.md` files for a directory and its subdirectories:

```bash
./generate-readme.py -p <directory_path>
```

### **Options**:
- `-p`, `--path` : Root directory path. Defaults to the current working directory if not specified.

## **How it Works**

1. **Database Initialization**: The script initializes an SQLite database (`file_hashes.db`) that stores file paths and their corresponding hashes.
2. **Scanning Files**: It recursively scans the directory specified, processing all files and folders while skipping hidden files and folders.
3. **Change Detection**: For each file, it computes the file hash and checks it against the stored hash in the database. If the file has changed (or is new), it marks the file for inclusion in the `README.md` file.
4. **README Creation/Update**: In each directory, the script creates or updates the `README.md` file with an updated listing of the directory's files and subdirectories.
5. **Logging and Metrics**: During the scan, the script logs events like README creation and file skipping to the terminal and/or the database. Once the scan is complete, it prints scan statistics to the terminal.

## **Logging**

The logging system tracks important events like file changes, README creations/updates, and errors. Logs are stored in the database, and some events are printed to the terminal. Adjust log levels via `log_config.py`.

## **Scan Statistics**

Once the scan completes, statistics are displayed in the terminal:
- Total files scanned
- Number of skipped files
- Number of README files created or updated
- Total time taken for the scan
- Average scan rate (files per second)

## **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Create a Pull Request

## **License**

This project is licensed under the MIT License. See the [LICENSE.md](LICENSE.md) file for more information.

---

This README covers all the key details needed for running, understanding, and contributing to the project. Let me know if you'd like to add or modify any sections!