"""Database initialization script"""
import os
if os.path.exists('test.db'):
    os.remove('test.db')

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