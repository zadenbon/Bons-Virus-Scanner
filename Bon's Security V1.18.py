import customtkinter as ctk
import tkinter.filedialog as fd

MIDNIGHT = "#0A192F"
NAVY_BLUE = "#112240"
ELECTRIC = "#64FFDA"
STEEL_BLUE = "#334455"

ctk.set_appearance_mode("dark")

class SentinelApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SENTINEL v2.0")
        self.geometry("700x600")
        self.configure(fg_color=MIDNIGHT)

        self.title_label = ctk.CTkLabel(
            self, 
            text="SENTINEL SECURITY", 
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
        self.output_box.insert("0.0", ">>> SYSTEM READY\n>>> WAITING FOR INPUT...")

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
        url = self.url_entry.get()
        if url:
            self.output_box.delete("0.0", "end")
            self.output_box.insert("end", f"[URL TARGET]: {url}\n")
            self.output_box.insert("end", "[*] ANALYSING LINK...")

    def run_logic(self):
        file_path = fd.askopenfilename()
        if file_path:
            self.output_box.delete("0.0", "end")
            self.output_box.insert("end", f"[FILE TARGET]: {file_path}\n")
            self.output_box.insert("end", "[*] UPLOADING HASH...")

if __name__ == "__main__":
    app = SentinelApp()
    app.mainloop()
