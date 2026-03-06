# Bon's Antivirus - Created by Zadenbon
# License: CC BY 4.0 - Credit must be given if shared or modified


import requests
import time
import os

API_KEY = "d090b626424dde0d6e1c9686bb99e79ead7383aafbfcada0dbd6425d44cdea7e"

def scan_url(url):
    print("Submitting URL to VirusTotal...")
    response = requests.post(
        "https://www.virustotal.com/api/v3/urls",
        headers={"x-apikey": API_KEY},
        data={"url": url}
    )
    result_id = response.json()["data"]["id"]
    print("Waiting for results...")
    time.sleep(5)
    analysis = requests.get(
        f"https://www.virustotal.com/api/v3/analyses/{result_id}",
        headers={"x-apikey": API_KEY}
    )
    stats = analysis.json()["data"]["attributes"]["stats"]
    malicious = stats["malicious"]
    harmless = stats["harmless"]
    print(f"\n--- Scan Results for URL ---")
    print(f"Malicious:  {malicious}")
    print(f"Harmless:   {harmless}")
    if malicious > 0:
        print("WARNING: This URL may be dangerous!")
    else:
        print("✅ URL looks safe!")

def scan_file(filepath):
    filepath = filepath.strip('"')
    print(f"Scanning file: {filepath}...")
    with open(filepath, "rb") as f:
        response = requests.post(
            "https://www.virustotal.com/api/v3/files",
            headers={"x-apikey": API_KEY},
            files={"file": f}
        )
    result_id = response.json()["data"]["id"]
    print("Waiting for results...")
    time.sleep(10)
    analysis = requests.get(
        f"https://www.virustotal.com/api/v3/analyses/{result_id}",
        headers={"x-apikey": API_KEY}
    )
    stats = analysis.json()["data"]["attributes"]["stats"]
    malicious = stats["malicious"]
    harmless = stats["harmless"]
    print(f"\n--- Scan Results for {os.path.basename(filepath)} ---")
    print(f"Malicious:  {malicious}")
    print(f"Harmless:   {harmless}")
    if malicious > 0:
        print("⚠️  WARNING: This file may be dangerous!")
    else:
        print("✅ File looks safe!")

def scan_folder(folderpath):
    folderpath = folderpath.strip('"')
    print(f"\nScanning all files in: {folderpath}")
    files = []
    for root, dirs, filenames in os.walk(folderpath):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    print(f"Found {len(files)} files to scan...\n")
    for filepath in files:
        scan_file(filepath)
        print("---")
        time.sleep(2)

print("=================================")
print("        Bon's Antivirus")
print("=================================")

choice = input("What do you want to scan?\n1. File\n2. URL\n3. Folder\nEnter 1, 2 or 3: ")

if choice == "1":
    path = input("Enter the full file path: ")
    path = path.strip('"')
    if os.path.exists(path):
        scan_file(path)
    else:
        print("File not found!")

elif choice == "2":
    url = input("Enter the URL to scan: ")
    scan_url(url)

elif choice == "3":
    folder = input("Enter the full folder path: ")
    folder = folder.strip('"')
    if os.path.exists(folder):
        scan_folder(folder)
    else:
        print("❌ Folder not found!")

else:
    print("Invalid choice!")
    
    input("\nPress Enter to exit...")
