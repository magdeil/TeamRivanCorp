import paramiko
import threading

USERNAME = "Administrator"
PASSWORD = "C1sc0123"

NETWORK_BASE = "10.3.3"

MONITORS = [
    11, 12,
    21, 22,
    31, 32,
    41, 42,
    51, 52,
    61, 62,
    71, 72,
    80, 82,
    91, 92
]

COMMAND = "shutdown -f -p"

MY_MONITOR = 42  # <-- set your PC here

ips = [f"{NETWORK_BASE}.{m + 100}" for m in MONITORS]

my_ip = f"{NETWORK_BASE}.{MY_MONITOR + 100}"

if my_ip in ips:
    ips.remove(my_ip)
    ips.append(my_ip)


def shutdown_host(ip):
    try:
        print(f"[+] {ip}")

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(ip, username=USERNAME, password=PASSWORD, timeout=5)
        ssh.exec_command(COMMAND)

        print(f"[OK] {ip}")

        ssh.close()

    except Exception as e:
        print(f"[ERROR] {ip} -> {e}")


threads = []

for ip in ips:
    t = threading.Thread(target=shutdown_host, args=(ip,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()