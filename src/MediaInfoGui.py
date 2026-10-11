#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Nov 25, 2011
Vern�nftige GTK Oberfl�che f�r media info
@author: kanehekili
'''
import subprocess
import sys
import json
import re
from subprocess import Popen


VERSION="@xxxx@"


def parseLines(lines):
    result = []
    for line in lines:
        row = line.decode("utf-8")
        token = re.split('[ ]+:[ ]+', row)
        result.append((token[0], token[1] if len(token) > 1 else ""))
    return result


def isHeader(row):
    return len(row[1]) == 0 and len(row[0]) > 0


def formatForClipboard(rows):
    lines = []
    for t0, t1 in rows:
        if t0 and not t1:
            lines.append(t0)
        elif t0 or t1:
            lines.append(f"{t0:<40} : {t1}")
        else:
            lines.append("")
    return "\n".join(lines)


def _isMpegTS(lines):
    for line in lines:
        if b"MPEG-TS" in line:
            return True
    return False


def _streamResolvable(s):
    ct = s.get("codec_type", "unknown")
    if ct == "video":
        return int(s.get("width", 0) or 0) > 0
    if ct == "audio":
        sr = s.get("sample_rate")
        return sr is not None and str(sr) not in ("0", "N/A", "")
    return False


def _getTSProgramLines(filename):
    try:
        proc = Popen(
            ["ffprobe", "-v", "quiet", "-show_programs", "-of", "json", filename],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        out, _ = proc.communicate()
    except FileNotFoundError:
        return []

    try:
        data = json.loads(out)
    except ValueError:
        return []

    programs = data.get("programs", [])
    if not programs:
        return []

    lines = []
    lines.append(b"MPEG-TS Programs")
    lines.append(f"{'Program count':<40} : {len(programs)}".encode())

    for prog in programs:
        prog_id  = prog.get("program_id", "?")
        pmt_pid  = prog.get("pmt_pid", "?")
        streams  = prog.get("streams", [])
        nb       = len(streams)

        if nb == 0:
            value = f"PMT PID {pmt_pid} - no streams (broken)"
        else:
            type_counts = {}
            for s in streams:
                ct = s.get("codec_type", "unknown")
                type_counts[ct] = type_counts.get(ct, 0) + 1
            type_str = ", ".join(f"{v} {k}" for k, v in type_counts.items())
            resolvable = any(_streamResolvable(s) for s in streams)
            broken = "" if resolvable else " (unresolvable)"
            value = f"PMT PID {pmt_pid} - {nb} stream{'s' if nb != 1 else ''} ({type_str}){broken}"

        lines.append(f"{'Program ' + str(prog_id):<40} : {value}".encode())

    lines.append(b"")
    return lines


def _insertAfterGeneral(lines, extraLines):
    in_general = False
    for i, line in enumerate(lines):
        row = line.decode("utf-8", errors="replace")
        is_section_header = len(re.split(r'[ ]+:[ ]+', row)) == 1
        stripped = row.strip()

        if is_section_header and stripped == "General":
            in_general = True
            continue
        if in_general and is_section_header:
            if stripped == "":
                # insert after this blank separator line
                return lines[:i+1] + extraLines + lines[i+1:]
            else:
                # no blank line found before next section - insert one
                return lines[:i] + [b""] + extraLines + lines[i:]

    return lines + [b""] + extraLines


NO_FILE_TEXT = "- no file selected -"
INVALID_FILE_TEXT = "- no media info available -"
NO_TOOL_TEXT = "- mediainfo not installed -"


def readMediaInfo(type,filename):
    lines = []
    placeholder = NO_FILE_TEXT
    if len(filename)>3:
        placeholder = INVALID_FILE_TEXT
        try:
            result=Popen(["mediainfo",filename],stdout=subprocess.PIPE).communicate()[0]
        except FileNotFoundError:
            placeholder = NO_TOOL_TEXT
            result = b""
        if len(result) > 10:
            lines = result.splitlines()
            if _isMpegTS(lines):
                tsLines = _getTSProgramLines(filename)
                if tsLines:
                    lines = _insertAfterGeneral(lines, tsLines)

    if not lines:
        #no (usable) file given - show an empty list instead of an error dialog
        lines = [placeholder.encode()]

    showListDialog(type,filename,lines)


def windowTitle(fileName):
    paths = [p for p in fileName.split("/") if p]
    if not paths:
        return "Media Info"
    return "/".join(paths[-2:])


def showListDialog(type,fileName,mediaInfoList):
    item = windowTitle(fileName)
    rows = parseLines(mediaInfoList)
    if type == "gtk3":
        import MediaInfoWidgetsGTK3
        MediaInfoWidgetsGTK3.main([item,rows])
    elif type == "gtk4":
        import MediaInfoWidgetsGTK4
        MediaInfoWidgetsGTK4.main([item,rows])
    else:
        import MediaInfoWidgetsQt
        MediaInfoWidgetsQt.main([item,rows])


def detectToolkit():
    #No toolkit requested: take the first one that is actually installed.
    #The order matches the alternative depends of the debian package
    #(gir1.2-gtk-4.0 | gir1.2-gtk-3.0), so package and app agree.
    import importlib.util
    if importlib.util.find_spec("gi") is not None:
        import gi
        for ui,gtkVersion in (("gtk4","4.0"),("gtk3","3.0")):
            try:
                gi.require_version('Gtk', gtkVersion)
                return ui
            except ValueError:
                pass
    #nothing found either - let the Qt import raise a readable error
    return "qt"


def main(argv = None):
    filename=""
    type=""
    if argv is None:
        argv = sys.argv
        args=argv[1:]
        #the toolkit is optional - a single argument is taken as the filename
        if args and args[0] in ("qt","gtk3","gtk4"):
            type=args.pop(0)
        if args:
            filename=args[0]

    if type=="":
        type=detectToolkit()

    print("Version:"+VERSION+" UI:"+type)
    readMediaInfo(type,filename)

if __name__ == '__main__':
    sys.exit(main())
