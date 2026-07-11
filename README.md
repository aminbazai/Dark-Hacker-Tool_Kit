# Dark-Hacker-Tool_Kit<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:FF0000,25:8B00FF,50:00F0FF,75:00FF41,100:FF0000&height=230&section=header&text=DARK%20HACKER&fontSize=60&animation=twinkling&fontAlignY=35&desc=How%20To%20Use%20-%20Complete%20Setup%20Guide&descAlignY=58&descSize=19&fontColor=00FF41" width="100%"/>

<a href="https://git.io/typing-svg">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=24&duration=2500&pause=700&color=FF2E63,00FF41,00F0FF,FF0000&center=true&vCenter=true&width=800&lines=%F0%9F%93%98+Step-by-Step+Installation+Guide;%F0%9F%AA%9F+Works+on+Windows+%26+Linux;%E2%9A%A1+Get+Running+in+Under+5+Minutes" alt="Typing SVG" />
</a>

<br/>

<img src="https://img.shields.io/badge/Windows-Supported-00F0FF?style=for-the-badge&logo=windows&logoColor=white&labelColor=000000"/>
<img src="https://img.shields.io/badge/Linux-Supported-00FF41?style=for-the-badge&logo=linux&logoColor=white&labelColor=000000"/>
<img src="https://img.shields.io/badge/Python-3.8%2B-FF2E63?style=for-the-badge&logo=python&logoColor=white&labelColor=000000"/>

<br/><br/>

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="450">

<br/>

![Divider](https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif)

</div>

## ✅ Prerequisites (Both OS)

<img src="https://img.shields.io/badge/-📋%20REQUIREMENTS-000000?style=flat-square&color=8B00FF"/>

- Python **3.8 or higher** installed
- `dark_hacker.py` and `requirements.txt` saved in the **same folder**

Check your Python version:

```bash
python --version
```
(On Linux, sometimes it's `python3 --version`)

<br/>

## <img src="https://cdn.simpleicons.org/windows/00F0FF" width="28"/> WINDOWS — Step by Step

<img src="https://img.shields.io/badge/-🪟%20WINDOWS%20SETUP-000000?style=flat-square&color=00F0FF"/>

### 1️⃣ Install Python (if not already installed)
Download from [python.org](https://python.org) → during setup, **check the box "Add Python to PATH"**.

### 2️⃣ Open Command Prompt (CMD)
Press `Win + R`, type `cmd`, hit Enter.

### 3️⃣ Go to the folder where your files are saved
```cmd
cd C:\Users\YourName\Downloads
```
👉 Replace with your actual folder path. If unsure where the files are, run:
```cmd
dir /s /b dark_hacker.py
```

### 4️⃣ Install required libraries
```cmd
python -m pip install -r requirements.txt
```

### 5️⃣ Run the toolkit
```cmd
python dark_hacker.py
```

### 6️⃣ Use the menu
Type the number of the tool you want (e.g. `1` for Password Strength Checker) and press Enter.

> ⚠️ Some tools (Firewall Checker, System Hardening Audit) need **Administrator** rights:
> Right-click CMD → **"Run as administrator"** → repeat step 3 & 5.

<br/>

![Divider](https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif)

## <img src="https://cdn.simpleicons.org/linux/00FF41" width="28"/> LINUX — Step by Step

<img src="https://img.shields.io/badge/-🐧%20LINUX%20SETUP-000000?style=flat-square&color=00FF41"/>

### 1️⃣ Check/Install Python
Most distros have Python pre-installed. If not:
```bash
sudo apt update && sudo apt install python3 python3-pip -y
```

### 2️⃣ Open Terminal and go to the folder
```bash
cd ~/Downloads
```
👉 Replace with the actual folder where you saved the files.

### 3️⃣ Install required libraries
```bash
pip3 install -r requirements.txt --break-system-packages
```
(If that flag isn't needed on your system, just use `pip3 install -r requirements.txt`)

### 4️⃣ Run the toolkit
```bash
python3 dark_hacker.py
```

### 5️⃣ Use the menu
Type the number of the tool you want and press Enter.

> ⚠️ Some tools (Firewall Checker, Hardening Audit, Persistence Checker) need **root/sudo** access to see full system info:
> ```bash
> sudo python3 dark_hacker.py
> ```

<br/>

![Divider](https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif)

## 🧯 Common Errors & Fixes

<img src="https://img.shields.io/badge/-🧯%20TROUBLESHOOTING-000000?style=flat-square&color=FF0000"/>

| Error | Fix |
|---|---|
| `python is not recognized` | Reinstall Python and check "Add to PATH" (Windows) |
| `Could not open requirements file` | You're in the wrong folder — `cd` to where the file actually is |
| `ModuleNotFoundError: No module named 'cryptography'` | Run the pip install command again |
| `Permission denied` (Linux firewall/hardening tools) | Run with `sudo python3 dark_hacker.py` |
| `pip is not recognized` | Use `python -m pip install ...` instead |

<br/>

## 📋 Quick Reference Card

<img src="https://img.shields.io/badge/-📋%20QUICK%20REFERENCE-000000?style=flat-square&color=8B00FF"/>

| Task | Windows | Linux |
|---|---|---|
| Check Python | `python --version` | `python3 --version` |
| Install deps | `python -m pip install -r requirements.txt` | `pip3 install -r requirements.txt` |
| Run tool | `python dark_hacker.py` | `python3 dark_hacker.py` |
| Run as admin/root | Right-click CMD → Run as Administrator | `sudo python3 dark_hacker.py` |

<br/>

## ⚖️ Legal Reminder

<div align="center">
<img src="https://img.shields.io/badge/⚠️-For%20Educational%20%26%20Authorized%20Use%20Only-FF0000?style=for-the-badge&labelColor=000000"/>
</div>

Only use this toolkit on systems, networks, or files **you own** or have **explicit written permission** to test. It's built for **learning and authorized security work only**.

<br/>

<div align="center">

<img src="https://user-images.githubusercontent.com/74038190/213866269-5d00981c-7c98-46d7-8a8e-16f462f15227.gif" width="350">

<br/>

<img src="https://img.shields.io/badge/DARK-HACKER-000000?style=for-the-badge&labelColor=FF0000&color=00FF41"/>

<br/><br/>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:FF0000,25:8B00FF,50:00F0FF,75:00FF41,100:FF0000&height=120&section=footer"/>

</div>
