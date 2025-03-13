#!/usr/bin/env python3

import getpass
import telnetlib
import time

user = input("Enter your telnet username: ")
password = getpass.getpass()

# Open the file containing switch IP addresses called myswitches
with open('myswitches') as f:
    for line in f:
        HOST = line.strip()
        print(f"Configuring switch {HOST}")

        try:
            tn = telnetlib.Telnet(HOST, timeout=10)  # Add timeout

            tn.read_until(b"Username: ")
            tn.write(user.encode('ascii') + b"\n")
            if password:
                tn.read_until(b"Password: ")
                tn.write(password.encode('ascii') + b"\n")

            # Wait for login to be successful
            login_output = tn.read_until(b"#", timeout=5).decode('ascii')
            print(login_output)  # Debugging
            if "#" not in login_output:
                print(f"Login failed for {HOST}. Skipping...")
                continue  # Move to the next switch

            # Enter global configuration mode
            tn.write(b"configure terminal\n")
            tn.read_until(b"(config)#")
            time.sleep(1)  # Prevent command flooding

            # VLAN Configuration Loop
            for n in range(350, 356):
                print(f"Creating VLAN {n} on {HOST}...")
                tn.write(f"vlan {n}\n".encode('ascii'))
                tn.read_until(b"(config-vlan)#", timeout=5)
                tn.write(f"name LAN{n}\n".encode('ascii'))
                tn.read_until(b"(config-vlan)#", timeout=5)
                tn.write(b"exit\n")
                tn.read_until(b"(config)#", timeout=5)
                time.sleep(0.1)  # Increase delay

            # Save configuration
            tn.write(b"end\n")
            tn.read_until(b"#")
            tn.write(b"write memory\n")  # Save configuration
            tn.read_until(b"#")

            # Close session
            tn.write(b"exit\n")
            tn.close()

            print(f"VLANs  successfully configured on {HOST}!")

        except Exception as e:
            print(f"Error configuring switch {HOST}: {e}")

