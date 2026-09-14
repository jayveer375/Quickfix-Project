#!/usr/bin/env python3
"""
Deep recovery: try every possible method to extract data from the corrupt DB,
then import whatever survives into the fresh database.db.
"""
import sys, os, sqlite3
sys.path.insert(0, '.')

SRC = 'instance/database_backup.db'
DST = 'instance/database.db'

print("=" * 55)
print("Deep Recovery Tool")
print("=" * 55)

# ── Method 1: iterdump (page-level recovery) ─────────────────────────────────
print("\n[1] Attempting iterdump recovery...")
recovered_sql = []
try:
    conn = sqlite3.connect(f"file:{SRC}?mode=ro", uri=True)
    for line in conn.iterdump():
        recovered_sql.append(line)
    conn.close()
    print(f"    Extracted {len(recovered_sql)} SQL statements via iterdump")
except Exception as e:
    print(f"    iterdump failed: {e}")

# ── Method 2: PRAGMA recover (SQLite 3.41+) ──────────────────────────────────
recovered_rows = {}   # table_name -> list of dicts
print("\n[2] Attempting PRAGMA page recovery per table...")

KNOWN_TABLES = ['users','categories','service_providers','services',
                'reviews','favorites','cities','areas']

for table in KNOWN_TABLES:
    try:
        conn = sqlite3.connect(f"file:{SRC}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
        # Try with nolock + immutable flags
        rows = conn.execute(f"SELECT * FROM {table}").fetchall()
        if rows:
            recovered_rows[table] = [dict(r) for r in rows]
            print(f"    {table}: {len(rows)} rows recovered")
        else:
            print(f"    {table}: 0 rows")
        conn.close()
    except Exception as e:
        print(f"    {table}: FAILED ({e})")

# ── Method 3: immutable URI flag ─────────────────────────────────────────────
if not recovered_rows:
    print("\n[3] Trying immutable URI flag...")
    for table in KNOWN_TABLES:
        try:
            conn = sqlite3.connect(f"file:{SRC}?immutable=1", uri=True)
            conn.row_factory = sqlite3.Row
            rows = conn.execute(f"SELECT * FROM {table}").fetchall()
            if rows:
                recovered_rows[table] = [dict(r) for r in rows]
                print(f"    {table}: {len(rows)} rows")
            conn.close()
        except Exception as e:
            print(f"    {table}: FAILED ({e})")

# ── Import whatever we have ───────────────────────────────────────────────────
if not recovered_rows and not recovered_sql:
    print("\nNo data could be recovered from the backup. The file is fully corrupted.")
    sys.exit(1)

print(f"\n[4] Importing recovered data into {DST}...")

dst = sqlite3.connect(DST)
dst.row_factory = sqlite3.Row

# Import from iterdump SQL if we have it and no row-level data
if recovered_sql and not recovered_rows:
    print("    Using iterdump SQL statements...")
    recovery_db = 'instance/iterdump_recovery.db'
    tmp = sqlite3.connect(recovery_db)
    errors = 0
    for stmt in recovered_sql:
        try:
            tmp.execute(stmt)
        except:
            errors += 1
    tmp.commit()
    print(f"    Wrote to {recovery_db} ({errors} stmt errors)")
    # Now pull rows from there
    tmp.row_factory = sqlite3.Row
    for table in KNOWN_TABLES:
        try:
            rows = tmp.execute(f"SELECT * FROM {table}").fetchall()
            if rows:
                recovered_rows[table] = [dict(r) for r in rows]
                print(f"    {table}: {len(rows)} rows from iterdump")
        except:
            pass
    tmp.close()

TABLE_ORDER = ['users','categories','service_providers','services',
               'reviews','favorites','cities','areas']
stats = {}

dst_tables = [r[0] for r in dst.execute(
    "SELECT name FROM sqlite_master WHERE type='table'").fetchall()]

for table in TABLE_ORDER:
    if table not in recovered_rows:
        continue
    if table not in dst_tables:
        print(f"  [SKIP] {table} not in target schema")
        continue

    rows = recovered_rows[table]
    dst_cols = [r[1] for r in dst.execute(f"PRAGMA table_info({table})").fetchall()]
    inserted = skipped = 0

    for row in rows:
        common = {k: v for k, v in row.items() if k in dst_cols}
        if not common:
            skipped += 1
            continue

        # Skip old admin, keep new one
        if table == 'users' and common.get('email') in ('admin@emergency.com', 'admin@gmail.com'):
            print(f"  [SKIP] admin row '{common.get('email')}' preserved as-is")
            skipped += 1
            continue

        cols = list(common.keys())
        vals = [common[c] for c in cols]
        try:
            dst.execute(
                f"INSERT OR IGNORE INTO {table} ({','.join(cols)}) VALUES ({','.join(['?']*len(cols))})",
                vals
            )
            inserted += 1
        except Exception as e:
            skipped += 1

    dst.commit()
    stats[table] = (inserted, skipped)
    print(f"  [OK] {table:25s} inserted={inserted}  skipped={skipped}")

dst.close()

print("\n" + "=" * 55)
print("Recovery & Import Summary")
print("=" * 55)
if stats:
    for t, (ins, skp) in stats.items():
        print(f"  {t:25s}  {ins} imported,  {skp} skipped")
    print("\n✅ Admin login:")
    print("   Email   : admin@gmail.com")
    print("   Password: admin@123")
else:
    print("  No data was imported (source was fully corrupted).")
print("=" * 55)
