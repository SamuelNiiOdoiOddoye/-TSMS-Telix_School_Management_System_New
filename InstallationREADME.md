# TSMS Installation Guide

This guide covers the current **Telix School Management System V1** desktop application. It is a local Python/Tkinter application that stores data in local JSON files. It is not the planned hosted or multi-user V2 platform.

## 1. Requirements

- Python 3.10 or later. Python 3.13 is the current development baseline.
- Tkinter/ttk available in your Python installation.
- Git (recommended) or a downloaded ZIP of the repository.
- A writable folder for the project and its local data.

The current application has no third-party runtime dependencies. The `requirements.txt` file installs the local project. Optional developer tools (Ruff and mypy) are defined in `pyproject.toml`.

## 2. Get the source code

Clone the repository:

```bash
git clone https://github.com/SamuelNiiOdoiOddoye/-TSMS-Telix_School_Management_System_New.git
cd -TSMS-Telix_School_Management_System_New
```

Alternatively, use **Code → Download ZIP** on GitHub, extract the ZIP, and open a terminal in the extracted repository folder.

## 3. Create a virtual environment

### Windows (PowerShell)

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell blocks environment activation, you can run the environment's Python directly instead:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Linux

First ensure Python, venv support, pip, and Tkinter are installed. On Debian/Ubuntu-based distributions, these packages are commonly available as follows:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip python3-tk
```

Package names vary by distribution. Then, from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### macOS

Install a supported Python version (for example, from python.org), then from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If Tkinter is unavailable, install or repair a Python distribution that includes Tcl/Tk support. The exact fix depends on how Python was installed.

## 4. Verify Tkinter

Run:

```bash
python -m tkinter
```

A small Tkinter test window should open. Close it to continue. If Python reports that Tkinter is missing, resolve that operating-system/Python installation issue before launching TSMS.

## 5. Initialise the first administrator

From the repository root, run:

```bash
python -m telix.bootstrap_admin
```

Follow the prompts to create the initial local Super Admin account. Choose a strong password. The bootstrap command should not replace an existing Super Admin.

Do not use real student or staff information when testing the application. For disposable demonstration data, consult the demo-account instructions in the main README.

## 6. Launch TSMS

From the repository root, run either command:

```bash
python -m telix
```

or:

```bash
python main.py
```

Keep the project and its data files in a location where your user account has write permission. Until data-directory handling is fully validated across operating systems, launch the application from the repository root rather than an unrelated working directory.

## 7. Run the automated tests

```bash
python -m unittest discover -s tests -t .
```

To install the optional development tools used for linting, formatting, and static type checking:

```bash
python -m pip install -e ".[dev]"
```

Then run:

```bash
python -m ruff check .
python -m ruff format --check .
python -m mypy
```

Use the exact commands and configuration in the repository if the development workflow changes.

## 8. Troubleshooting

### `No module named tkinter`

Tkinter is missing from the active Python installation. Install the relevant Tk package for your Linux distribution or repair/install a Python distribution with Tcl/Tk support. Creating a virtual environment does not add a missing Tkinter system component.

### `No module named telix` or imports fail

Check that the terminal is in the repository root and that the virtual environment is activated. Re-run `python -m pip install -r requirements.txt` from that root.

### Permission or file-write errors

Move the project to a user-writable directory and check folder permissions. Do not run the app as administrator/root as a workaround unless a specific, understood system requirement calls for it.

### The application does not open a window

Confirm that you are using a desktop session with a graphical display, that Tkinter verification succeeds, and that the terminal shows no startup error.

## 9. Data and privacy warning

V1 is a local desktop application using JSON files. Do not use real school records until the application has been appropriately reviewed for your intended deployment and backup process. Keep data files and backups private. Never attach student records, passwords, or other sensitive information to a bug report.

## 10. Diagnostics and bug reports

Automatic diagnostic bundles, crash reports, and the proposed `issue_log` workflow are **not claimed to be implemented by this guide**. Their implementation requires changes to the application code and testing on supported operating systems.

Until that feature is implemented, when reporting a problem, include:
- Operating system and version.
- Python version (`python --version`).
- Steps that reproduce the problem.
- Expected result and actual result.
- The full error/traceback, after removing passwords, personal information, and school-record data.

Send the sanitised report to **samuel.oddoye@icloud.com**. Do not send the JSON data files.
