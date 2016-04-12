rm /tmp/testfs.py
touch /tmp/testfs.py
./testfs/mktestfs /tmp/fs 2> /tmp/testfs.py
./testfs/testfs.exe /tmp/fs 2> /tmp/testfs.py
