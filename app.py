import tkinter as tk
from tkinter import ttk, messagebox
from modules import username_search
import threading

class BeatcodesApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("beatcodes")
        self.geometry("900x600")

        # Header
        title = tk.Label(
            self,
            text="beatcodes",
            fg="#4da6ff",
            font=("Segoe UI", 20, "bold"),
            cursor="hand2"
        )
        title.pack(pady=(10, 0))
        title.bind("<Button-1>", lambda e: self.open_link())

        link = tk.Label(
            self,
            text="guns.lol/beatcodes",
            fg="#1e90ff",
            cursor="hand2"
        )
        link.pack()
        link.bind("<Button-1>", lambda e: self.open_link())

        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=10)

        # Input frame
        input_frame = tk.Frame(self)
        input_frame.pack(fill="x", padx=20)

        tk.Label(input_frame, text="Username").grid(row=0, column=0, sticky="w")
        self.username_entry = tk.Entry(input_frame, width=40)
        self.username_entry.grid(row=1, column=0, padx=(0, 10))

        self.run_button = tk.Button(
            input_frame,
            text="Run Username Scan",
            command=self.run_scan
        )
        self.run_button.grid(row=1, column=1)

        info = tk.Label(
            input_frame,
            text="Tor routing is disabled on web deployments",
            fg="gray"
        )
        info.grid(row=0, column=1, sticky="e")

        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=10)

        # Results
        self.output = tk.Text(self, wrap="word", state="disabled")
        self.output.pack(expand=True, fill="both", padx=20, pady=10)

    def open_link(self):
        import webbrowser
        webbrowser.open("https://guns.lol/beatcodes")

    def log(self, text):
        self.output.configure(state="normal")
        self.output.insert("end", text + "\n")
        self.output.configure(state="disabled")
        self.output.see("end")

    def run_scan(self):
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showwarning("Missing Input", "Enter a username")
            return

        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.configure(state="disabled")

        threading.Thread(target=self.scan_worker, args=(username,), daemon=True).start()

    def scan_worker(self, username):
        self.log("Scanning...")
        try:
            results = username_search.find_socials(username, tor=False)
            if not results:
                self.log("No results found")
                return

            for site, data in results.items():
                self.log(f"\n{site} (confidence {data['weight']})")
                for url in sorted(set(data["urls"])):
                    self.log(f"  • {url}")

            self.log("\nScan complete")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            
if __name__ == "__main__":
    app = BeatcodesApp()
    app.mainloop()


