import bcrypt
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from threading import Thread
from .thread import *
import paramiko, hashlib, time, pyshark
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Credentials
from django.contrib.auth.hashers import check_password

start_capture = None
bw_list = []


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = Credentials.objects.get(username=username)

            if hashlib.sha256(password.encode('utf-8')).hexdigest() == user.password:
                # Passwords match, so log in the user
                request.session['username'] = username
                return redirect('index')
            else:
                # Passwords don't match, so show an error
                error = "Invalid username or password"
        except Credentials.DoesNotExist:
            # User doesn't exist, so show an error
            error = "Invalid username or password"

        return render(request, 'dmvpn/login.html', {'error': error})

    return render(request, 'dmvpn/login.html')


def register(request):
    if request.method == 'POST':
        # Create a new user form and save it if valid
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Create a new Credentials instance for the new user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            print(f"Username: {username}, Password: {password}")
            c = Credentials(username=username, password=password)
            c.save()
            # Redirect the user to the login page
            return redirect('login')
    else:
        # Display a blank form for the user to fill out
        form = UserCreationForm()
    return render(request, 'dmvpn/register.html', {'form': form})


def index(request):
    if request.session.get('username'):
        if request.method == 'GET':
            global start_capture
            if start_capture:
                start_capture.stop()
                start_capture = None
        return render(request, 'dmvpn/index.html')
    else:
        return redirect('login')


def bucuresti(request):
    if request.session.get('username'):
        global start_capture
        bw_list.clear()
        if not start_capture:
            start_capture = StartCaptureBucuresti()
            start_capture.start()
        return render(request, 'dmvpn/bucuresti.html')
    else:
        return redirect('login')


def phase1(request):
    # Router credentials
    HOST_BUC = '192.168.0.98'
    HOST_BV = '192.168.0.97'
    HOST_CJ = '192.168.0.96'
    HOST_CT = '192.168.0.95'
    USER = 'admin'
    PASSWORD = 'admin '

    # Connect to the router BUC via SSH
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST_BUC, username=USER, password=PASSWORD, look_for_keys=False, allow_agent=False)

    # Start an interactive session
    channel = client.invoke_shell()

    # Wait for the router to respond
    time.sleep(1)

    # Send commands to configure the router
    channel.send('configure terminal\n')
    time.sleep(1)
    channel.send('int t0\n')
    time.sleep(1)
    channel.send('no ip nhrp redirect\n')
    time.sleep(1)

    # Exit configuration mode
    channel.send('exit\n')

    # Save the configuration changes
    channel.send('write memory\n')

    # Close the SSH connection
    client.close()

    # Connect to the router BV via SSH
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST_BV, username=USER, password=PASSWORD, look_for_keys=False, allow_agent=False)

    # Start an interactive session
    channel = client.invoke_shell()

    # Wait for the router to respond
    time.sleep(1)

    # Send commands to configure the router
    channel.send('configure terminal\n')
    time.sleep(1)
    channel.send('int t0\n')
    time.sleep(1)
    channel.send('no ip nhrp shortcut\n')
    time.sleep(1)

    # Exit configuration mode
    channel.send('exit\n')

    # Save the configuration changes
    channel.send('write memory\n')

    # Close the SSH connection
    client.close()

    # Connect to the router CJ via SSH
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST_CJ, username=USER, password=PASSWORD, look_for_keys=False, allow_agent=False)

    # Start an interactive session
    channel = client.invoke_shell()

    # Wait for the router to respond
    time.sleep(1)

    # Send commands to configure the router
    channel.send('configure terminal\n')
    time.sleep(1)
    channel.send('int t0\n')
    time.sleep(1)
    channel.send('no ip nhrp shortcut\n')
    time.sleep(1)

    # Exit configuration mode
    channel.send('exit\n')

    # Save the configuration changes
    channel.send('write memory\n')

    # Close the SSH connection
    client.close()

    # Connect to the router CT via SSH
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST_CT, username=USER, password=PASSWORD, look_for_keys=False, allow_agent=False)

    # Start an interactive session
    channel = client.invoke_shell()

    # Wait for the router to respond
    time.sleep(1)

    # Send commands to configure the router
    channel.send('configure terminal\n')
    time.sleep(1)
    channel.send('int t0\n')
    time.sleep(1)
    channel.send('no ip nhrp shortcut\n')
    time.sleep(1)

    # Exit configuration mode
    channel.send('exit\n')

    # Save the configuration changes
    channel.send('write memory\n')

    # Close the SSH connection
    client.close()

    return redirect(calcul_bw_buc)


