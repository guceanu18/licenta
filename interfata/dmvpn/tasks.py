import pyshark
import subprocess
import threading
import os
import pyshark
import subprocess
import time
from celery import shared_task



def capture_traffic():
    subprocess.call([r'C:\Users\Guci\Desktop\test.bat'])

def update_bw_partial():
    myBat = open(r'C:\Users\Guci\Desktop\test.bat', 'w+')
    myBat.write('"C:\Program Files\EVE-NG\plink.exe" -ssh -batch -pw eve root@192.168.0.99 "tcpdump -U -i '
                'vunl0_28_0 -s 0 -w -" | "C:\Program Files\Wireshark\Wireshark.exe" -k -i - -w C:\\Users\\Guci\\Desktop\\capture.pcap')
    myBat.close()
    capture_thread = threading.Thread(target=capture_traffic)
    capture_thread.start()

    bw_partial = 0
    while os.path.getsize('C:\\Users\\Guci\\Desktop\\capture.pcap') != 0 and bw_partial < 10000:
        bw_partial = 0
        cap = pyshark.FileCapture('C:\\Users\\Guci\\Desktop\\capture.pcap')
        for packet in cap:
            bw_partial += int(packet.length)
        time.sleep(30)
        
    return bw_partial


@shared_task
def run_capture():
    bw_partial = update_bw_partial()
    return bw_partial



    



