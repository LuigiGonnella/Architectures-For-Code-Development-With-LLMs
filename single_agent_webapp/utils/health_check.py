"""
Health check script for the webapp
Tests if both frontend and backend are running and accessible
"""

import requests
import sys
from time import sleep

BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

def check_backend():
    """Check if backend is healthy"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend is healthy")
            print(f"   Model: {data.get('model', 'Unknown')}")
            return True
        else:
            print(f"❌ Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Backend is not running at {BACKEND_URL}")
        return False
    except Exception as e:
        print(f"❌ Backend error: {str(e)}")
        return False

def check_frontend():
    """Check if frontend is accessible"""
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            print(f"✅ Frontend is accessible at {FRONTEND_URL}")
            return True
        else:
            print(f"❌ Frontend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Frontend is not running at {FRONTEND_URL}")
        return False
    except Exception as e:
        print(f"❌ Frontend error: {str(e)}")
        return False

def test_backend_api():
    """Test a simple query to the backend"""
    try:
        print("\n🧪 Testing backend API with sample query...")
        response = requests.post(
            f"{BACKEND_URL}/api/query",
            json={
                "query": "Write a simple function that returns 'Hello World'",
                "show_node_info": False
            },
            timeout=60
        )
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Backend API test successful")
                print(f"   Generated code snippet:")
                code = data.get('code', '')
                if code:
                    lines = code.split('\n')[:3]
                    for line in lines:
                        print(f"   {line}")
                    if len(code.split('\n')) > 3:
                        print("   ...")
                return True
            else:
                print("❌ Backend API returned success=False")
                return False
        else:
            print(f"❌ Backend API returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend API test error: {str(e)}")
        return False

def main():
    print("🔍 LLM-for-SE WebApp Health Check\n")
    print("=" * 50)
    
    # Check backend
    print("\n📡 Checking Backend...")
    backend_ok = check_backend()
    
    # Check frontend
    print("\n🎨 Checking Frontend...")
    frontend_ok = check_frontend()
    
    # Test backend API if backend is healthy
    api_ok = False
    if backend_ok:
        api_ok = test_backend_api()
    
    # Summary
    print("\n" + "=" * 50)
    print("\n📊 Summary:")
    print(f"   Backend: {'✅ Healthy' if backend_ok else '❌ Not Running'}")
    print(f"   Frontend: {'✅ Accessible' if frontend_ok else '❌ Not Running'}")
    print(f"   API Test: {'✅ Passed' if api_ok else '⚠️  Not Tested' if not backend_ok else '❌ Failed'}")
    
    if backend_ok and frontend_ok:
        print("\n✅ All systems operational!")
        print(f"\n   Open your browser to: {FRONTEND_URL}")
        return 0
    else:
        print("\n❌ Some components are not running")
        if not backend_ok:
            print("   Start backend: cd single_agent_webapp/backend && python -m uvicorn main:app --reload")
        if not frontend_ok:
            print("   Start frontend: cd single_agent_webapp/frontend && npm run dev")
        return 1

if __name__ == "__main__":
    sys.exit(main())
