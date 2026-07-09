This repository, **FIM-File-Integrity-Manager-**, is a Python-based utility designed to monitor the integrity of a specific file by detecting unauthorized or accidental modifications. It implements a basic File Integrity Monitoring (FIM) system, which is a critical component in security auditing and change management.

The system works by calculating a cryptographic hash (SHA-256) of a target file and periodically re-calculating it to check for discrepancies. If the file's content changes, the script detects the mismatch and logs the event—including the previous hash, the new hash, and a timestamp—into a MySQL database for historical tracking. This provides a digital "paper trail" of file modifications.

## 1. How all main components connect

The architecture follows a classic "Monitor-and-Log" pattern. The core logic resides in `main_file.py`, which acts as the orchestrator. It consumes configuration data from `db_config.py` to establish a connection with a MySQL instance. The database schema, defined in `file_sql.sql`, must be initialized beforehand to provide the storage layer for change events.

The workflow operates in a continuous loop:
1.  **Initialization**: `main_file.py` calculates the baseline SHA-256 hash of the target file (currently configured as `info.txt`).
2.  **Monitoring**: The script enters an infinite loop, sleeping for 10 seconds between checks.
3.  **Detection**: It re-calculates the file hash. If the `current_hash` differs from the `initial_hash`, a change is identified.
4.  **Persistence**: The `db_change` function is invoked to insert a record into the `file_change` table in MySQL.
5.  **Update**: The baseline hash is updated to the new hash to prepare for the next monitoring cycle.


## 2. Repository Structure

```text
FIM-File-Integrity-Manager-/
├── db_config.py
├── file_sql.sql
├── info.txt
└── main_file.py
```


## 3. Other important information

### Tech Stack
*   **Language**: Python 3.x
*   **Database**: MySQL
*   **Libraries**: `hashlib` (standard library for SHA-256), `mysql-connector-python` (for database interaction), and `time` (for polling intervals).

### Key Implementation Details
*   **Hashing Algorithm**: The project uses **SHA-256** via the `hashlib` library in `main_file.py`. This ensures that even a single-bit change in the target file results in a completely different hash (the avalanche effect).
*   **Database Schema**: The table `file_change` in `file_sql.sql` is well-structured for auditing, capturing the `file_path`, a `timestamp`, `old_hash`, `new_hash`, and a `change_type` string.
*   **Polling Mechanism**: The system uses a synchronous polling approach with `time.sleep(10)`, checking for changes every 10 seconds.

### Setup and Configuration
1.  **Database Setup**: Execute the queries in `file_sql.sql` to create the `int_file` database and the `file_change` table.
2.  **Configuration**: Update `db_config.py` with your local MySQL credentials (host, user, and password).
3.  **Target File**: In `main_file.py`, the `file_name` variable is currently hardcoded to a specific Windows absolute path (`C:\\Users\\shrav\\...`). To use this in a different environment, this path must be updated to point to the file you wish to monitor, such as the provided `info.txt`.
4.  **Dependencies**: Ensure the MySQL connector is installed:
    ```bash
    pip install mysql-connector-python
    ```

This project serves as a foundational example of how security automation scripts interact with relational databases to maintain a stateful record of system changes.
