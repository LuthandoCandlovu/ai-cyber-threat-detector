import sys
import os
import threading
import time
from datetime import datetime
import random

# Add the parent directory to Python path for absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now use absolute imports
from app.database import SessionLocal
from app.models import Threat
from app.threat_detector import detector

class PacketSniffer:
    def __init__(self):
        self.running = False
        self.sniffer_thread = None
        
    def generate_simulated_packet(self):
        """Generate realistic network packet data for simulation"""
        protocols = ['TCP', 'UDP', 'ICMP']
        flags = ['S', 'A', 'F', 'R', '']  # SYN, ACK, FIN, RST, None
        
        return {
            'src_ip': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            'dst_ip': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            'src_port': random.randint(1024, 65535),
            'dst_port': random.choice([22, 80, 443, 53, 3389, 1433, 3306]),
            'protocol': random.choice(protocols),
            'packet_size': random.randint(64, 1500),
            'flags': random.choice(flags),
            'payload': ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=random.randint(0, 100))),
            'timestamp': datetime.now()
        }

    def save_threat(self, packet_info, threat_type, severity, confidence):
        """Save detected threat to database"""
        db = SessionLocal()
        try:
            threat = Threat(
                source_ip=packet_info.get('src_ip', 'unknown'),
                destination_ip=packet_info.get('dst_ip', 'unknown'),
                threat_type=threat_type,
                severity=severity,
                confidence=confidence,
                packet_info=str(packet_info)
            )
            db.add(threat)
            db.commit()
            return threat
        except Exception as e:
            print(f"❌ Error saving threat: {e}")
            db.rollback()
            return None
        finally:
            db.close()

    def packet_callback(self, packet):
        """Process each packet and detect threats"""
        if not self.running:
            return
            
        # Detect threats
        threat_type, severity, confidence = detector.detect_threat(packet)
        
        if threat_type:
            # Save to database
            threat = self.save_threat(packet, threat_type, severity, confidence)
            
            # Print alert
            if threat:
                print(f"🚨 THREAT DETECTED: {threat_type.upper()} from {packet['src_ip']}")
                print(f"   📊 Severity: {severity.upper()}, Confidence: {confidence:.2%}")
                print(f"   🎯 Destination: {packet['dst_ip']}:{packet['dst_port']}")
                print("   " + "═" * 50)
        else:
            # Normal traffic
            if random.random() < 0.1:  # Only show 10% of normal traffic
                print(f"✅ Normal traffic: {packet['src_ip']} → {packet['dst_ip']}:{packet['dst_port']}")

    def start_sniffing(self):
        """Start the packet sniffing simulation"""
        self.running = True
        print("📡 Starting packet sniffer simulation...")
        print("👁️  Monitoring network traffic...")
        print("═" * 60)
        
        try:
            while self.running:
                # Generate simulated packet
                packet = self.generate_simulated_packet()
                
                # Process packet
                self.packet_callback(packet)
                
                # Random delay between packets
                time.sleep(random.uniform(0.1, 1.0))
                
        except KeyboardInterrupt:
            self.stop_sniffing()

    def stop_sniffing(self):
        """Stop the packet sniffer"""
        self.running = False
        print("\n🛑 Stopping packet sniffer...")

    def start(self):
        """Start sniffer in a separate thread"""
        self.sniffer_thread = threading.Thread(target=self.start_sniffing, daemon=True)
        self.sniffer_thread.start()
        return self.sniffer_thread

# Global sniffer instance
sniffer = PacketSniffer()