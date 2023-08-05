#!python3
# -*- coding: utf-8 -*-
import os
import sys
import uiautomation as automation

def GetDirChildren(directory):
    if os.path.isdir(directory):
        subdirs = []
        files = []
        for it in os.listdir(directory):
            absPath = os.path.join(directory, it)
            if os.path.isdir(absPath):
                subdirs.append(absPath)
            else:
                files.append(absPath)
        return subdirs + files

def main(directory, maxDepth = 0xFFFFFFFF):
    remain = {}
    text = []
    absdir = os.path.abspath(directory)
    for it, depth, remainCount in automation.WalkTree(absdir, getChildrenFunc= GetDirChildren, includeTop= True, maxDepth= maxDepth):
        remain[depth] = remainCount
        prefix = ''.join(['|     ' if remain[i+1] else '      ' for i in range(depth - 1)]) + ('|---- ' if depth > 0 else '')
        file = it[it.rfind('\\')+1:]
        text.append(prefix)
        text.append(file)
        text.append('\n')
        text += prefix + file + '\n'
        automation.Logger.Write(prefix)
        automation.Logger.WriteLine(file, automation.ConsoleColor.Cyan if os.path.isdir(it) else -1)
    automation.SetClipboardText(''.join(text))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        adir = input('input a dir: ')
        main(adir)
    elif len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        main(sys.argv[1], int(sys.argv[2]))
    input('\nThe pretty dir tree has been copied to clipboard, just paste it\nPress Enter to exit')
