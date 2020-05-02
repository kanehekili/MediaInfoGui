#!/bin/bash
#check if sudo
if [ "$EUID" -ne 0 ] ; then
  echo "Sorry, but you are not root. Use sudo to run"
  exit 1
fi

read -p "Which flavour do you want? 1) QT5 2) GTK3 :" sel

#copy desktop to /usr/share applications
sudo mkdir -p /usr/local/bin/MediaInfoGui;
if [ "$sel" = "1" ]
then
	sudo cp MediaInfoGuiQt.desktop /usr/share/applications/MediaInfoGui.desktop
        echo "copying QT"
        prompt="#    *pyqt5 or python3-pyqt5                       #"
elif [ "$sel" = "2" ]
then
	sudo cp MediaInfoGuiGTK3.desktop /usr/share/applications/MediaInfoGui.desktop
        prompt="#    *python-gobject                               #"
        echo "copying GTK3"
else
   echo "Invalid choice. Aborting"
   exit 1
fi		
sudo cp * /usr/local/bin/MediaInfoGui/;

echo "####################################################"
echo "#   Ensure you have installed:                     #"                     
echo "$prompt"
echo "#    *mediainfo                                    #"
echo "####################################################"
echo "App installed."
