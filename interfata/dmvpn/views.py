from django.shortcuts import render
from django.http import HttpResponse
from threading import Thread
import pyshark
from .thread import *


def index(request):
    return render(request, 'dmvpn/index.html')


def bucuresti(request):
    CreateWiresharkThread().start()

    return render(request, 'dmvpn/bucuresti.html')


bw_list = []

def calcul_bw(request):
    t1 = CalculateBandwidthThread()
    t1.start()

    start_time = None
    end_time = None
    bytes_total = 0
    protocols = {}
    packets_processed = 0

    for packet in t1.cap:
        if not start_time:
            start_time = float(packet.sniff_timestamp)
        end_time = float(packet.sniff_timestamp)
        bytes_total += int(packet.length)

        protocol = packet.highest_layer
        if protocol in protocols:
            protocols[protocol] += 1
        else:
            protocols[protocol] = 1

        packets_processed += 1
        if packets_processed == 1000:
            t1.cap.clear()
            packets_processed = 0

    elapsed_time = end_time - start_time
    bandwidth = bytes_total / elapsed_time
    # rezultatul in Bytes/s

    bandwidth = bandwidth * 8 / 1000
    # rezultatul in Kbps

    bw_list.append(bandwidth)

    params = []
    params.append(bw_list)
    params.append(protocols)

    context = {'params': params}

    return render(request, 'dmvpn/bucuresti_bw.html', context)
