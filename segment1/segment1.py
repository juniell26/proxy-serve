import scapy.all as scapy
import segment2
import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Set up the database connection
engine = create_engine('sqlite:///packets.db')
Base = declarative_base()

# Define a Packet model
class Packet(Base):
    __tablename__ = 'packets'

    id = Column(Integer, primary_key=True)
    src_ip = Column(String)
    dst_ip = Column(String)
    src_port = Column(Integer)
    dst_port = Column(Integer)
    device = Column(String)
    handshake = Column(String)
    packet_location = Column(String)

# Create the database tables
Base.metadata.create_all(engine)

# Set up the database session
Session = sessionmaker(bind=engine)
session = Session()

def process_packet(packet):
    # Extract relevant information from the packet
    src_ip = packet[scapy.IP].src
    dst_ip = packet[scapy.IP].dst
    src_port = packet[scapy.TCP].sport
    dst_port = packet[scapy.TCP].dport
    device = packet[scapy.RadioTap].notdecoded
    handshake = packet[scapy.TCP].flags
    packet_location = packet[scapy.GPS].location

    # Perform analysis on the packet data
    # ...
    # If an anomaly is detected, block the connection
    if len(packet[scapy.Raw].load) > 1000:
        # Create an iptables rule to drop all traffic to and from the source IP address
        os.system(f"iptables -A INPUT -s {src_ip} -j DROP")
        os.system(f"iptables -A OUTPUT -d {src_ip} -j DROP")
        print(f"Connection from {src_ip}:{src_port} blocked due to anomaly detected.")

    # Insert the packet information into the database
    packet_info = Packet(src_ip=src_ip, dst_ip=dst_ip, src_port=src_port, dst_port=dst_port, device=device, handshake=handshake, packet_location=packet_location)
    session.add(packet_info)
    session.commit()


def run_packet_capture():
    # Set up the packet capture filter
    capture_filter = "tcp and (dst port 80 or dst port 443)"  # capture HTTP and HTTPS traffic

    # Start capturing packets
    scapy.sniff(filter=capture_filter, prn=process_packet)

# Start capturing packets
run_packet_capture()
