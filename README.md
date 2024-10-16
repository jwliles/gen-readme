# go_readme

**go_readme** is a high-performance, concurrent tool written in Go for scanning directories, generating or updating `README.md` files, and tracking file changes. It efficiently handles large file systems, with support for skipping hidden files and concurrent processing of file metadata, making it ideal for large-scale projects.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Basic Usage](#basic-usage)
  - [CLI Options](#cli-options)
  - [Skipping Hidden Files](#skipping-hidden-files)
  - [Concurrency](#concurrency)
  - [Database Integration](#database-integration)
  - [Examples](#examples)
- [Code Breakdown](#code-breakdown)
- [Troubleshooting](#troubleshooting)
- [Testing and Benchmarks](#testing-and-benchmarks)
- [License](#license)

---

## Features

- **High-Performance File Scanning**: Utilizes Go's goroutines for concurrent file scanning and processing.
- **Directory Traversal**: Walks through directories, skipping hidden files and folders if specified.
- **README Generation**: Automatically generates or updates `README.md` files in every directory.
- **Database Support**: Tracks file metadata (hashes, modified times) in an SQLite database for change detection.
- **Customizable**: Allows the exclusion of hidden files, setting custom scanning depth, and more.

---

## Installation

To install **go_readme**, you'll need Go installed on your system.

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/go_readme.git
    cd go_readme
    ```

2. Install dependencies and build the project:
    ```bash
    go mod tidy
    go build -o go_readme .
    ```

3. Run the tool:
    ```bash
    ./go_readme --path /path/to/your/project
    ```

---

## Usage

### Basic Usage

To scan a directory and generate or update `README.md` files in every subdirectory:

```bash
./go_readme --path /path/to/your/project
```

This will scan the directory at `/path/to/your/project`, process the files, and either create or update `README.md` files.

### CLI Options

| Option          | Description                                               | Example                                                   |
| --------------- | --------------------------------------------------------- | --------------------------------------------------------- |
| `--path`        | The root directory to scan (default is `pwd`).            | `./go_readme --path /home/user/project`                   |
| `--skip-hidden` | Skip hidden files and directories.                        | `./go_readme --path /home/user/project --skip-hidden`     |
| `--max-workers` | Set the number of concurrent workers (default: 4).        | `./go_readme --max-workers 8`                             |
| `--db-path`     | Path to the SQLite database file (default: project root). | `./go_readme --db-path /home/user/project/file_hashes.db` |
| `--verbose`     | Enable verbose output for debugging.                      | `./go_readme --verbose`                                   |

---

### Skipping Hidden Files

By default, the program scans all files, including hidden files and directories. To skip hidden files and directories (e.g., files starting with a `.` on Unix systems), use the `--skip-hidden` flag.

```bash
./go_readme --path /path/to/your/project --skip-hidden
```

This will exclude any hidden files or folders from being processed or having `README.md` files generated.

### Concurrency

**go_readme** uses Go's concurrency features to speed up file scanning by leveraging multiple workers. You can control the number of workers by using the `--max-workers` option.

For example, to use 8 concurrent workers:

```bash
./go_readme --path /path/to/your/project --max-workers 8
```

This can be useful if you have a large directory structure and want to maximize CPU utilization.

### Database Integration

**go_readme** uses an SQLite database to track file metadata such as file paths, hashes, and modification times. The database allows the tool to detect changes in files since the last scan and only regenerate `README.md` files where necessary.

By default, the database is created in the root of the directory being scanned. You can specify a custom database path using the `--db-path` flag:

```bash
./go_readme --path /path/to/your/project --db-path /path/to/database/file_hashes.db
```

---

### Examples

#### 1. Basic File Scan:
```bash
./go_readme --path /home/user/project
```
This scans the `/home/user/project` directory, creates or updates `README.md` files, and tracks changes in an SQLite database.

#### 2. Skipping Hidden Files:
```bash
./go_readme --path /home/user/project --skip-hidden
```
Scans the directory but skips any hidden files and directories.

#### 3. Concurrent File Scanning with 8 Workers:
```bash
./go_readme --path /home/user/project --max-workers 8
```
Uses 8 concurrent workers to speed up file scanning.

#### 4. Custom Database Path:
```bash
./go_readme --path /home/user/project --db-path /home/user/project/file_hashes.db
```
Stores file metadata in a custom database file.

---

## Code Breakdown

The following is a breakdown of the key components of the project.

### 1. **Main Program (main.go)**

This is the entry point for the program. It parses command-line arguments, initializes the scan, and coordinates the creation or update of README files.

Key functions:
- `main()`: Handles argument parsing and initializes the scanning process.
- `walkDirectory()`: Recursively walks through directories, sending file paths to be processed via channels.
- `processFiles()`: Processes each file, generates metadata, and updates the database.

### 2. **File Scanning (scanner.go)**

Responsible for scanning directories and filtering out hidden files (if specified).

Key functions:
- `walkDirectory()`: Uses `filepath.WalkDir` to traverse directories while filtering hidden files.
- `isHidden()`: Checks if a file or directory is hidden by examining its name.

### 3. **README Generation (readme_generator.go)**

Handles the creation and updating of `README.md` files in each directory.

Key functions:
- `createReadme()`: Generates a `README.md` file based on the contents of the directory.
- `updateReadme()`: Updates an existing `README.md` file if there are changes to the directory.

### 4. **Database Management (database.go)**

Manages the SQLite database, tracking file metadata for change detection.

Key functions:
- `createDatabase()`: Initializes the SQLite database and creates necessary tables.
- `insertFileMetadata()`: Inserts or updates file metadata (file path, hash, modification time) into the database.
- `detectChanges()`: Compares the current state of files with the stored metadata to determine if updates are needed.

---

## Troubleshooting

### 1. **Slow Performance**

- **Solution**: Increase the number of concurrent workers with the `--max-workers` flag. For example, try setting `--max-workers 8` or higher to leverage multi-core CPUs more effectively.

### 2. **Database File Not Found**

- **Solution**: Ensure that the correct `--db-path` is specified. If no custom database path is provided, the database will be created in the root directory of the scanned project.

### 3. **README Files Not Updating**

- **Solution**: If `README.md` files are not being updated, ensure that files are actually being modified (i.e., their hashes or modification times are changing). If the files are unchanged, the tool will not regenerate the README.

### 4. **Hidden Files Being Scanned**

- **Solution**: Use the `--skip-hidden` flag to exclude hidden files and directories from being scanned or having `README.md` files generated.

---

## Testing and Benchmarks

### Unit Testing

Unit tests can be written using Go's standard testing framework. To run tests:

```bash
go test ./...
```

### Benchmarking

To benchmark the performance of the file scanning process, you can use Go's built-in benchmarking tools. Example:

```go
func BenchmarkWalkDirectory(b *testing.B) {
    for i := 0; i < b.N; i++ {
        walkDirectory("/path/to/test_directory")
    }
}
```

To run benchmarks:

```bash
go test -bench=.
```

This will give you insights into the performance of different components of the program.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.

---

With this README, users should be able to fully understand how to install, use, and troubleshoot **go_readme**, as well as contribute to or benchmark the project. Let me know if you need further adjustments!
