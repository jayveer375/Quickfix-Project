#!/usr/bin/env python3
"""
Import data from old/backup database into the new fresh database.
Tries both database_recovered.db and database_backup.db as sources.
Skips rows that fail (corrupted) and reports what was imported.
"""
import sys, os, sqlite3
sys.path.insert(0, '.')

# ── helpers ──────────────────────────────────────────────────────────────────

def open_db(path):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    # Allow reading even slightly corrupt pages
    conn.execute("PRAGMA integrity_check")
    return conn

def safe_fetchall(conn, sql, params=()):
    try:
        return conn.execute(sql, params).fetchall()
    except Exception as e:
        print(f"  [WARN] Query failed: {e}")
        return []

def get_tables(conn):
    rows = safe_fetchall(conn, "SELECT name FROM sqlite_master WHERE type='table'")
    return [r[0] for r in rows]

# ── main ─────────────────────────────────────────────────────────────────────

# Pick best source — prefer recovered, fall back to backup
SOURCE_CANDIDATES = [
    'instance/database_recovered.db',
    'instance/database_backup.db',
]

src_path = None
for c in SOURCE_CANDIDATES:
    if os.path.exists(c):
        try:
            t = sqlite3.connect(c)
            tables = t.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
            t.close()
            if tables:
                src_path = c
                print(f"Using source DB: {c}  (tables: {[r[0] for r in tables]})")
                break
        except Exception as e:
            print(f"Skipping {c}: {e}")

if not src_path:
    print("ERROR: No readable source database found.")
    sys.exit(1)

# Make sure target DB exists (start the app to create it if not)
TARGET = 'instance/database.db'
if not os.path.exists(TARGET):
    print("Target DB not found — creating it via app factory...")
    from app import create_app, db as flask_db
    app = create_app()
    with app.app_context():
        flask_db.create_all()
    print("Target DB created.\n")

src = sqlite3.connect(src_path)
src.row_factory = sqlite3.Row
dst = sqlite3.connect(TARGET)
dst.row_factory = sqlite3.Row

src_tables = get_tables(src)
dst_tables = get_tables(dst)
print(f"\nSource tables : {src_tables}")
print(f"Target tables : {dst_tables}\n")

# Order matters for FK constraints
TABLE_ORDER = [
    'users',
    'categories',
    'service_providers',
    'services',
    'reviews',
    'favorites',
    'cities',
    'areas',
]

# Tables in source but not in our order list
extra = [t for t in src_tables if t not in TABLE_ORDER and t != 'sqlite_sequence']
TABLE_ORDER += extra

stats = {}

for table in TABLE_ORDER:
    if table not in src_tables:
        continue
    if table not in dst_tables:
        print(f"[SKIP] {table} — not in target schema")
        continue

    # Get columns present in BOTH src and dst
    src_cols = [r[1] for r in src.execute(f"PRAGMA table_info({table})").fetchall()]
    dst_cols = [r[1] for r in dst.execute(f"PRAGMA table_info({table})").fetchall()]
    common_cols = [c for c in src_cols if c in dst_cols]

    if not common_cols:
        print(f"[SKIP] {table} — no common columns")
        continue

    rows = safe_fetchall(src, f"SELECT {','.join(common_cols)} FROM {table}")
    if not rows:
        print(f"[SKIP] {table} — no rows or unreadable")
        continue

    inserted = skipped = 0
    col_str = ', '.join(common_cols)
    placeholders = ', '.join(['?' for _ in common_cols])

    for row in rows:
        values = tuple(row[c] for c in common_cols)

        # Special case: for the 'users' table, skip the old admin and let
        # the app-created admin@gmail.com stay in place.
        if table == 'users':
            email_idx = common_cols.index('email') if 'email' in common_cols else None
            if email_idx is not None:
                email = values[email_idx]
                if email in ('admin@emergency.com', 'admin@gmail.com'):
                    print(f"  [SKIP] users row — admin account '{email}' kept as-is")
                    skipped += 1
                    continue

        try:
            dst.execute(
                f"INSERT OR IGNORE INTO {table} ({col_str}) VALUES ({placeholders})",
                values
            )
            inserted += 1
        except Exception as e:
            skipped += 1
            # Uncomment below to debug individual row errors:
            # print(f"  [ERR] {table} row skipped: {e}")

    dst.commit()
    stats[table] = (inserted, skipped)
    print(f"[OK]   {table:25s}  inserted={inserted}  skipped={skipped}")

src.close()
dst.close()

print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("Import complete! Summary:")
for t, (ins, skp) in stats.items():
    print(f"  {t:25s}  {ins} rows imported,  {skp} skipped")
print("\nAdmin login:")
print("  Email   : admin@gmail.com")
print("  Password: admin@123")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
