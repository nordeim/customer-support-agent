# scripts/post_deployment_validation.py
import requests
import time
import sys
from typing import Dict, List

class PostDeploymentValidator:
    """Validates system health after deployment"""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.frontend_url = "http://localhost:80"
        self.results = []
    
    def check_backend_health(self) -> bool:
        """Check backend health"""
        try:
            response = requests.get(f"{self.base_url}/health/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get("status") == "healthy"
            return False
        except Exception as e:
            print(f"Backend health check failed: {e}")
            return False
    
    def check_frontend_health(self) -> bool:
        """Check frontend health"""
        try:
            response = requests.get(f"{self.frontend_url}/health", timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"Frontend health check failed: {e}")
            return False
    
    def test_chat_flow(self) -> bool:
        """Test basic chat flow"""
        try:
            # Create session
            response = requests.post(
                f"{self.base_url}/chat/sessions",
                json={"user_id": "test-user"},
                timeout=10
            )
            if response.status_code != 200:
                return False
            
            session_id = response.json()["session_id"]
            
            # Send message
            response = requests.post(
                f"{self.base_url}/chat/sessions/{session_id}/messages",
                data={"message": "Test message"},
                timeout=30
            )
            
            return response.status_code == 200
        except Exception as e:
            print(f"Chat flow test failed: {e}")
            return False
    
    def check_monitoring(self) -> bool:
        """Check monitoring systems"""
        try:
            # Check Prometheus
            response = requests.get("http://localhost:9090/-/healthy", timeout=10)
            if response.status_code != 200:
                return False
            
            # Check Grafana
            response = requests.get("http://localhost:3000/api/health", timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"Monitoring check failed: {e}")
            return False
    
    def run_all_checks(self) -> Dict[str, bool]:
        """Run all validation checks"""
        checks = {
            "Backend Health": self.check_backend_health,
            "Frontend Health": self.check_frontend_health,
            "Chat Flow": self.test_chat_flow,
            "Monitoring": self.check_monitoring
        }
        
        results = {}
        for check_name, check_func in checks.items():
            print(f"Running {check_name}...")
            result = check_func()
            results[check_name] = result
            status = "✓" if result else "✗"
            print(f"{status} {check_name}: {'PASS' if result else 'FAIL'}")
        
        return results
    
    def generate_report(self, results: Dict[str, bool]) -> str:
        """Generate validation report"""
        passed = sum(results.values())
        total = len(results)
        
        report = f"""
Post-Deployment Validation Report
=================================
Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}
Overall Status: {'PASS' if passed == total else 'FAIL'}
Tests Passed: {passed}/{total}

Test Results:
"""
        
        for check_name, result in results.items():
            status = "PASS" if result else "FAIL"
            report += f"  {check_name}: {status}\n"
        
        if passed == total:
            report += "\n✓ All checks passed. Deployment validated successfully."
        else:
            report += "\n✗ Some checks failed. Please investigate and resolve issues."
        
        return report

def main():
    validator = PostDeploymentValidator()
    results = validator.run_all_checks()
    report = validator.generate_report(results)
    
    print(report)
    
    # Exit with error code if any checks failed
    if not all(results.values()):
        sys.exit(1)

if __name__ == "__main__":
    main()
