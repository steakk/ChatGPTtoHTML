# ChatGPT To HTML

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## 📌 Overview

`ChatGPT_To_HTML.py` is a **Python script** that converts **ChatGPT conversation data (`conversations.json`) into an organized, searchable, and structured HTML format**. The script generates:  

- A **main `conversations.html`** file with a sidebar navigation menu  
- **Individual weekly conversation files** (`conversations_YYYY_W##.html`)  
- **Properly formatted user & assistant messages**  
- **Collapsible sidebar sections** for easy browsing  

This allows you to **quickly search, navigate, and reference** past ChatGPT conversations.

---

## 📥 Installation

### **🔹 Prerequisites**
Ensure you have **Python 3.6+** installed. You can download it here:  
👉 [https://www.python.org/downloads/](https://www.python.org/downloads/)

### **🔹 Clone the Repository**
```sh
git clone https://github.com/yourusername/ChatGPT-To-HTML.git
cd ChatGPT-To-HTML
```

### **🔹 Install Dependencies**
The script uses the **`pytz`** library for timezone conversions. Install it via:
```sh
pip install pytz
```

---

## 🚀 Usage

### **🔹 Step 1: Place Your ChatGPT Conversations File**
Ensure your **ChatGPT conversation export (`conversations.json`)** is in the same directory as `ChatGPT_To_HTML.py`.

### **🔹 Step 2: Run the Script**
```sh
python ChatGPT_To_HTML.py
```

### **🔹 Step 3: Open the Generated HTML Files**
1. Navigate to the `output/` folder.
2. Open `conversations.html` in your web browser.
3. Use the sidebar to **search, expand, and browse** your ChatGPT conversations.

---

## 📂 Output Structure

| File | Description |
|------|------------|
| `output/conversations.html` | Main page with sidebar navigation |
| `output/conversations_YYYY_W##.html` | Individual weekly conversation files |
| `style.css` | Stylesheet for formatting |
| `script.js` | JavaScript for interactivity |

---

## 🎯 Features

✅ **Organized by Year & Week** – Conversations are sorted **by week**, with the most recent weeks **at the top**  
✅ **Fully Searchable** – Search bar lets you find conversations quickly  
✅ **Expandable Sidebar** – Collapse or expand sections for a clean view  
✅ **Properly Formatted Messages** – Preserves line breaks & structure  
✅ **Standalone HTML Files** – No need for external databases or APIs  

---

## 🛠 How It Works

1. **Reads `conversations.json`**  
   - Extracts **title, timestamps, and messages**  
   - Groups conversations by **Year → Week**  

2. **Formats the Data**  
   - Converts timestamps to **America/Chicago timezone**  
   - Groups consecutive messages from the same user together  
   - Escapes special characters to **preserve formatting**  

3. **Generates Static HTML Files**  
   - Creates a **main `conversations.html`** file with sidebar navigation  
   - Generates **individual weekly files** to keep things lightweight  
   - Saves output in the `output/` folder  

---

## 📚 Documentation & Links

- **Python:** [https://www.python.org/](https://www.python.org/)
- **GitHub Flavored Markdown:** [https://github.github.com/gfm/](https://github.github.com/gfm/)
- **pytz Library:** [https://pypi.org/project/pytz/](https://pypi.org/project/pytz/)
- **ChatGPT:** [https://openai.com/chatgpt](https://openai.com/chatgpt)

---

## 📜 License

This project is licensed under the **MIT License**. See the [`LICENSE`](LICENSE) file for details.

---

## 👨‍💻 Contributing

Feel free to **submit issues, fork the repository, or suggest enhancements!**  

Pull requests are welcome. Please follow the contribution guidelines and format your code properly.

---

## ⭐ Like This Project?

If you found this useful, **give it a star ⭐ on GitHub!** 😊
