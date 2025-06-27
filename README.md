# Password Toolkit Ultra

A powerful Python toolkit for generating custom password wordlists and analyzing password strength, featuring an intuitive graphical interface.

---

## 🚀 Features

- **Password Strength Analyzer:**  
  Instantly analyze the strength of any password using the advanced [zxcvbn](https://github.com/dropbox/zxcvbn) algorithm.
- **Custom Wordlist Generator:**  
  Create huge, personalized password wordlists based on your own keywords, with leetspeak, suffixes, and combinations.
- **Downloadable Wordlists:**  
  Save your generated wordlists as `.txt` files for use with password recovery tools.
- **Modern GUI:**  
  User-friendly, stylish interface built with Tkinter.
- **No command line needed:**  
  Everything works from the graphical interface.

---

## 🖥️ Screenshots

### Password Analyzer
![Password Analyzer Screenshot](password_analyzer.png)

### Wordlist Generator
![Wordlist Generator Screenshot](wordlist_generator.png)

### Example Downloaded Wordlist (TXT)
![Sample Wordlist TXT Screenshot](wordlist_sample.png)

---

## 📦 Installation

1. **Clone or Download this repository**
    - Click the green `Code` button and choose `Download ZIP`, or use GitHub Desktop.

2. **Install Python 3.x**  
    - Download from [python.org](https://www.python.org/downloads/).

3. **Install dependencies**
    - Open a terminal/command prompt in the project folder and run:
      ```
      pip install -r requirements.txt
      ```
    - Example `requirements.txt`:
      ```
      zxcvbn
      ```

---

## 🛠️ Usage

### Launch the GUI



### Password Analysis

- Go to the **Password Analysis** tab.
- Enter your password and click **Analyze Strength**.
- View the strength meter, estimated crack time, and suggestions.

### Wordlist Generator

- Go to the **Wordlist Generator** tab.
- Enter your keywords (comma-separated).
- Click **Show Suggestions** to view the top 10 wordlist entries.
- Click **Download Full List** to save the complete wordlist as a `.txt` file.

---

---

## 💡 Example

**Generate a wordlist:**
### python password_analyzer.py generate "john,doe,2024" --output mywordlist.txt

**Analyze a password:**

---

## ❓ FAQ

**Q: Can I use this wordlist with tools like John the Ripper or Hashcat?**  
A: Yes! The generated `.txt` files are compatible with all standard password cracking tools.

**Q: Is my data stored anywhere?**  
A: No, everything runs locally on your computer and nothing is sent over the internet.

**Q: Can I add more leetspeak rules or suffixes?**  
A: Yes! Edit `wordlist_generator.py` to customize leet mappings or suffixes.

---

## 🤝 Contributing

Pull requests, bug reports, and feature suggestions are welcome!  
Feel free to fork this repo and submit improvements.

---

## 📄 License

MIT License

---

## 👤 Author

Mohit Kumar  


---