def phase3(request):
    # Router credentials
    HOST_BUC = '192.168.0.98'
    HOST_BV = '192.168.0.97'
    HOST_CJ = '192.168.0.96'
    HOST_CT = '192.168.0.95'
    USER = 'admin'
    PASSWORD = 'admin '

    # Connect to the router BUC via SSH
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST_BUC, username=USER, password=PASSWORD, look_for_keys=False, allow_agent=False)

    # Start an interactive session
    channel = client.invoke_shell()

    # Wait for the router to respond
    time.sleep(1)

    # Send commands to configure the router
    channel.send('configure terminal\n')
    time.sleep(1)
    channel.send('int t0\n')
    time.sleep(1)
    channel.send('ip nhrp redirect\n')
    time.sleep(1)

    # Exit configuration mode
    channel.send('exit\n')

    # Save the configuration changes
    channel.send('write memory\n')

    # Close the SSH connection
    client.close()

    # Connect to the router BV via SSH
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST_BV, username=USER, password=PASSWORD, look_for_keys=False, allow_agent=False)

    # Start an interactive session
    channel = client.invoke_shell()

    # Wait for the router to respond
    time.sleep(1)

    # Send commands to configure the router
    channel.send('configure terminal\n')
    time.sleep(1)
    channel.send('int t0\n')
    time.sleep(1)
    channel.send('ip nhrp shortcut\n')
    time.sleep(1)

    # Exit configuration mode
    channel.send('exit\n')

    # Save the configuration changes
    channel.send('write memory\n')

    # Close the SSH connection
    client.close()

    # Connect to the router CJ via SSH
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST_CJ, username=USER, password=PASSWORD, look_for_keys=False, allow_agent=False)

    # Start an interactive sessions
    channel = client.invoke_shell()

    # Wait for the router to respond
    time.sleep(1)

    # Send commands to configure the router
    channel.send('configure terminal\n')
    time.sleep(1)
    channel.send('int t0\n')
    time.sleep(1)
    channel.send('ip nhrp shortcut\n')
    time.sleep(1)

    # Exit configuration mode
    channel.send('exit\n')

    # Save the configuration changes
    channel.send('write memory\n')

    # Close the SSH connection
    client.close()

    # Connect to the router CT via SSH
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST_CT, username=USER, password=PASSWORD, look_for_keys=False, allow_agent=False)

    # Start an interactive session
    channel = client.invoke_shell()

    # Wait for the router to respond
    time.sleep(1)

    # Send commands to configure the router
    channel.send('configure terminal\n')
    time.sleep(1)
    channel.send('int t0\n')
    time.sleep(1)
    channel.send('ip nhrp shortcut\n')
    time.sleep(1)

    # Exit configuration mode
    channel.send('exit\n')

    # Save the configuration changes
    channel.send('write memory\n')

    # Close the SSH connection
    client.close()

    return redirect(calcul_bw_buc)


