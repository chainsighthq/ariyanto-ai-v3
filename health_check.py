import subprocess
import sys
from datetime import datetime

def check_health():
    print(f"\n{'='*60}")
    print(f"ARIYANTO AI v3 - HEALTH CHECK")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    checks = []
    
    # 1. Service status
    try:
        result = subprocess.run(["systemctl", "is-active", "ariyanto-ai"], capture_output=True, text=True)
        if result.stdout.strip() == "active":
            print("✅ Service: RUNNING")
            checks.append(True)
        else:
            print(f"❌ Service: {result.stdout.strip().upper()}")
            checks.append(False)
    except:
        print("❌ Service: ERROR")
        checks.append(False)
    
    # 2. Redis
    try:
        result = subprocess.run(["redis-cli", "ping"], capture_output=True, text=True)
        if "PONG" in result.stdout:
            print("✅ Redis: CONNECTED")
            checks.append(True)
        else:
            print("❌ Redis: NOT RESPONDING")
            checks.append(False)
    except:
        print("❌ Redis: NOT INSTALLED")
        checks.append(False)
    
    # 3. Python imports
    try:
        result = subprocess.run(
            [sys.executable, "-c", "from ariyanto_ai_v3.agents.supervisor_agent import SupervisorAgent; print('OK')"],
            capture_output=True, text=True, cwd="/home/ubuntu/ariyanto-ai-v3",
            env={**dict(__import__('os').environ), "PYTHONPATH": "src"}
        )
        if "OK" in result.stdout:
            print("✅ Python Imports: OK")
            checks.append(True)
        else:
            print(f"❌ Python Imports: FAILED")
            checks.append(False)
    except:
        print("❌ Python Imports: ERROR")
        checks.append(False)
    
    # 4. Disk space
    try:
        result = subprocess.run(["df", "-h", "/"], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        if len(lines) > 1:
            usage = lines[1].split()[4].replace('%', '')
            if int(usage) < 80:
                print(f"✅ Disk Space: {usage}% used")
                checks.append(True)
            else:
                print(f"⚠️  Disk Space: {usage}% used (HIGH!)")
                checks.append(False)
    except:
        print("❌ Disk Space: ERROR")
        checks.append(False)
    
    # 5. Backup
    try:
        import os
        backup_dir = "/home/ubuntu/ariyanto-ai-v3/backups"
        if os.path.exists(backup_dir):
            backups = os.listdir(backup_dir)
            if backups:
                print(f"✅ Backup: {len(backups)} backups available")
                checks.append(True)
            else:
                print("⚠️  Backup: No backups yet")
                checks.append(False)
        else:
            print("⚠️  Backup: Folder not found")
            checks.append(False)
    except:
        print("❌ Backup: ERROR")
        checks.append(False)
    
    # Summary
    print(f"\n{'='*60}")
    passed = sum(checks)
    total = len(checks)
    print(f"SUMMARY: {passed}/{total} checks passed")
    
    if passed == total:
        print("✅ SYSTEM HEALTH: EXCELLENT")
    elif passed >= total - 1:
        print("⚠️  SYSTEM HEALTH: GOOD (minor issues)")
    else:
        print("❌ SYSTEM HEALTH: NEEDS ATTENTION")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    check_health()
