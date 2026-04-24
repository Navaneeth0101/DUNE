import os
import sys
from ctypes import windll
import string
import magic

def unitconversion(x):
    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB"]
    for i in range(len(units)):
        if x < 1024:
            break
        x/=1024
    x = round(x,2)
    return str(x) + " " + units[i]

def get_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1
    return drives

def scan(location):
    if os.access(location, os.R_OK):
        if os.path.isfile(location):
            node = {"path": location, "size": os.path.getsize(location), "children": [], "isdir": False, "access": True}
            return node
        else:
            try:
                children = os.listdir(location)
            except:
                return {"path": location, "size": 0, "children": [], "isdir": True, "access": False}
            node = {"path": location, "children": [], "isdir": True, "access": True}
            dirsize = 0
            for i in children:
                child = scan(os.path.join(location, i))
                node["children"].append(child)
                dirsize += child["size"]
            node["size"] = dirsize
            return node
            
    else:
        return {"path": location, "size": 0, "children": [], "isdir": os.path.isdir(location), "access": False}

#schema for children
"""
{
    "path",
    "size",
    "children",
    "isdir",
    "access"
}
"""

def cleardisplay():
    print("\033[2J\033[1;1H")

def chkvalue(x):
    return x["size"]

def display(x):
    while True: 
        cleardisplay()
        if not (x["isdir"]):
            print("="*10)
            print(x["path"])
            print("="*10 + "\n\n")
            splitpath = os.path.split(x["path"])
            elementname = splitpath[-1] if splitpath[1] else splitpath[0][0]
            print("Name: "+elementname)
            try:
                print("Type:",magic.from_file(x["path"], mime=True))
                print("Details:",magic.from_file(x["path"]))
            except:
                print("Type: Error parsing")
                print("Details: Error parsing")
            input("press enter to go back..")
            return

        print("="*10)
        print(x["path"])
        print("="*10 + "\n\n")
        children = x["children"]
        children.sort(key= chkvalue, reverse= True)
        count = 1
        print("[0] [back] ...")
        max_len = 0
        max_num = len(str(len(children)))
        for child in children:
            name = os.path.basename(child["path"])
            if len(name) > max_len:
                max_len = len(name)
        for child in children:
            splitpath = os.path.split(child["path"])
            elementname = splitpath[-1] if splitpath[1] else splitpath[0][0]
            print(f"[{count:>{max_num}}] [{"D" if child["isdir"] else "F"}] {elementname:<{max_len}}         {unitconversion(child["size"]):>8} [{"ACCESSIBLE" if child["access"] else "INACCESSIBLE"}]" )
            count += 1
        print("="*10)
        while True:
            ch = input("enter index to open or q to quit: ").lower()
            if ch == "q":
                sys.exit()
            else:
                if ch.isdigit():
                    ch = int(ch)
                else:
                    print("invalid input.")
                    continue
            if ch < 0 or ch > len(children):
                print("invalid input.")
                continue
            else:
                break
        
        if ch == 0:
            return
        else:
            display(children[ch-1])


drives = get_drives()
while 1:
    cleardisplay()
    while 1:
        print("="*5+"SELECT DRIVE"+"="*5+"\n\n")
        for i in range(len(drives)):
            print(i+1,": ", drives[i],sep = "")
        print("\n\n"+"="*12)
        dskch = input("\nselect which one to scan or enter q to exit: ")
        if dskch == "q":
            sys.exit()
        else:
            if dskch.isdigit():
                dskch = int(dskch)
            else:
                sys.stderr.write("INVALID INPUT\n")
                continue
        if dskch <= len(drives) and dskch > 0:
            drive = drives[dskch - 1]
            break
        else:
            cleardisplay()
            sys.stderr.write("INVALID INPUT\n")
            continue
    drive = drive + ":\\"
    cleardisplay()
    print("scanning...")
    result = scan(drive)
    display(result)

