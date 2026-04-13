import asyncio
import os
import sys

# Ensure backend directory is in python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.async_database import AsyncSessionLocal
from app.services.auth_service import AuthService
from app.schemas.auth import RegisterInput

async def create_test_user():
    async with AsyncSessionLocal() as db:
        try:
            auth_service = AuthService(db)

            # Fix neon schema manually for profile embedding
            from sqlalchemy import text
            await db.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
            await db.execute(text("ALTER TABLE profiles ADD COLUMN IF NOT EXISTS embedding vector(384);"))
            await db.commit()
            
            test_user = RegisterInput(
                email="test@gmail.com",
                password="Testing123!",
                firstName="Testing",
                lastName="Account"
            )
            
            print(f"[*] Attempting to create test account: {test_user.email}...")
            result = await auth_service.register(test_user)
            print(f"[+] Successfully created test account!")
            print(f"    Email: {result['user']['email']}")
            print(f"    Name: {result['user']['first_name']} {result['user']['last_name']}")
        except Exception as e:
            if "already registered" in str(e).lower() or "unique constraint" in str(e).lower():
                print("[-] Test user already exists.")
            else:
                print(f"[!] Error creating test user: {e}")

if __name__ == "__main__":
    asyncio.run(create_test_user())
