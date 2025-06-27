import argparse
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from zxcvbn import zxcvbn
from wordlist_generator import WordlistGenerator

def round_rectangle(canvas, x1, y1, x2, y2, radius=28, **kwargs):
    points = [
        x1+radius, y1,
        x2-radius, y1,
        x2, y1,
        x2, y1+radius,
        x2, y2-radius,
        x2, y2,
        x2-radius, y2,
        x1+radius, y2,
        x1, y2,
        x1, y2-radius,
        x1, y1+radius,
        x1, y1
    ]
    return canvas.create_polygon(points, **kwargs, smooth=True)

class PasswordAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Toolkit Ultra")
        self.root.geometry("750x600")
        self.root.configure(bg="#d9edff")  # Light blue background

        # --- Title Banner ---
        self.title_label = ttk.Label(
            self.root,
            text="Password Toolkit Ultra",
            font=("Segoe UI", 22, "bold italic"),
            background="#d9edff",
            foreground="#1c3f76"
        )
        self.title_label.place(relx=0.5, y=18, anchor="n")

        # --- Divider ---
        self.divider = ttk.Separator(self.root, orient='horizontal')
        self.divider.place(relx=0.06, rely=0.13, relwidth=0.88)

        # --- Custom Style ---
        style = ttk.Style()
        style.theme_use("clam")

        # Default tab style (normal)
        style.configure("TNotebook.Tab",
                        background="#b8d9ff",
                        foreground="#1c3f76",
                        font=("Segoe UI", 13, "italic"),
                        padding=[16, 8])

        # Highlight active tab: just a little taller/bolder
        style.map("TNotebook.Tab",
                  background=[("selected", "#4a86e8")],
                  foreground=[("selected", "white")],
                  font=[("selected", ("Segoe UI", 14, "bold italic"))],
                  padding=[("selected", [20, 12])])  # Just a little more than normal

        style.configure("TNotebook", background="#d9edff", borderwidth=0)
        style.configure("TFrame", background="#d9edff")
        style.configure("TLabel", background="#d9edff", foreground="#1c3f76", font=("Segoe UI", 13, "italic"))
        style.configure("Accent.TButton",
                        background="#4a86e8",
                        foreground="#ffffff",
                        font=("Segoe UI", 13, "italic"),
                        borderwidth=0,
                        focusthickness=3,
                        focuscolor="#1b4965",
                        padding=[14, 8])
        style.map("Accent.TButton",
                  background=[("active", "#1c4587")],
                  foreground=[("active", "#ffffff")])

        # --- Main Notebook ---
        self.notebook = ttk.Notebook(root)
        self.tab_analyze = ttk.Frame(self.notebook)
        self.tab_generate = ttk.Frame(self.notebook)
        self.setup_analysis_tab()
        self.setup_generator_tab()
        self.notebook.add(self.tab_analyze, text="🔒 Password Analysis")
        self.notebook.add(self.tab_generate, text="📝 Wordlist Generator")
        self.notebook.pack(expand=True, fill="both", padx=20, pady=20)

    def setup_analysis_tab(self):
        frame = ttk.Frame(self.tab_analyze, padding=15, style="TFrame")
        frame.pack(expand=True, fill="both")

        # Question label
        question_label = ttk.Label(
            frame,
            text="Is your password strong enough?",
            font=("Segoe UI", 17, "bold italic"),
            background="#d9edff",
            foreground="#1c3f76"
        )
        question_label.pack(pady=(5, 10))

        # Password entry
        entry_frame = ttk.Frame(frame, style="TFrame")
        entry_frame.pack(fill="x", padx=30, pady=(0, 10))
        ttk.Label(
            entry_frame,
            text="Enter Password:",
            font=("Segoe UI", 13, "italic"),
            background="#d9edff",
            foreground="#1c3f76"
        ).pack(side="left", padx=(0, 10))
        self.entry_password = ttk.Entry(entry_frame, width=30, font=("Segoe UI", 13, "italic"))
        self.entry_password.pack(side="left", expand=True, fill="x", ipady=4)

        btn_analyze = ttk.Button(
            frame,
            text="Analyze Strength",
            style="Accent.TButton",
            command=self.analyze
        )
        btn_analyze.pack(pady=10)

        # --- Split Results Area ---
        canvas_width = 900
        canvas_height = 300
        results_canvas = tk.Canvas(frame, width=canvas_width, height=canvas_height, bg="#d9edff", highlightthickness=0)
        results_canvas.pack(pady=10)

        # Draw two larger rounded rectangles side by side with more space and padding
        left_rect_coords = (15, 15, 450, 285)
        right_rect_coords = (470, 15, 885, 285)
        self.left_rect = round_rectangle(results_canvas, *left_rect_coords, radius=28, fill="#e6f2ff", outline="#b8d9ff", width=2)
        self.right_rect = round_rectangle(results_canvas, *right_rect_coords, radius=28, fill="#e6f2ff", outline="#b8d9ff", width=2)

        # Draw bar graph for strength (initially 0)
        self.strength_bars = []
        self.bar_labels = []
        self._draw_strength_graph(results_canvas, 0, left_rect_coords)

        # Place a frame on top of the right rectangle for results
        self.result_frame = tk.Frame(results_canvas, bg="#e6f2ff")
        self.result_window = results_canvas.create_window(
            right_rect_coords[0]+20, right_rect_coords[1]+20, anchor="nw",
            window=self.result_frame, width=right_rect_coords[2]-right_rect_coords[0]-40, height=right_rect_coords[3]-right_rect_coords[1]-40
        )

        self.result_header = tk.Label(
            self.result_frame,
            text="Analysis Results",
            font=("Segoe UI", 15, "bold italic"),
            bg="#e6f2ff",
            fg="#1c3f76"
        )
        self.result_header.pack(pady=(2, 8), anchor="w")

        self.result_text = tk.Text(
            self.result_frame,
            height=12,  # Increased height
            width=45,   # Increased width
            font=("Segoe UI", 12, "italic"),
            bg="#e6f2ff",
            fg="#1c3f76",
            bd=0,
            relief="flat",
            wrap="word",
            padx=8,
            pady=5
        )
        self.result_text.pack(fill="both", expand=True, padx=2, pady=2)
        self.result_text.config(state=tk.DISABLED)

        self.results_canvas = results_canvas
        self.left_rect_coords = left_rect_coords

    def _draw_strength_graph(self, canvas, score, rect_coords):
        # Remove old bars/labels if any
        for bar in getattr(self, "strength_bars", []):
            canvas.delete(bar)
        for label in getattr(self, "bar_labels", []):
            canvas.delete(label)
        self.strength_bars = []
        self.bar_labels = []

        # Bar colors from red to green
        colors = ["#a10000", "#ff6d6d", "#8be28b", "#009900"]
        labels = ["1", "2", "3", "4"]
        bar_width = 48
        spacing = 28
        # Place bars with plenty of padding inside the left rectangle
        base_x = rect_coords[0] + 50
        base_y = rect_coords[3] - 30
        max_height = rect_coords[3] - rect_coords[1] - 70

        for i in range(4):
            bar_height = int((i+1) / 4 * max_height)
            fill = colors[i] if i <= score else "#c0c0c0"
            bar = canvas.create_rectangle(
                base_x + i*(bar_width+spacing), base_y-bar_height,
                base_x + (i+1)*bar_width + i*spacing, base_y,
                fill=fill, outline="#b8d9ff", width=2
            )
            self.strength_bars.append(bar)
            label = canvas.create_text(
                base_x + i*(bar_width+spacing) + bar_width//2, base_y+18,
                text=labels[i], font=("Segoe UI", 13, "bold"), fill="#1c3f76"
            )
            self.bar_labels.append(label)

    def analyze(self):
        password = self.entry_password.get()
        if not password:
            messagebox.showerror("Error", "Please enter a password")
            self._draw_strength_graph(self.results_canvas, 0, self.left_rect_coords)
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)
            self.result_text.config(state=tk.DISABLED)
            return

        result = zxcvbn(password)
        score = result['score']
        # Ensure score is always between 0 and 3 (so displayed as 1-4)
        score = max(0, min(score, 3))

        # Update bar graph
        self._draw_strength_graph(self.results_canvas, score, self.left_rect_coords)

        # Update results (score+1 so display is 1-4, not 0-3)
        feedback = (
            f"Password Strength: {score+1}/4\n"
            f"Estimated Crack Time: {result['crack_times_display']['offline_slow_hashing_1e4_per_second']}\n\n"
            "Suggestions:\n" + "\n".join(result['feedback']['suggestions'])
        )
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, feedback)
        self.result_text.config(state=tk.DISABLED)

    def setup_generator_tab(self):
        frame = ttk.Frame(self.tab_generate, padding=25, style="TFrame")
        frame.pack(expand=True, fill="both")

        # Question label
        question_label = ttk.Label(
            frame,
            text="Ready to create your custom wordlist?",
            font=("Segoe UI", 17, "bold italic"),
            background="#d9edff",
            foreground="#1c3f76"
        )
        question_label.pack(pady=(10, 20))

        # Keywords entry
        entry_frame = ttk.Frame(frame, style="TFrame")
        entry_frame.pack(fill="x", padx=30, pady=(0, 15))
        ttk.Label(
            entry_frame,
            text="Enter keywords:",
            font=("Segoe UI", 13, "italic"),
            background="#d9edff",
            foreground="#1c3f76"
        ).pack(side="left", padx=(0, 10))
        self.entry_keywords = ttk.Entry(entry_frame, width=30, font=("Segoe UI", 13, "italic"))
        self.entry_keywords.pack(side="left", expand=True, fill="x", ipady=4)

        btn_generate = ttk.Button(
            frame,
            text="Generate Wordlist",
            style="Accent.TButton",
            command=self.generate_wordlist
        )
        btn_generate.pack(pady=15)

    def generate_wordlist(self):
        keywords = self.entry_keywords.get()
        if not keywords:
            messagebox.showerror("Error", "Please enter keywords")
            return

        user_inputs = [kw.strip() for kw in keywords.split(",")]
        generator = WordlistGenerator(user_inputs)
        wordlist = generator.generate()
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )
        if filepath:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("\n".join(wordlist))
            messagebox.showinfo("Success", f"Generated {len(wordlist)} words!\nSaved to:\n{filepath}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Password Strength Analyzer and Wordlist Generator")
    subparsers = parser.add_subparsers(dest="command")
    analyze_parser = subparsers.add_parser("analyze")
    analyze_parser.add_argument("password", help="Password to analyze")
    generate_parser = subparsers.add_parser("generate")
    generate_parser.add_argument("keywords", help="Comma-separated keywords")
    generate_parser.add_argument("--output", required=True, help="Output file path")
    args = parser.parse_args()
    if args.command == "analyze":
        result = zxcvbn(args.password)
        print(f"Strength: {result['score']}/4")
        print("Suggestions:")
        for suggestion in result['feedback']['suggestions']:
            print(f"- {suggestion}")
    elif args.command == "generate":
        generator = WordlistGenerator([kw.strip() for kw in args.keywords.split(",")])
        with open(args.output, "w", encoding="utf-8") as f:
            f.write("\n".join(generator.generate()))
        print(f"Wordlist saved to {args.output}")
    else:
        root = tk.Tk()
        app = PasswordAnalyzerApp(root)
        root.mainloop()
