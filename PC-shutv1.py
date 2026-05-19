import paramiko
import threading

# =========================
# CONFIG
# =========================

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
    81, 82,
    91, 92
]

COMMAND = "shutdown -f -p"

# Windows:
# COMMAND = "shutdown /s /f /t 0"


# =========================
# ASK USER
# =========================

my_monitor = int(input("Enter YOUR monitor number: "))

# Build IPs
ips = [f"{NETWORK_BASE}.{m + 100}" for m in MONITORS]

# Your IP
my_ip = f"{NETWORK_BASE}.{my_monitor + 100}"

# Move your PC to end
if my_ip in ips:
    ips.remove(my_ip)
    ips.append(my_ip)

# =========================
# PRINT ORDER FIRST
# =========================

print("\n==============================")
print(" SHUTDOWN ORDER ")
print("==============================")

for index, ip in enumerate(ips, start=1):

    if ip == my_ip:
        print(f"{index}. {ip}  <-- YOUR PC (LAST)")
    else:
        print(f"{index}. {ip}")

print("==============================\n")

confirm_all = input("Continue shutdown? (y/n): ").lower()

if confirm_all != "y":
    print("Cancelled.")
    exit()


# =========================
# SSH FUNCTION
# =========================

def shutdown_host(ip):
    try:
        print(f"[+] Connecting -> {ip}")

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(
            hostname=ip,
            username=USERNAME,
            password=PASSWORD,
            timeout=5
        )

        ssh.exec_command(COMMAND)

        print(f"[OK] Shutdown sent -> {ip}")

        ssh.close()

    except Exception as e:
        print(f"[ERROR] {ip} -> {e}")


# =========================
# SHUTDOWN OTHERS FIRST
# =========================

threads = []

for ip in ips[:-1]:
    t = threading.Thread(target=shutdown_host, args=(ip,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()


# =========================
# LAST PC CONFIRMATION
# =========================

print(f"\nLAST PC: {ips[-1]}")

confirm_last = input("Shutdown your PC too? (y/n): ").lower()

if confirm_last == "y":
    shutdown_host(ips[-1])
else:
    print("Your PC skipped.")