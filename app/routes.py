from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .database import get_db
from .models import Threat

router = APIRouter()

@router.get("/threats", response_model=List[dict])
def get_threats(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all threats from database"""
    threats = db.query(Threat).order_by(Threat.timestamp.desc()).offset(skip).limit(limit).all()
    return [
        {
            "id": threat.id,
            "source_ip": threat.source_ip,
            "threat_type": threat.threat_type,
            "severity": threat.severity,
            "confidence": threat.confidence,
            "timestamp": threat.timestamp.isoformat(),
            "is_resolved": threat.is_resolved
        }
        for threat in threats
    ]

@router.get("/threats/stats")
def get_threat_stats(db: Session = Depends(get_db)):
    """Get threat statistics"""
    total = db.query(Threat).count()
    critical = db.query(Threat).filter(Threat.severity == "critical").count()
    high = db.query(Threat).filter(Threat.severity == "high").count()
    medium = db.query(Threat).filter(Threat.severity == "medium").count()
    low = total - (critical + high + medium)
    
    return {
        "total_threats": total,
        "by_severity": {
            "critical": critical,
            "high": high,
            "medium": medium,
            "low": low
        }
    }

@router.post("/threats/{threat_id}/resolve")
def resolve_threat(threat_id: int, db: Session = Depends(get_db)):
    """Mark a threat as resolved"""
    threat = db.query(Threat).filter(Threat.id == threat_id).first()
    if not threat:
        raise HTTPException(status_code=404, detail="Threat not found")
    
    threat.is_resolved = True
    db.commit()
    return {"message": f"Threat {threat_id} resolved successfully"}