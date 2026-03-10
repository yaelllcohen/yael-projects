import os, shutil #הספרייה הזאת יכולה למחוק תיקייה גם כשיש תוכן בפנים

base = os.path.join("keys", "client")
for folder in os.listdir(base):
    path = os.path.join(base, folder)
    if os.path.isdir(path):
        shutil.rmtree(path) #פה אני בעצם מוחקת
        print(f"Deleted {path}")
