import threading
import subprocess
import pyshark
import psutil
import time
import paramiko


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


class StartCaptureBrasov(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.process = None

    def run(self):
        try:
            myBat = open(r'C:\Users\Guci\Desktop\LicentaDjango\files\brasov.bat', 'w+')
            myBat.write('"C:\Program Files\EVE-NG\plink.exe" -ssh -batch -pw eve root@192.168.0.99 "tcpdump -U -i '
                        'vunl0_10_16 -s 0 -w -" | "C:\Program Files\Wireshark\Wireshark.exe" -k -i - -w C:\\Users\\Guci\\Desktop\\LicentaDjango\\files\\brasov.pcap')
            myBat.close()

            self.process = subprocess.Popen([r'C:\Users\Guci\Desktop\LicentaDjango\files\brasov.bat'])
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


class ReadCaptureBrasov(threading.Thread):
    cap = pyshark.FileCapture('C:\\Users\\Guci\\Desktop\\LicentaDjango\\files\\brasov.pcap')

    def __init__(self):
        threading.Thread.__init__(self)


class StartCaptureCluj(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.process = None

    def run(self):
        try:
            myBat = open(r'C:\Users\Guci\Desktop\LicentaDjango\files\cluj.bat', 'w+')
            myBat.write('"C:\Program Files\EVE-NG\plink.exe" -ssh -batch -pw eve root@192.168.0.99 "tcpdump -U -i '
                        'vunl0_11_19 -s 0 -w -" | "C:\Program Files\Wireshark\Wireshark.exe" -k -i - -w C:\\Users\\Guci\\Desktop\\LicentaDjango\\files\\cluj.pcap')
            myBat.close()

            self.process = subprocess.Popen([r'C:\Users\Guci\Desktop\LicentaDjango\files\cluj.bat'])
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


class ReadCaptureCluj(threading.Thread):
    cap = pyshark.FileCapture('C:\\Users\\Guci\\Desktop\\LicentaDjango\\files\\cluj.pcap')

    def __init__(self):
        threading.Thread.__init__(self)


class StartCaptureConstanta(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.process = None

    def run(self):
        try:
            myBat = open(r'C:\Users\Guci\Desktop\LicentaDjango\files\constanta.bat', 'w+')
            myBat.write('"C:\Program Files\EVE-NG\plink.exe" -ssh -batch -pw eve root@192.168.0.99 "tcpdump -U -i '
                        'vunl0_12_16 -s 0 -w -" | "C:\Program Files\Wireshark\Wireshark.exe" -k -i - -w C:\\Users\\Guci\\Desktop\\LicentaDjango\\files\\constanta.pcap')
            myBat.close()

            self.process = subprocess.Popen([r'C:\Users\Guci\Desktop\LicentaDjango\files\constanta.bat'])
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


class ReadCaptureConstanta(threading.Thread):
    cap = pyshark.FileCapture('C:\\Users\\Guci\\Desktop\\LicentaDjango\\files\\constanta.pcap')

    def __init__(self):
        threading.Thread.__init__(self)



