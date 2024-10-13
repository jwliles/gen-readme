### 1. **Subfolder Database Updates Only on Recursive Update**:

- **Description**: Subfolder databases should only be updated when the user explicitly initiates a **recursive update** using a CLI flag, such as `--recursive` or `-r`. By default, subfolder databases should not be updated, to maintain efficient runtime.

### 2. **Safe Mode for Preserving Databases**:

- **Description**: Add a CLI flag (`--safe` or `-sf`) that allows users to mark a database as "safe" from deletion. This will store the database path in `settings.json` so that even during a hard scan, the database will be preserved.

### 3. **CLI-Accessible Settings**:

- **Description**: Implement a `--config` flag, allowing users to view and modify the settings (e.g., manage safe databases, set a default folder). This would allow easier management of settings directly from the command line.

### 4. **Hard Scan**:

- **Description**: Implement a **hard scan** feature (triggered by `--hard`), which rehashes all files and regenerates README files without checking existing file hashes. It will also handle subfolder databases by removing them unless they are marked as safe.

### 5. **View Current Configuration**:

- **Description**: Implement a way to display the current `settings.json` via the `--config` flag, so users can view and manage their settings directly from the CLI.

### Proposed Incremental Steps:

1. **Implement Subfolder Database Updates on Recursive Update**:
   - Add the `--recursive` flag and ensure subfolder databases are only updated when explicitly requested.
2. **Implement Safe Mode**:

   - Add the `--safe` (`-sf`) flag and modify the script to support safe databases that cannot be deleted. Store these settings in `settings.json`.

3. **Implement CLI-Accessible Settings**:

   - Allow users to view and modify settings (such as marking databases as safe) from the CLI using the `--config` flag.

4. **Implement Hard Scan**:

   - Implement the `--hard` flag to trigger a full scan, regenerate README files, and rehash all files. This scan should also delete subfolder databases unless they are marked as safe.

5. **View Current Configuration**:
   - Implement a command to display the current configuration (`settings.json`) for users, allowing them to see the current state of safe databases and other settings.

### How would you like to proceed?

We can start with any of these steps, such as **adding the `--recursive` flag** to handle subfolder database updates first, and then move forward incrementally with the others. Let me know where you'd like to begin!
