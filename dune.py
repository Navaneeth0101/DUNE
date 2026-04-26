import os
import sys
from ctypes import windll
import string
import magic

class Node:
    __slots__ = ("name", "size", "children", "isdir", "access")

    def __init__(self, name, size, children, isdir, access):
        self.name = name
        self.size = size
        self.children = children
        self.isdir = isdir
        self.access = access

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
            #node = ("path": location, "children": [], "isdir": True, "access": True)
            splitpath = os.path.split(location)
            elementname = splitpath[-1] if splitpath[1] else splitpath[0][0]
            node = Node(elementname, 0, [], True, True)
            dirsize = 0
            try:
                with os.scandir(location) as children:
                    for child in children:
                        if child.is_file():
                            #childnode = {"path": child.path, "size": child.stat().st_size if os.access(child.path, os.R_OK) else 0, "children": [], "isdir": False, "access": os.access(child.path, os.R_OK)}
                            try:
                                childnode = Node(child.name, child.stat().st_size, None, False, True)
                            except (PermissionError, OSError):
                                childnode = Node(child.name, 0, None, False, False)
                        else:
                            childnode = scan(child.path)
                        node.children.append(childnode)
                        dirsize += childnode.size
            except:
                # return {"path": location, "size": 0, "children": [], "isdir": True, "access": False}
                splitpath = os.path.split(location)
                elementname = splitpath[-1] if splitpath[1] else splitpath[0][0]
                return Node(elementname, 0, [], True, False)
            node.size = dirsize
            return node
            
    else:
        # return {"path": location, "size": 0, "children": [], "isdir": os.path.isdir(location), "access": False}
        return Node(location, 0, [], True, False)
        #THIS ASSUMES THAT EVERY NODE PASSED INTO SCAN FUNCTION IS A DIRECTORY NODE

#schema for children
"""
{
    "name",
    "size",
    "children",
    "isdir",
    "access"
}
"""

def cleardisplay():
    print("\033[2J\033[1;1H")

def chkvalue(x):
    return x.size
currentdir = []

def getlocation():
    return os.path.join(currentdir[0] + ":\\", *currentdir[1:])

def display(x):
    global currentdir
    currentdir.append(x.name)
    clocation = getlocation()
    while True: 
        cleardisplay()
        if not (x.isdir):
            print("="*10)
            print(clocation)
            print("="*10 + "\n\n")
            # splitpath = os.path.split(x.path)
            # elementname = splitpath[-1] if splitpath[1] else splitpath[0][0]
            print("Name: "+x.name)
            try:
                print("Type:",magic.from_file(clocation , mime=True))
                print("Details:",magic.from_file(clocation))
            except:
                print("Type: Error parsing")
                print("Details: Error parsing")
            input("press enter to go back..")
            currentdir.pop()

            return

        print("="*10)
        print(clocation)
        print("="*10 + "\n\n")
        children = x.children
        children.sort(key= chkvalue, reverse= True)
        count = 1
        print("[0] [back] ...")
        max_len = 0
        max_num = len(str(len(children)))
        for child in children:
            if len(child.name) > max_len:
                max_len = len(child.name)
        for child in children:
            print(f"[{count:>{max_num}}] [{"D" if child.isdir else "F"}] {child.name:<{max_len}}         {unitconversion(child.size):>10} [{"ACCESSIBLE" if child.access else "INACCESSIBLE"}]" )
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
            currentdir.pop()
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

