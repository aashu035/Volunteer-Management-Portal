import requests
import json

BASE_URL = "http://localhost:8001/api/v1"

print("--- Starting Security Vulnerability Tests ---")

def test_sql_injection_login():
    print("\n[1] Testing SQL Injection on Login (/auth/login)...")
    payload = {
        "email": "admin@amaanitvam.org' OR '1'='1",
        "password": "password123' OR '1'='1"
    }
    try:
        res = requests.post(f"{BASE_URL}/auth/login", json=payload)
        
        if res.status_code == 200:
            print("❌ VULNERABILITY FOUND: SQL Injection succeeded on Login endpoint!")
            return False
        else:
            print(f"✅ PASSED: SQL Injection prevented. (Status Code: {res.status_code})")
            return True
    except Exception as e:
        print(f"Error testing SQLi: {e}")
        return False

def get_admin_token():
    res = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "admin@amaanitvam.org",
        "password": "Admin@123"
    })
    return res.json().get("access_token")

def test_xss_event_creation():
    print("\n[2] Testing Cross-Site Scripting (XSS) on Event Creation...")
    token = get_admin_token()
    if not token:
        print("⚠️ Could not get admin token, skipping XSS test.")
        return False
        
    headers = {"Authorization": f"Bearer {token}"}
    
    payload = {
        "title": "<script>alert('XSS')</script> Malicious Event",
        "description": "<img src=x onerror=alert('XSS')>",
        "location": "Test Location",
        "start_time": "2027-01-01T10:00:00Z",
        "end_time": "2027-01-01T14:00:00Z",
        "capacity": 50,
        "required_skills": ["Testing"]
    }
    
    try:
        res = requests.post(f"{BASE_URL}/events/", json=payload, headers=headers)
        
        if res.status_code in [200, 201]:
            data = res.json()
            if "<script>" in data.get("title", "") or "<img" in data.get("description", ""):
                print("❌ VULNERABILITY FOUND: XSS payload accepted and reflected without sanitization!")
                return False
        
        print(f"✅ PASSED: XSS payload handled properly (or rejected). (Status: {res.status_code})")
        return True
    except Exception as e:
        print(f"Error testing XSS: {e}")
        return False

def test_rate_limiting():
    print("\n[3] Testing Rate Limiting (Brute Force Protection)...")
    
    failed_attempts = 0
    # The limit is 5/minute. We try 10 times.
    for i in range(10):
        res = requests.post(f"{BASE_URL}/auth/login", json={
            "email": "admin@amaanitvam.org",
            "password": "WrongPassword123"
        })
        if res.status_code == 429: # Too Many Requests
            print(f"✅ PASSED: Rate limiting triggered after {i} attempts!")
            return True
            
    print(f"❌ VULNERABILITY FOUND: No rate limiting detected. Last status: {res.status_code}")
    return False

if __name__ == "__main__":
    test_sql_injection_login()
    test_xss_event_creation()
    test_rate_limiting()
    print("\n--- Security Tests Completed ---")