def test_delay_buc(request):
    # Router credentials
    HOST_BUC = '192.168.0.98'
    HOST_BV = '192.168.0.97'
    HOST_CJ = '192.168.0.96'
    USER = 'admin'
    PASSWORD = 'admin '

    # Connect to the router BUC via SSH
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST_BUC, username=USER, password=PASSWORD, look_for_keys=False, allow_agent=False)

    # Start an interactive session
    channel = client.invoke_shell()

    # Wait for the router to respond
    time.sleep(1)

    # Send commands to configure the router
    channel.send('ping 10.255.255.2 repeat 50\n')
    time.sleep(2)
    # Close the SSH connection
    client.close()

    return redirect(calcul_bw_buc)


def calcul_bw_buc(request):
    if request.session.get('username'):
        t1 = ReadCaptureBucuresti()
        t1.start()

        delay_list = []
        drop_list = []
        bytes_total = 0
        ping_requests = {}
        start_time = None
        end_time = None
        packets_processed = 0
        protocols = {}
        num_drops = 0
        prev_seq = 0

        for packet in t1.cap:
            packets_processed += 1
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
                # Check if the packet is a ping reply
                elif int(packet.icmp.type) == 0:
                    ping_request = ping_requests.get(int(packet.icmp.ident), None)
                    if ping_request:
                        delay = float(packet.sniff_timestamp) - float(ping_request.sniff_timestamp)
                        # compute the delay in ms
                        delay = delay * 1000
                        delay_list.append(delay)

            if 'TCP' in packet:
                seq = int(packet.tcp.seq)
                if seq < prev_seq:
                    num_drops += 1
                    drop_list.append(num_drops)
                prev_seq = seq

            if packets_processed >= 10000:
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
    else:
        return redirect('login')


def brasov(request):
    if request.session.get('username'):
        global start_capture
        bw_list.clear()
        if not start_capture:
            start_capture = StartCaptureBrasov()
            start_capture.start()
        return render(request, 'dmvpn/brasov.html')
    else:
        return redirect('login')


def calcul_bw_bv(request):
    if request.session.get('username'):
        t1 = ReadCaptureBrasov()
        t1.start()

        delay_list = []
        drop_list = []
        bytes_total = 0
        ping_requests = {}
        start_time = None
        end_time = None
        packets_processed = 0
        protocols = {}
        num_drops = 0
        prev_seq = 0

        for packet in t1.cap:
            packets_processed += 1
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
                # Check if the packet is a ping reply
                elif int(packet.icmp.type) == 0:
                    ping_request = ping_requests.get(int(packet.icmp.ident), None)
                    if ping_request:
                        delay = float(packet.sniff_timestamp) - float(ping_request.sniff_timestamp)
                        # compute the delay in ms
                        delay = delay * 1000
                        delay_list.append(delay)

            if 'TCP' in packet:
                seq = int(packet.tcp.seq)
                if seq < prev_seq:
                    num_drops += 1
                    drop_list.append(num_drops)
                prev_seq = seq

            if packets_processed >= 10000:
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

        return render(request, 'dmvpn/brasov_bw.html', context)
    else:
        return redirect('login')


def test_delay_bv(request):
    # Router credentials
    HOST_BUC = '192.168.0.98'
    HOST_BV = '192.168.0.97'
    HOST_CJ = '192.168.0.96'
    USER = 'admin'
    PASSWORD = 'admin '

    # Connect to the router BV via SSH
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST_BV, username=USER, password=PASSWORD, look_for_keys=False, allow_agent=False)

    # Start an interactive session
    channel = client.invoke_shell()

    # Wait for the router to respond
    time.sleep(1)

    # Send commands to configure the router
    channel.send('ping 10.255.255.3 repeat 50\n')
    time.sleep(2)
    # Close the SSH connection
    client.close()

    return redirect(calcul_bw_bv)


def cluj(request):
    if request.session.get('username'):
        global start_capture
        bw_list.clear()
        if not start_capture:
            start_capture = StartCaptureCluj()
            start_capture.start()
        return render(request, 'dmvpn/cluj.html')
    else:
        return redirect('login')


