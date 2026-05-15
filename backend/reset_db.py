"""Reset database"""
import os
import sys

# Ensure we're using a fresh database
for f in ['test.db', 'ai_video.db']:
    if os.path.exists(f):
        os.remove(f)
        print(f'Removed {f}')

# Run in subprocess to ensure fresh import
import subprocess
result = subprocess.run([
    sys.executable, '-c', '''
from app.database import Base, engine

import app.models.user
import app.models.wallet
import app.models.membership
import app.models.digital_human
import app.models.voice
import app.models.script
import app.models.asset
import app.models.video
import app.models.message
import app.models.statistics
import app.models.admin

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Done!")
'''
], cwd=os.path.dirname(os.path.abspath(__file__)))

print(result.stdout)
if result.returncode != 0:
    print(result.stderr)