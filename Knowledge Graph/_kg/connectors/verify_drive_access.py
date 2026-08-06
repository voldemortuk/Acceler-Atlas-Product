#!/usr/bin/env python3
"""
Run this once after sharing a Drive folder with the service account, to confirm
the credential works and the folder is actually visible before wiring the daily
sync on top of it. Usage:

    .venv/bin/python verify_drive_access.py <folder_id_or_url>
"""
import os
import re
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
KEY_FILE = os.path.expanduser('~/.config/acceler-kg/drive-service-account.json')

def extract_folder_id(arg):
    m = re.search(r'/folders/([a-zA-Z0-9_-]+)', arg)
    return m.group(1) if m else arg

def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: verify_drive_access.py <folder_id_or_drive_url>")
    if not os.path.exists(KEY_FILE):
        raise SystemExit(
            f"Missing {KEY_FILE}\n"
            "Download the service account JSON key from Google Cloud Console "
            "and save it at that path first."
        )

    folder_id = extract_folder_id(sys.argv[1])
    creds = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
    print(f"Service account: {creds.service_account_email}")

    svc = build('drive', 'v3', credentials=creds)
    resp = svc.files().list(
        q=f"'{folder_id}' in parents and trashed = false",
        fields="files(id, name, mimeType, modifiedTime)",
        pageSize=50,
    ).execute()

    files = resp.get('files', [])
    if not files:
        print(
            "\nNo files visible in that folder.\n"
            f"Make sure the folder is shared with {creds.service_account_email} as Viewer, "
            "and that the folder ID is correct."
        )
        return

    print(f"\n{len(files)} file(s) visible:")
    for f in files:
        print(f"  - {f['name']}  ({f['mimeType']}, modified {f['modifiedTime']})")

if __name__ == '__main__':
    main()
