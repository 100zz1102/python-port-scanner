print("Started")
print("1. Scan ports")
print("2. Exit")

choice = input("Choose: ").strip()

import socket
import threading

if choice == "1":
    print("YOU CHOSE 1")

    target = input("Enter ip: ")
    start = int(input("Start port: "))
    end = int(input("End port: "))

    open_ports = []

    print(f"\n[+] Scanning {target} from port {start} to {end}...\n")

    def scan(port):
        s = socket.socket()
        s.settimeout(1)

        result = s.connect_ex((target, port))

        if result == 0:
            service = "Unknown"

            try:
                s.sendall(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
                s.settimeout(1)

                response = s.recv(1024).decode(errors="ignore")

                if "HTTP" in response:
                    service = "HTTP"

            except:
                pass

            print(f"[+] Open port: {port}")
            open_ports.append((port, service))

    threads = []

    for port in range(start, end):
        t = threading.Thread(target=scan, args=(port,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    with open("result.txt", "w") as f:
        for port, service in open_ports:
            f.write(f"[OPEN] Port {port} | {service}\n")

    print("\nScan finished")

    if open_ports:
        print(f"[+] Found {len(open_ports)} open ports")
    else:
        print("[-] No open ports found")

elif choice == "2":
    print("Exiting...")