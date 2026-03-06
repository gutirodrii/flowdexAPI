"""
Diagnostic script: checks DB column types and tests login query directly.
Run with: python test_db.py
"""
import asyncio
import asyncpg
from dotenv import dotenv_values


async def main():
    env = dotenv_values(".env")
    raw_url = env["DATABASE_URL"]

    # asyncpg needs postgresql:// not postgresql+asyncpg://
    asyncpg_url = raw_url.replace("postgresql+asyncpg://", "postgresql://")

    print(f"Connecting to: {asyncpg_url}\n")

    conn = await asyncpg.connect(asyncpg_url, statement_cache_size=0)

    # 1. Check actual column types in the DB
    print("=== Column types for 'usuarios' ===")
    rows = await conn.fetch("""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_name = 'usuarios'
        ORDER BY ordinal_position
    """)
    for r in rows:
        print(f"  {r['column_name']}: {r['data_type']} (nullable={r['is_nullable']})")

    # 2. Test the SELECT that was failing
    print("\n=== Testing SELECT query ===")
    try:
        rows = await conn.fetch(
            "SELECT usuario_id, email, last_login_at, created_at FROM usuarios LIMIT 3"
        )
        print(f"  OK — {len(rows)} rows returned")
        for r in rows:
            print(f"    email={r['email']}  last_login_at={r['last_login_at']}  created_at={r['created_at']}")
    except Exception as e:
        print(f"  ERROR: {e}")

    # 3. Test UPDATE with a timezone-aware datetime
    print("\n=== Testing UPDATE with timezone-aware datetime ===")
    from datetime import datetime, timezone
    now_tz = datetime.now(timezone.utc)
    try:
        result = await conn.execute(
            "UPDATE usuarios SET last_login_at = $1 WHERE email = $2",
            now_tz, "admin@flowdex.com"
        )
        print(f"  OK — {result}")
    except Exception as e:
        print(f"  ERROR: {e}")

    await conn.close()
    print("\nDone.")


asyncio.run(main())
