#!/usr/bin/env python3
from scapy.all import *
import sys
import threading
import time

def send_spoofed_udp(spoofed_ip, target_ip, target_port, message, source_port=12345):
    """Send UDP packet with spoofed source IP using Scapy"""
    try:
        # Create packet with spoofed IP
        packet = IP(src=spoofed_ip, dst=target_ip) / UDP(sport=source_port, dport=target_port) / message
        
        # Send packet
        send(packet, verbose=False)
        
        print(f"Spoofed UDP packet sent!")
        print(f"Fake source: {spoofed_ip}:{source_port}")
        print(f"Target: {target_ip}:{target_port}")
        print(f"Message: {message}")
        
    except Exception as e:
        print(f"Error sending packet: {e}")

def send_spoofed_tcp_syn(spoofed_ip, target_ip, target_port, source_port=12345):
    """Send TCP SYN packet with spoofed IP"""
    try:
        # Create TCP SYN packet
        packet = IP(src=spoofed_ip, dst=target_ip) / TCP(sport=source_port, dport=target_port, flags="S")
        
        # Send packet
        send(packet, verbose=False)
        
        print(f"Spoofed TCP SYN packet sent!")
        print(f"Fake source: {spoofed_ip}:{source_port}")
        print(f"Target: {target_ip}:{target_port}")
        
    except Exception as e:
        print(f"Error sending packet: {e}")

def send_spoofed_icmp(spoofed_ip, target_ip, message="Spoofed ping"):
    """Send ICMP packet with spoofed IP"""
    try:
        # Create ICMP packet
        packet = IP(src=spoofed_ip, dst=target_ip) / ICMP() / message
        
        # Send packet
        send(packet, verbose=False)
        
        print(f"Spoofed ICMP packet sent!")
        print(f"Fake source: {spoofed_ip}")
        print(f"Target: {target_ip}")
        print(f"Message: {message}")
        
    except Exception as e:
        print(f"Error sending packet: {e}")


# Command line interface
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Scapy IP Spoofing Demonstration Tool")
        print("=====================================")
        print("Usage:")
        print("  UDP spoofing:     python3 script.py udp <spoofed_ip> <target_ip> <port> <message>")
        print("  TCP SYN spoofing: python3 script.py tcp <spoofed_ip> <target_ip> <port>")
        print("  ICMP spoofing:    python3 script.py icmp <spoofed_ip> <target_ip> [message]")
        print("  Packet listener:  python3 script.py listen [filter] [count]")
        print("  Continuous spoof: python3 script.py continuous <spoofed_ip> <target_ip> <port> <message> [interval]")
        print("  Demo all:         python3 script.py demo <spoofed_ip> <target_ip>")
        print("\nExamples:")
        print("  python3 script.py udp 192.168.1.100 192.168.1.200 9999 'Hello World'")
        print("  python3 script.py listen 'udp and port 9999' 10")
        print("  python3 script.py demo 192.168.1.100 192.168.1.200")
        sys.exit(1)
    
    mode = sys.argv[1].lower()
    
    if mode == "udp":
        if len(sys.argv) != 6:
            print("UDP usage: python3 script.py udp <spoofed_ip> <target_ip> <port> <message>")
            sys.exit(1)
        send_spoofed_udp(sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5])
        
    elif mode == "tcp":
        if len(sys.argv) != 5:
            print("TCP usage: python3 script.py tcp <spoofed_ip> <target_ip> <port>")
            sys.exit(1)
        send_spoofed_tcp_syn(sys.argv[2], sys.argv[3], int(sys.argv[4]))
        
    elif mode == "icmp":
        if len(sys.argv) < 4:
            print("ICMP usage: python3 script.py icmp <spoofed_ip> <target_ip> [message]")
            sys.exit(1)
        message = sys.argv[4] if len(sys.argv) > 4 else "Spoofed ping"
        send_spoofed_icmp(sys.argv[2], sys.argv[3], message)

    elif mode == "demo":
        if len(sys.argv) != 4:
            print("Demo usage: python3 script.py demo <spoofed_ip> <target_ip>")
            sys.exit(1)
        demo_multiple_protocols(sys.argv[2], sys.argv[3])
        
    else:
        print(f"Unknown mode: {mode}")
        print("Use udp, tcp, icmp, listen, continuous, or demo")