d=`date +%m-%d`
s="RPISW"
diskutil list
echo "Choose the disk with the name 'boot': "
read bName
sudo dd if=$bName of=/Volumes/NO\ NAME/$s-$d.DMG
cd /Volumes/NO\ NAME/
echo $s-$d.DMG
tar -jcvf $s-$d.tar.bz2 $s-$d.DMG
rm $s-$d.DMG