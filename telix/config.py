"""Filesystem locations used by the application."""

from __future__ import annotations

import os
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = PROJECT_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"


def _default_user_data_dir() -> Path:
    override = os.environ.get("TELIX_APPDATA_DIR")
    if override:
        return Path(override).expanduser().resolve()
    if os.name == "nt":
        local_app_data = os.environ.get("LOCALAPPDATA")
        if local_app_data:
            return Path(local_app_data).expanduser().resolve()
        return Path.home() / "AppData" / "Local"
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support"
    return Path.home() / ".local" / "share"


APP_DATA_DIR = _default_user_data_dir() / "Telix School Management System"
LOG_DIR = APP_DATA_DIR / "logs"
ISSUE_LOG_DIR = APP_DATA_DIR / "issue_log"
TELIX_LOG_FILE = LOG_DIR / "telix.log"

TELIX_ICON_PATH = IMAGES_DIR / "telix_image.ico"
TELIX_ICON_IMAGE_PATH = IMAGES_DIR / "telix_image.png"

STUDENT_FILE = PROJECT_DIR / "student_records.json"
TEACHER_FILE = PROJECT_DIR / "teacher_records.json"
ACADEMIC_FILE = PROJECT_DIR / "academic_records.json"
CLASS_FILE = PROJECT_DIR / "classes.json"
SUBJECT_FILE = PROJECT_DIR / "subjects.json"
ACADEMIC_YEAR_FILE = PROJECT_DIR / "academic_years.json"
TERM_FILE = PROJECT_DIR / "terms.json"
ENROLLMENT_FILE = PROJECT_DIR / "enrollments.json"
TEACHER_ASSIGNMENT_FILE = PROJECT_DIR / "teacher_assignments.json"
ATTENDANCE_FILE = PROJECT_DIR / "attendance_records.json"
PAYMENT_FILE = PROJECT_DIR / "payments.json"
EXPENSE_FILE = PROJECT_DIR / "expenses.json"
ASSESSMENT_FILE = PROJECT_DIR / "assessment_records.json"
GRADING_PROFILE_FILE = PROJECT_DIR / "grading_profiles.json"
USERS_FILE = PROJECT_DIR / "users.json"
