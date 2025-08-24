import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict
import random

class ThreatDetector:
    def __init__(self):
        # Rule-based detection counters
        self.ssh_attempts = defaultdict(int)
        self.port_scan_attempts = defaultdict(int)
        self.ddos_attempts = defaultdict(list)
        self.THRESHOLD = 5
        self.TIME_WINDOW = timedelta(minutes=1)
        
        # Simulate ML model loading
        print("🤖 Loading AI threat detection models...")
        self.ml_models_loaded = True

    def ml_detect_anomaly(self, features):
        """Simulate ML-based anomaly detection"""
        if self.ml_models_loaded:
            # Simulate ML prediction
            anomaly_score = random.random()
            is_anomaly = anomaly_score > 0.7  # 30% chance of anomaly
            return is_anomaly, anomaly_score
        return False, 0.0

    def rule_based_detection(self, packet):
        """Rule-based threat detection"""
        current_time = datetime.now()
        src_ip = packet.get('src_ip', 'unknown')
        
        # SSH Bruteforce detection
        if packet.get('dst_port') == 22 and packet.get('protocol') == 'TCP':
            self.ssh_attempts[src_ip] += 1
            if self.ssh_attempts[src_ip] > self.THRESHOLD:
                return "ssh_bruteforce", "high", 0.95
        
        # Port Scan detection
        if packet.get('flags') == 'S':  # SYN packet
            self.port_scan_attempts[src_ip] += 1
            if self.port_scan_attempts[src_ip] > self.THRESHOLD * 2:
                return "port_scan", "medium", 0.85
        
        # DDoS detection
        self.ddos_attempts[src_ip] = [t for t in self.ddos_attempts.get(src_ip, []) 
                                    if current_time - t < self.TIME_WINDOW]
        self.ddos_attempts[src_ip].append(current_time)
        
        if len(self.ddos_attempts[src_ip]) > self.THRESHOLD * 10:
            return "ddos_attempt", "critical", 0.99
        
        return None, None, 0.0

    def extract_features(self, packet):
        """Extract features for ML analysis"""
        return [
            packet.get('packet_size', 0),
            packet.get('src_port', 0),
            packet.get('dst_port', 0),
            packet.get('protocol', 0),
            len(packet.get('payload', ''))
        ]

    def detect_threat(self, packet):
        """Main threat detection method"""
        # Rule-based detection first
        rule_threat, severity, confidence = self.rule_based_detection(packet)
        if rule_threat:
            return rule_threat, severity, confidence
        
        # ML-based detection
        features = self.extract_features(packet)
        is_anomaly, ml_confidence = self.ml_detect_anomaly(features)
        
        if is_anomaly:
            threat_types = ["suspicious_traffic", "potential_intrusion", "anomalous_behavior"]
            return random.choice(threat_types), "medium", ml_confidence
        
        return None, None, 0.0

# Global detector instance
detector = ThreatDetector()