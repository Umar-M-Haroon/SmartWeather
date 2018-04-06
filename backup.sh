#get the current date and create a string RPISW
d=`date +%m-%d`
s="RPISW"
#Show connected disks and asks for the
#user to choose the SD card disk and stores the disk name in bName
diskutil list
echo "Choose the disk with the name 'boot': "
read bName
#create the .dmg from the SD card and output it to the USB
sudo dd if=$bName of=/Volumes/NO\ NAME/$s-$d.DMG
cd /Volumes/NO\ NAME/
#Go to the USB, compress the backup, delete the original DMG to save space
tar -jcvf $s-$d.tar.bz2 $s-$d.DMG
rm $s-$d.DMG