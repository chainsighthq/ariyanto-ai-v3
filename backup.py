import shutil
import os
from datetime import datetime
from pathlib import Path

def backup():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path("backups") / timestamp
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    # Backup database
    if Path("data/ariyanto_ai.db").exists():
        shutil.copy("data/ariyanto_ai.db", backup_dir / "ariyanto_ai.db")
        print(f"✅ Database backed up")
    
    # Backup logs
    if Path("logs").exists():
        shutil.copytree("logs", backup_dir / "logs", dirs_exist_ok=True)
        print(f"✅ Logs backed up")
    
    print(f"\n✅ Backup completed: {backup_dir}")

if __name__ == "__main__":
    backup()