def calcul_bw_cj(request):
    if request.session.get('username'):
        t1 = ReadCaptureCluj()
        t1.start()

        delay_list = []
        drop_list = []
        bytes_total = 0
        ping_requests = {}
        start_time = None
        end_time = None
        packets_processed = 0
        protocols = {}
        num_drops = 0
        prev_seq = 0

        for packet in t1.cap:
            packets_processed += 1
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
                # Check if the packet is a ping reply
                elif int(packet.icmp.type) == 0:
                    ping_request = ping_requests.get(int(packet.icmp.ident), None)
                    if ping_request:
                        delay = float(packet.sniff_timestamp) - float(ping_request.sniff_timestamp)
                        # compute the delay in ms
                        delay = delay * 1000
                        delay_list.append(delay)

            if 'TCP' in packet:
                seq = int(packet.tcp.seq)
                if seq < prev_seq:
                    num_drops += 1
                    drop_list.append(num_drops)
                prev_seq = seq

            if packets_processed >= 10000:
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

        return render(request, 'dmvpn/cluj_bw.html', context)
    else:
        return redirect('login')


def test_delay_cj(request):
    # Router credentials
    HOST_BUC = '192.168.0.98'
    HOST_BV = '192.168.0.97'
    HOST_CJ = '192.168.0.96'
    USER = 'admin'
    PASSWORD = 'admin '

    # Connect to the router CJ via SSH
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST_CJ, username=USER, password=PASSWORD, look_for_keys=False, allow_agent=False)

    # Start an interactive session
    channel = client.invoke_shell()

    # Wait for the router to respond
    time.sleep(1)

    # Send commands to configure the router
    channel.send('ping 10.255.255.2 repeat 50\n')
    time.sleep(2)
    # Close the SSH connection
    client.close()

    return redirect(calcul_bw_cj)


def constanta(request):
    if request.session.get('username'):
        global start_capture
        bw_list.clear()
        if not start_capture:
            start_capture = StartCaptureConstanta()
            start_capture.start()
        return render(request, 'dmvpn/constanta.html')
    else:
        return redirect('login')


def calcul_bw_ct(request):
    if request.session.get('username'):
        t1 = ReadCaptureConstanta()
        t1.start()

        delay_list = []
        drop_list = []
        bytes_total = 0
        ping_requests = {}
        start_time = None
        end_time = None
        packets_processed = 0
        protocols = {}
        num_drops = 0
        prev_seq = 0

        for packet in t1.cap:
            packets_processed += 1
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
                # Check if the packet is a ping reply
                elif int(packet.icmp.type) == 0:
                    ping_request = ping_requests.get(int(packet.icmp.ident), None)
                    if ping_request:
                        delay = float(packet.sniff_timestamp) - float(ping_request.sniff_timestamp)
                        # compute the delay in ms
                        delay = delay * 1000
                        delay_list.append(delay)

            if 'TCP' in packet:
                seq = int(packet.tcp.seq)
                if seq < prev_seq:
                    num_drops += 1
                    drop_list.append(num_drops)
                prev_seq = seq

            if packets_processed >= 10000:
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

        return render(request, 'dmvpn/constanta_bw.html', context)
    else:
        return redirect('login')


def test_delay_ct(request):
    # Router credentials
    HOST_BUC = '192.168.0.98'
    HOST_BV = '192.168.0.97'
    HOST_CJ = '192.168.0.96'
    HOST_CT = '192.168.0.95'
    USER = 'admin'
    PASSWORD = 'admin '

    # Connect to the router CT via SSH
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST_CT, username=USER, password=PASSWORD, look_for_keys=False, allow_agent=False)

    # Start an interactive session
    channel = client.invoke_shell()

    # Wait for the router to respond
    time.sleep(1)

    # Send commands to configure the router
    channel.send('ping 10.255.255.3 repeat 50\n')
    time.sleep(2)
    # Close the SSH connection
    client.close()

    return redirect(calcul_bw_ct)
