# MediaInfoGui
GUI for MediaInfo data — available in Qt6, GTK3 and GTK4

Version 1.3.2

[Download](https://github.com/kanehekili/MediaInfoGui/releases/download/1.3.2/MediaInfoGui1.3.2.tar)

This simple GUI for the media info binary runs on Linux. Provides a fast & clean overview of the contents of a media file.

##### Qt6 Implementation

![Screenshot](https://github.com/kanehekili/MediaInfoGui/blob/master/Screenshot-Qt5.png)

##### GTK3 Implementation

![Screenshot](https://github.com/kanehekili/MediaInfoGui/blob/master/Screenshot-GTK3.png)

### Features
- Opens on a given filename, usually from a file manager
- Shows codec data for video, audio and images
- Displays full MPEG-TS program structure (PAT/PMT), including broken or unresolvable programs — requires `ffprobe`
- Section headers highlighted with the theme's selection colour
- Copy to clipboard button ("Clip") for pasting media info into other applications
- Supports light and dark themes
- Proper desktop integration: docks, taskbars and app switchers identify the window and show the application icon — on X11 and Wayland

### Prerequisites
- `mediainfo`
- Qt6: `python3-pyqt6` (PyQt6)
- GTK3: `python3-gi` with GTK 3
- GTK4: `python3-gi` with GTK 4
- Optional: `ffprobe` (from ffmpeg) for MPEG-TS program info

### How to install
 * Download the MediaInfoGui*.tar from the [releases page](https://github.com/kanehekili/MediaInfoGui/releases/download/1.3.2/MediaInfoGui1.3.2.tar)
 * Unpack it and run the command  **sudo ./install.sh** in the unpacked folder.
 * Select 1 for Qt6, 2 for GTK3, 3 for GTK4 — or just press enter for the auto detection
 * Install copies a desktop file and the python scripts to /opt/mediainfogui, and links it as /usr/bin/mediainfogui

