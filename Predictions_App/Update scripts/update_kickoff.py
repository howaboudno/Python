import sys
sys.path.insert(0, '.')

from datetime import datetime, timezone
from backend.core.database import SessionLocal
from backend.models.models import Fixture

# All 72 group stage matches with correct UTC kickoff times
# Format: (fixture_number, utc_datetime)
KICKOFFS = {
    1:  datetime(2026, 6, 11, 19,  0, tzinfo=timezone.utc),  # Mexico vs South Africa
    2:  datetime(2026, 6, 12,  2,  0, tzinfo=timezone.utc),  # Korea Republic vs Czechia
    3:  datetime(2026, 6, 12, 19,  0, tzinfo=timezone.utc),  # Canada vs Bosnia
    4:  datetime(2026, 6, 13,  1,  0, tzinfo=timezone.utc),  # USA vs Paraguay
    5:  datetime(2026, 6, 13, 22,  0, tzinfo=timezone.utc),  # Brazil vs Morocco
    6:  datetime(2026, 6, 13,  4,  0, tzinfo=timezone.utc),  # Australia vs Türkiye
    7:  datetime(2026, 6, 14,  1,  0, tzinfo=timezone.utc),  # Haiti vs Scotland
    8:  datetime(2026, 6, 13, 19,  0, tzinfo=timezone.utc),  # Qatar vs Switzerland
    9:  datetime(2026, 6, 14, 17,  0, tzinfo=timezone.utc),  # Germany vs Curaçao
    10: datetime(2026, 6, 14, 23,  0, tzinfo=timezone.utc),  # Ivory Coast vs Ecuador
    11: datetime(2026, 6, 14, 20,  0, tzinfo=timezone.utc),  # Netherlands vs Japan
    12: datetime(2026, 6, 15,  2,  0, tzinfo=timezone.utc),  # Sweden vs Tunisia
    13: datetime(2026, 6, 15, 19,  0, tzinfo=timezone.utc),  # Belgium vs Egypt
    14: datetime(2026, 6, 16,  1,  0, tzinfo=timezone.utc),  # Iran vs New Zealand
    15: datetime(2026, 6, 15, 16,  0, tzinfo=timezone.utc),  # Spain vs Cape Verde
    16: datetime(2026, 6, 15, 22,  0, tzinfo=timezone.utc),  # Saudi Arabia vs Uruguay
    17: datetime(2026, 6, 16, 19,  0, tzinfo=timezone.utc),  # France vs Senegal
    18: datetime(2026, 6, 16, 22,  0, tzinfo=timezone.utc),  # Iraq vs Norway
    19: datetime(2026, 6, 17,  1,  0, tzinfo=timezone.utc),  # Argentina vs Algeria
    20: datetime(2026, 6, 17,  4,  0, tzinfo=timezone.utc),  # Austria vs Jordan
    21: datetime(2026, 6, 17, 17,  0, tzinfo=timezone.utc),  # Portugal vs DR Congo
    22: datetime(2026, 6, 18,  2,  0, tzinfo=timezone.utc),  # Uzbekistan vs Colombia
    23: datetime(2026, 6, 17, 20,  0, tzinfo=timezone.utc),  # England vs Croatia
    24: datetime(2026, 6, 17, 23,  0, tzinfo=timezone.utc),  # Ghana vs Panama
    25: datetime(2026, 6, 18, 16,  0, tzinfo=timezone.utc),  # Czechia vs South Africa
    26: datetime(2026, 6, 19,  1,  0, tzinfo=timezone.utc),  # Mexico vs Korea Republic
    27: datetime(2026, 6, 18, 19,  0, tzinfo=timezone.utc),  # Switzerland vs Bosnia
    28: datetime(2026, 6, 18, 22,  0, tzinfo=timezone.utc),  # Canada vs Qatar
    29: datetime(2026, 6, 19, 22,  0, tzinfo=timezone.utc),  # Scotland vs Morocco
    30: datetime(2026, 6, 20,  0, 30, tzinfo=timezone.utc),  # Brazil vs Haiti (8:30PM ET)
    31: datetime(2026, 6, 19, 19,  0, tzinfo=timezone.utc),  # USA vs Australia
    32: datetime(2026, 6, 20,  3,  0, tzinfo=timezone.utc),  # Türkiye vs Paraguay
    33: datetime(2026, 6, 20, 20,  0, tzinfo=timezone.utc),  # Germany vs Ivory Coast
    34: datetime(2026, 6, 21,  0,  0, tzinfo=timezone.utc),  # Ecuador vs Curaçao
    35: datetime(2026, 6, 20, 17,  0, tzinfo=timezone.utc),  # Netherlands vs Sweden
    36: datetime(2026, 6, 21,  4,  0, tzinfo=timezone.utc),  # Tunisia vs Japan
    37: datetime(2026, 6, 21, 19,  0, tzinfo=timezone.utc),  # Belgium vs Iran
    38: datetime(2026, 6, 22,  1,  0, tzinfo=timezone.utc),  # New Zealand vs Egypt
    39: datetime(2026, 6, 21, 16,  0, tzinfo=timezone.utc),  # Spain vs Saudi Arabia
    40: datetime(2026, 6, 21, 22,  0, tzinfo=timezone.utc),  # Uruguay vs Cape Verde
    41: datetime(2026, 6, 22, 21,  0, tzinfo=timezone.utc),  # France vs Iraq
    42: datetime(2026, 6, 23,  0,  0, tzinfo=timezone.utc),  # Norway vs Senegal
    43: datetime(2026, 6, 22, 17,  0, tzinfo=timezone.utc),  # Argentina vs Austria
    44: datetime(2026, 6, 23,  3,  0, tzinfo=timezone.utc),  # Jordan vs Algeria
    45: datetime(2026, 6, 23, 17,  0, tzinfo=timezone.utc),  # Portugal vs Uzbekistan
    46: datetime(2026, 6, 24,  2,  0, tzinfo=timezone.utc),  # Colombia vs DR Congo
    47: datetime(2026, 6, 23, 20,  0, tzinfo=timezone.utc),  # England vs Ghana
    48: datetime(2026, 6, 23, 23,  0, tzinfo=timezone.utc),  # Panama vs Croatia
    49: datetime(2026, 6, 25,  1,  0, tzinfo=timezone.utc),  # Czechia vs Mexico
    50: datetime(2026, 6, 25,  1,  0, tzinfo=timezone.utc),  # South Africa vs Korea Republic
    51: datetime(2026, 6, 24, 19,  0, tzinfo=timezone.utc),  # Switzerland vs Canada
    52: datetime(2026, 6, 24, 19,  0, tzinfo=timezone.utc),  # Bosnia vs Qatar
    53: datetime(2026, 6, 24, 22,  0, tzinfo=timezone.utc),  # Scotland vs Brazil
    54: datetime(2026, 6, 24, 22,  0, tzinfo=timezone.utc),  # Morocco vs Haiti
    55: datetime(2026, 6, 26,  2,  0, tzinfo=timezone.utc),  # Türkiye vs USA
    56: datetime(2026, 6, 26,  2,  0, tzinfo=timezone.utc),  # Paraguay vs Australia
    57: datetime(2026, 6, 25, 20,  0, tzinfo=timezone.utc),  # Curaçao vs Ivory Coast
    58: datetime(2026, 6, 25, 20,  0, tzinfo=timezone.utc),  # Ecuador vs Germany
    59: datetime(2026, 6, 25, 23,  0, tzinfo=timezone.utc),  # Japan vs Sweden
    60: datetime(2026, 6, 25, 23,  0, tzinfo=timezone.utc),  # Tunisia vs Netherlands
    61: datetime(2026, 6, 27,  3,  0, tzinfo=timezone.utc),  # Egypt vs Iran
    62: datetime(2026, 6, 27,  3,  0, tzinfo=timezone.utc),  # New Zealand vs Belgium
    63: datetime(2026, 6, 27,  0,  0, tzinfo=timezone.utc),  # Cape Verde vs Saudi Arabia
    64: datetime(2026, 6, 27,  0,  0, tzinfo=timezone.utc),  # Uruguay vs Spain
    65: datetime(2026, 6, 26, 19,  0, tzinfo=timezone.utc),  # Norway vs France
    66: datetime(2026, 6, 26, 19,  0, tzinfo=timezone.utc),  # Senegal vs Iraq
    67: datetime(2026, 6, 28,  2,  0, tzinfo=timezone.utc),  # Jordan vs Argentina
    68: datetime(2026, 6, 28,  2,  0, tzinfo=timezone.utc),  # Algeria vs Austria
    69: datetime(2026, 6, 27, 23, 30, tzinfo=timezone.utc),  # Colombia vs Portugal
    70: datetime(2026, 6, 27, 23, 30, tzinfo=timezone.utc),  # DR Congo vs Uzbekistan
    71: datetime(2026, 6, 27, 21,  0, tzinfo=timezone.utc),  # Panama vs England
    72: datetime(2026, 6, 27, 21,  0, tzinfo=timezone.utc),  # Croatia vs Ghana
}

db = SessionLocal()

try:
    fixtures = db.query(Fixture).filter(Fixture.tournament_id == 1).all()
    fixture_map = {int(f.fixture_number): f for f in fixtures}

    updated = 0
    missing = []

    for match_num, kickoff_utc in KICKOFFS.items():
        fixture = fixture_map.get(match_num)
        if not fixture:
            missing.append(match_num)
            continue
        # Strip tzinfo for SQLite storage (store as naive UTC)
        fixture.fixture_time = kickoff_utc.replace(tzinfo=None)
        updated += 1

    db.commit()
    print(f"Updated {updated} fixtures")
    if missing:
        print(f"Missing fixture numbers: {missing}")

    # Verify a few
    for num in [1, 17, 18, 23]:
        f = fixture_map.get(num)
        if f:
            print(f"  Match {num}: {f.team_1} vs {f.team_2} -> {f.fixture_time} UTC")

except Exception as e:
    db.rollback()
    print(f"Error: {e}")
    raise
finally:
    db.close()