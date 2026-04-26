# DUNE

**Disk Usage Navigator & Explorer**

A fast CLI utility for disk usage analysis, directory navigation, and file metadata inspection.

---

##  Features

* Recursive disk scanning
* Size-based sorting (largest first)
* Interactive directory navigation
* File metadata detection (via libmagic)
* Handles inaccessible files gracefully
* Lightweight and portable

---

##  Usage

###  Download

Download the latest release from the **Releases** section on GitHub.

---

###  Running from Source

#### Requirements

* Python 3.x
* `python-magic-bin`

Install dependency:

```bash
pip install python-magic-bin
```

#### Run

```bash
python dune.py
```

---

###  Navigation

* Enter number → open file/folder
* `0` → go back
* `q` → quit

---

##  Build

### Requirements

* PyInstaller

Install:

```bash
pip install pyinstaller
```

---

### Build Command

```bash
pyinstaller --onefile --console dune.py
```

The executable will be created inside the `dist/` folder.

---

##  Example

```
[ 1] [D] Windows                 25.66 GB  [ACCESSIBLE]
[ 2] [F] pagefile.sys             0 B      [INACCESSIBLE]
```

---

##  Notes

* Designed as an alternative to tools like `ncdu` for Windows
* Uses content-based file type detection using magic module instead of file extensions

---

##  License

MIT License

---

##  Credits

Built using Python and `python-magic`.
