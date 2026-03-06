import customtkinter as ctk
import tkinter.filedialog as fd
import requests
import base64
import time
import hashlib

API_KEY = "508674518b766a94b85949786eabad3496c28b93d8f55cc289384fcee2143dcb"

MIDNIGHT = "#0A192F"
NAVY_BLUE = "#112240"
ELECTRIC = "#64FFDA"
STEEL_BLUE = "#334455"

ctk.set_appearance_mode("dark")

class SentinelApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("BON'S SECURITY V1.18")
        self.geometry("700x600")
        self.configure(fg_color=MIDNIGHT)

        self.title_label = ctk.CTkLabel(
            self, 
            text="BON'S SECURITY V1.18", 
            font=("Impact", 36), 
            text_color=ELECTRIC
        )
        self.title_label.pack(pady=(30, 10))

        self.output_box = ctk.CTkTextbox(
            self, 
            width=600, 
            height=200, 
            corner_radius=15,
            border_width=2,
            border_color=ELECTRIC,
            fg_color=NAVY_BLUE,
            text_color="white",
            font=("Consolas", 13)
        )
        self.output_box.pack(pady=10)
        self.output_box.insert("0.0", ">>> SYSTEM READY\n>>> ENTER URL OR SELECT FILE")

        self.url_entry = ctk.CTkEntry(
            self, 
            width=400, 
            placeholder_text="Paste URL here...",
            fg_color=NAVY_BLUE,
            border_color=ELECTRIC
        )
        self.url_entry.pack(pady=10)

        self.url_btn = ctk.CTkButton(
            self, 
            text="SCAN URL", 
            font=("Arial", 14, "bold"),
            fg_color=ELECTRIC,
            text_color=MIDNIGHT,
            hover_color="#45c7ab",
            command=self.run_url_logic
        )
        self.url_btn.pack(pady=5)

        self.scan_btn = ctk.CTkButton(
            self, 
            text="LAUNCH FILE SCAN", 
            font=("Arial", 14, "bold"),
            corner_radius=10, 
            fg_color=ELECTRIC,
            text_color=MIDNIGHT, 
            hover_color="#45c7ab",
            height=40,
            width=220,
            command=self.run_logic
        )
        self.scan_btn.pack(pady=20)

        self.version_label = ctk.CTkLabel(
            self, 
            text="CORE v2.0.4 | DATABASE: VIRUSTOTAL", 
            font=("Arial", 10),
            text_color=STEEL_BLUE
        )
        self.version_label.pack(side="bottom", pady=10)

    def run_url_logic(self):
        url_to_scan = self.url_entry.get()
        if not url_to_scan: return
        self.output_box.delete("0.0", "end")
        self.output_box.insert("end", f">>> TARGET URL: {url_to_scan}\n>>> STATUS: SCANNING... (12s HOLD)\n")
        self.update()
        time.sleep(12)
        try:
            url_id = base64.urlsafe_b64encode(url_to_scan.encode()).decode().strip("=")
            api_url = f"https://www.virustotal.com/{url_id}"
            headers = {"x-apikey": API_KEY}
            response = requests.get(api_url, headers=headers)
            if response.status_code == 404:
                self.output_box.insert("end", "\n[!] NEW URL. SUBMITTING...")
                requests.post("https://www.virustotal.com", data={"url": url_to_scan}, headers=headers)
                self.output_box.insert("end", "\n[+] SUBMITTED. RE-SCAN IN 1 MINUTE.")
                return
            data = response.json()
            if response.status_code == 200:
                stats = data['data']['attributes']['last_analysis_stats']
                self.output_box.insert("end", f"\n[+] ANALYSIS COMPLETE")
                self.output_box.insert("end", f"\n[!] MALICIOUS: {stats['malicious']}")
                self.output_box.insert("end", f"\n[+] HARMLESS: {stats['harmless']}")
            else:
                self.output_box.insert("end", f"\n[API ERROR]: {data['error']['message']}")
        except Exception as e:
            self.output_box.insert("end", f"\n[SYSTEM ERROR]: {str(e)}")

    def run_logic(self):
        file_path = fd.askopenfilename()
        if not file_path: return
        self.output_box.delete("0.0", "end")
        self.output_box.insert("end", f">>> TARGET FILE: {file_path}\n>>> STATUS: SCANNING... (12s HOLD)\n")
        self.update()
        time.sleep(12)
        try:
            with open(file_path, "rb") as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            api_url = f"https://www.virustotal.com{file_hash}"
            headers = {"x-apikey": API_KEY}
            response = requests.get(api_url, headers=headers)
            data = response.json()
            if response.status_code == 200:
                stats = data['data']['attributes']['last_analysis_stats']
                self.output_box.insert("end", f"\n[+] ANALYSIS COMPLETE")
                self.output_box.insert("end", f"\n[!] MALICIOUS: {stats['malicious']}")
                self.output_box.insert("end", f"\n[+] HARMLESS: {stats['harmless']}")
            else:
                self.output_box.insert("end", f"\n[API ERROR]: {data['error']['message']}")
        except Exception as e:
            self.output_box.insert("end", f"\n[SYSTEM ERROR]: {str(e)}")

if __name__ == "__main__":
    app = SentinelApp()
    app.mainloop()
