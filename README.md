<div align="center">

# Noxu

### A lightweight system utility for global audio control via custom hotkeys.

[![Python](https://img.shields.io/badge/Python-3.5+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows_|_Linux-0078D6?style=for-the-badge&logo=windows&logoColor=white)]()
[![CPU](https://img.shields.io/badge/CPU_Usage-<1%25-brightgreen?style=for-the-badge)]()

</div>

---

## 📌 Overview

Noxu is a lightweight desktop utility that enables instant, global audio control across all active applications through a single configurable hotkey (`Shift+A` by default). Rather than manually adjusting volume application by application, Noxu hooks into the Windows/Linux audio session API to control all audio sources simultaneously.

The core challenge was achieving zero-latency response while maintaining minimal system impact — solved through optimized multithreaded background processing that keeps CPU utilization consistently below 1%.

---

## ✨ Features

| Feature | Description |
|---|---|
| ⌨️ **Global Hotkey** | `Shift+A` instantly mutes/unmutes all active applications system-wide |
| 🧵 **Multithreaded** | Background listener runs on a separate thread — no UI blocking |
| ⚡ **Zero Latency** | Sub-millisecond response time from keypress to audio change |
| 🪶 **Minimal Footprint** | Sub-1% CPU utilization, 50MB RAM, 15MB install |
| 🚀 **Startup Support** | Configurable to run automatically on system boot |
| 🖥️ **Cross-Platform** | Supports Windows 10/11 and Linux |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.5+ | Core application (~211 lines) |
| pycaw | Windows Core Audio API integration |
| keyboard | Global hotkey listener |
| threading | Multithreaded background process |

**Key Engineering:** The hotkey listener runs as a daemon thread entirely decoupled from the main process, ensuring zero UI impact. Audio session enumeration is cached on startup to minimize per-keypress latency.

---

## 🚀 Getting Started

### Prerequisites
- Windows 10/11 or Linux
- 15 MB disk space, 50 MB RAM

### Installation

```bash
# 1. Download and extract the ZIP
# 2. Ensure the assets/ folder is in the same directory as Noxu.exe
# 3. Run the executable
Noxu.exe
```

### Optional: Run on Startup
To have Noxu launch automatically on boot, add it to your startup folder. See [this guide](https://www.howtogeek.com/208224/how-to-add-programs-files-and-folders-to-system-startup-in-windows-8.1/) for Windows setup.

---

## 📁 Project Structure

```
Noxu/
├── assets/     # UI assets and icons
├── source/     # Python source code (~211 lines)
└── Noxu.exe    # Compiled executable
```

---

## ⌨️ Default Hotkey

| Hotkey | Action |
|---|---|
| `Shift + A` | Toggle mute/unmute all applications |

---

## 👤 Author

**Riyon Praveen** — Computer Science Student, University of South Florida

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](https://linkedin.com/in/riyonpraveen)
[![GitHub](https://img.shields.io/badge/GitHub-riyonp23-181717?style=flat&logo=github)](https://github.com/riyonp23)
