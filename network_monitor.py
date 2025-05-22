import socket
import time
import webbrowser
import subprocess
import platform

def check_network():
    try:
        # Create a socket object to test connectivity
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def get_default_gateway():
    if platform.system() == "Windows":
        # Get default gateway on Windows
        output = subprocess.check_output("ipconfig", shell=True).decode()
        for line in output.split('\n'):
            if "Default Gateway" in line:
                gateway = line.split(': ')[-1].strip()
                if gateway and gateway != '':
                    return gateway
    else:
        # For Linux/Mac (simplified)
        try:
            output = subprocess.check_output("ip route | grep default", shell=True).decode()
            return output.split()[2]
        except:
            pass
    return None

def main():
    # You can change this IP address to whatever you want to open
    target_ip = "http://192.168.4.1/"  # Replace this with your desired IP address
    
    print("Network Monitor Started...")
    print("Waiting for network connection...")
    
    # Wait for network connection
    while not check_network():
        time.sleep(2)
    
    print(f"Network connected! Opening IP address: {target_ip}")
    # Open the specified IP in the default web browser
    webbrowser.open(f"http://{target_ip}")

if __name__ == "__main__":
    main()
