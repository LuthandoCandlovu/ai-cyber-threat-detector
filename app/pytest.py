# test_threat_detection.py
from backend.app import threat_detection # type: ignore

def test_detect_failed_logins():
    class MockLog:
        def __init__(self, ip, event_type):
            self.ip = ip
            self.event_type = event_type

    mock_logs = [MockLog("192.168.1.1", "login_failed")] * 6
    result = threat_detection.detect_failed_logins(mock_logs, threshold=5)
    assert "192.168.1.1" in result