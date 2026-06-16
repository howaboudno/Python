import sys
sys.path.insert(0, '.')

import openpyxl
from backend.core.database import SessionLocal
from backend.models.models import User, Fixture, FixturePrediction

EXCEL_PATH = "WK_2026_PREDICKS.xlsx"
TOURNAMENT_ID = 1
PLAYERS = ["aboud", "ivan", "gosia", "antoine", "ridon", "petey", "alex", "elyas"]
BLOCK_START = [11, 21, 31, 41, 51, 61, 71, 81]

db = SessionLocal()

try:
    # Load users
    users = {u.username: u for u in db.query(User).all()}
    missing = [p for p in PLAYERS if p not in users]
    if missing:
        print(f"Missing users: {missing}")
        sys.exit(1)

    # Load all fixtures for this tournament keyed by fixture_number
    fixtures = db.query(Fixture).filter(Fixture.tournament_id == TOURNAMENT_ID).all()
    fixture_map = {int(f.fixture_number): f.id for f in fixtures}
    print(f"Found {len(fixture_map)} fixtures in database")

    # Read Excel
    wb = openpyxl.load_workbook(EXCEL_PATH, data_only=True)
    ws = wb["Predictions"]
    rows = list(ws.iter_rows(values_only=True))

    # Find match rows by match number in column index 1
    match_rows = {}
    for i, row in enumerate(rows):
        val = row[1]
        if val is None:
            continue
        try:
            match_num = int(float(str(val)))
            if 1 <= match_num <= 72:
                match_rows[match_num] = i
        except (ValueError, TypeError):
            pass

    print(f"Found {len(match_rows)} match rows in sheet")

    inserted = 0
    updated = 0
    skipped = 0

    for match_num, row_idx in sorted(match_rows.items()):
        row = rows[row_idx]
        fixture_db_id = fixture_map.get(match_num)

        if not fixture_db_id:
            print(f"  No fixture in DB for match {match_num}, skipping")
            skipped += 1
            continue

        for p_idx, player in enumerate(PLAYERS):
            block = BLOCK_START[p_idx]
            s1 = row[block + 2] if len(row) > block + 2 else None
            s2 = row[block + 3] if len(row) > block + 3 else None

            if s1 is None or s2 is None:
                continue
            try:
                s1 = int(float(str(s1)))
                s2 = int(float(str(s2)))
            except (ValueError, TypeError):
                continue

            user_id = users[player].id

            existing = db.query(FixturePrediction).filter(
                FixturePrediction.user_id == user_id,
                FixturePrediction.fixture_id == fixture_db_id
            ).first()

            if existing:
                existing.predicted_score_1 = s1
                existing.predicted_score_2 = s2
                updated += 1
            else:
                db.add(FixturePrediction(
                    user_id=user_id,
                    fixture_id=fixture_db_id,
                    predicted_score_1=s1,
                    predicted_score_2=s2,
                    predicted_pen_score_1=None,
                    predicted_pen_score_2=None
                ))
                inserted += 1

    db.commit()
    print(f"\nDone.")
    print(f"  Inserted: {inserted}")
    print(f"  Updated:  {updated}")
    print(f"  Skipped:  {skipped}")

    # Verify by checking aboud's predictions
    aboud_id = users['aboud'].id
    aboud_preds = db.query(FixturePrediction).filter(
        FixturePrediction.user_id == aboud_id
    ).count()
    print(f"\nAboud has {aboud_preds} fixture predictions in DB")

except Exception as e:
    db.rollback()
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    raise
finally:
    db.close()