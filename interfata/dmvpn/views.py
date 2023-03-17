from django.shortcuts import render
from django.http import HttpResponse
from threading import Thread
import pyshark
from .thread import *

start_capture = None
bw_list = []


def index(request):
    if request.method == 'POST':
        global start_capture
        if start_capture:
            start_capture.stop()
            start_capture = None
    return render(request, 'dmvpn/index.html')


def bucuresti(request):
    global start_capture
    bw_list.clear()
    if not start_capture:
        start_capture = StartCaptureBucuresti()
        start_capture.start()
    return render(request, 'dmvpn/bucuresti.html')


def calcul_bw_buc(request):
    t1 = ReadCaptureBucuresti()
    t1.start()

    start_time = None
    end_time = None
    bytes_total = 0
    ping_requests = {}
    protocols = {}
    packets_processed = 0
    num_drops = 0
    prev_seq = 0
    delay_list = []
    drop_list = []

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

        if packet.highest_layer == 'ICMP':
            # Check if the packet is a ping request
            if int(packet.icmp.type) == 8:
                ping_requests[int(packet.icmp.ident)] = packet
            # Check if the packet is a ping response
            elif int(packet.icmp.type) == 0:
                ping_request = ping_requests.get(int(packet.icmp.ident), None)
                if ping_request:
                    delay = float(packet.sniff_timestamp) - float(ping_request.sniff_timestamp)
                    delay = delay * 1000
                    delay_list.append(delay)

        if 'TCP' in packet:
            seq = int(packet.tcp.seq)
            if seq < prev_seq:
                num_drops += 1
                drop_list.append(num_drops)
            prev_seq = seq

        packets_processed += 1
        if packets_processed == 1000:
            t1.cap.clear()
            packets_processed = 0

    bandwidth = 0
    elapsed_time = end_time - start_time
    if elapsed_time == 0 or elapsed_time is None:
        bandwidth = 0
    else:
        bandwidth = bytes_total / elapsed_time

    # rezultatul in Bytes/s

    bandwidth = bandwidth * 8 / 1000
    # rezultatul in Kbps

    bw_list.append(bandwidth)



    params = []
    params.append(bw_list)
    params.append(protocols)
    params.append(delay_list)
    params.append(drop_list)

    context = {'params': params}

    return render(request, 'dmvpn/bucuresti_bw.html', context)


def brasov(request):
    global start_capture
    bw_list.clear()
    if not start_capture:
        start_capture = StartCaptureBrasov()
        start_capture.start()
    return render(request, 'dmvpn/brasov.html')


def calcul_bw_bv(request):
    t1 = ReadCaptureBrasov()
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

    return render(request, 'dmvpn/brasov_bw.html', context)
