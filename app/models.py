from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from datetime import datetime
from .database import Base

class Threat(Base):
    __tablename__ = "threats"
    
    id = Column(Integer, primary_key=True, index=True)
    source_ip = Column(String, index=True)
    destination_ip = Column(String)
    threat_type = Column(String)  # "ssh_bruteforce", "port_scan", "ddos", etc.
    severity = Column(String)     # "low", "medium", "high", "critical"
    confidence = Column(Float)    # ML confidence score
    timestamp = Column(DateTime, default=datetime.utcnow)
    packet_info = Column(String)
    is_resolved = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Threat {self.id}: {self.threat_type} from {self.source_ip}>"