import threading
import subprocess
import pyshark


class CreateWiresharkThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        try:
            myBat = open(r'C:\Users\Guci\Desktop\test.bat', 'w+')
            myBat.write('"C:\Program Files\EVE-NG\plink.exe" -ssh -batch -pw eve root@192.168.0.99 "tcpdump -U -i '
                        'vunl0_28_0 -s 0 -w -" | "C:\Program Files\Wireshark\Wireshark.exe" -k -i - -w C:\\Users\\Guci\\Desktop\\capture.pcap')
            myBat.close()
            subprocess.call([r'C:\Users\Guci\Desktop\test.bat'])
        except Exception as e:
            print(e)


class CalculateBandwidthThread(threading.Thread):
    cap = pyshark.FileCapture('C:\\Users\\Guci\\Desktop\\capture.pcap')

    def __init__(self):
        threading.Thread.__init__(self)

