import threading
import subprocess
import pyshark
import psutil


class StartCaptureBucuresti(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.process = None

    def run(self):
        try:
            myBat = open(r'C:\Users\Guci\Desktop\LicentaDjango\files\bucuresti.bat', 'w+')
            myBat.write('"C:\Program Files\EVE-NG\plink.exe" -ssh -batch -pw eve root@192.168.0.99 "tcpdump -U -i '
                        'vunl0_28_0 -s 0 -w -" | "C:\Program Files\Wireshark\Wireshark.exe" -k -i - -w C:\\Users\\Guci\\Desktop\\LicentaDjango\\files\\bucuresti.pcap')
            myBat.close()
            # subprocess.call([r'C:\Users\Guci\Desktop\LicentaDjango\files\bucuresti.bat'])
            self.process = subprocess.Popen([r'C:\Users\Guci\Desktop\LicentaDjango\files\bucuresti.bat'])
            self.process.communicate()
        except Exception as e:
            print(e)

    def stop(self):
        if self.process:
            for proc in psutil.process_iter():
                if proc.name() == "Wireshark.exe" or proc.name() == "Dumpcap.exe":
                    proc.terminate()
            self.process.terminate()
        self.stop_event.set()


class ReadCaptureBucuresti(threading.Thread):
    cap = pyshark.FileCapture('C:\\Users\\Guci\\Desktop\\LicentaDjango\\files\\bucuresti.pcap')

    def __init__(self):
        threading.Thread.__init__(self)

