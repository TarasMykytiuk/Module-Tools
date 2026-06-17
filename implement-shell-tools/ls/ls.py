import sys
import os
import pwd
import grp
import stat
from datetime import datetime
from pathlib import Path


def main():
    args = sys.argv[1:]
    flags = []
    parentDir = ".."
    currentDir = "."
    path = currentDir
    for item in args:
        if item[0] == "-":
            flags.append(item)
        else:
            path = item
    scanResult = os.scandir(path)
    isHiddenToShow = "-a" in flags
    isShowLineByLine = "-1" in flags
    isStatsToList = "-l" in flags
    content = sortDirContent(scanResult, isHiddenToShow)

    if not isHiddenToShow and not isStatsToList and not isShowLineByLine:
        output = ""
        for item in content:
            output += (
                addColorToStr("\033[34m", item.name) + "  "
                if Path(item).is_dir()
                else item.name + "  "
            )
        print(output)
    if not isHiddenToShow and not isStatsToList and isShowLineByLine:
        for item in content:
            print(
                addColorToStr("\033[34m", item.name) + "  "
                if Path(item).is_dir()
                else item.name + "  "
            )
    elif isHiddenToShow and not isStatsToList:
        output = (
            addColorToStr("\033[34m", currentDir)
            + "  "
            + addColorToStr("\033[34m", parentDir)
            + "  "
        )
        for item in content:
            output += (
                addColorToStr("\033[34m", item.name) + "  "
                if Path(item).is_dir()
                else item.name + "  "
            )
        print(output)
    elif not isHiddenToShow and isStatsToList:
        print("total " + str(calcTotalSpace(content)))
        printContentStats(content)
    elif isHiddenToShow and isStatsToList:
        print("total " + str(calcTotalSpace(content)))
        currentDirObj = Path(currentDir)
        parentDirObj = Path(parentDir)
        printContentStats([currentDirObj, parentDirObj])
        printContentStats(content)


def calcTotalSpace(content):
    sum = 0
    for item in content:
        sum += item.stat().st_blocks
    return sum // 2


def addColorToStr(color, str):
    reset = "\033[0m"
    return color + str + reset


def sortDirContent(scanResult, isHiddenToShow):
    files = []
    directories = []
    hidden = []
    for item in scanResult:
        if item.name[0] == ".":
            hidden.append(item)
        elif os.path.isfile(item):
            files.append(item)
        elif os.path.isdir(item):
            directories.append(item)
    content = files + directories + hidden if isHiddenToShow else files + directories
    return content


def readFilePermissions(path):
    permissions = os.stat(path)
    perm_str = stat.filemode(permissions.st_mode)
    return perm_str


def printContentStats(content):
    for item in content:
        perm = stat.filemode(item.stat().st_mode)
        links = str(item.stat().st_nlink)
        owner = pwd.getpwuid(item.stat().st_uid).pw_name
        group = grp.getgrgid(item.stat().st_gid).gr_name
        size = str(item.stat().st_size).rjust(4)
        lastModTime = formatTime(item.stat().st_mtime)
        itemName = str(item) if str(item) == "." else item.name
        if item.is_dir():
            itemName = addColorToStr("\033[34m", itemName)
        print(
            perm
            + " "
            + links
            + " "
            + owner
            + " "
            + group
            + " "
            + size
            + " "
            + lastModTime
            + " "
            + itemName
        )


def formatTime(timestamp):
    time = datetime.fromtimestamp(timestamp)
    month = time.strftime("%b")  # str(time.month)
    day = str(time.day)
    hour = str(time.hour)
    minute = str(time.minute)
    return month + " " + day + " " + hour.rjust(2, "0") + ":" + minute.rjust(2, "0")


if __name__ == "__main__":
    main()
