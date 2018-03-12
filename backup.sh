d=`date +%m-%d`
s="RPISW"
sudo dd if=/dev/disk2 of=/Volumes/NO\ NAME/$s-$d.DMG
cd /Volumes/NO\ NAME/
echo $s-$d.DMG
tar -jcvf $s-$d.tar.bz2 $s-$d.DMG
rm $s-$d.DMG