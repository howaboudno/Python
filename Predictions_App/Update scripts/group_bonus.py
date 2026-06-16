import sys
sys.path.insert(0, '.')

import openpyxl
from backend.core.database import SessionLocal
from backend.models.models import User, GroupPrediction, BonusPredictions

EXCEL_PATH = "WK_2026_PREDICKS.xlsx"
TOURNAMENT_ID = 1
PLAYERS = ["aboud", "ivan", "gosia", "antoine", "ridon", "petey", "alex", "elyas"]
BLOCKS = [11, 21, 31, 41, 51, 61, 71, 81]
GROUPS = list("ABCDEFGHIJKL")

# Extended normalisation map covering all typos found in the sheet
TEAM_NAME_MAP = {
    # Countries
    "mexico": "Mexico",
    "south africa": "South Africa",
    "s.africa": "South Africa",
    "korea republic": "South Korea",
    "south korea": "South Korea",
    "s.korea": "South Korea",
    "korea": "South Korea",
    "czechia": "Czech Republic",
    "czech republic": "Czech Republic",
    "czech": "Czech Republic",
    "canada": "Canada",
    "bosnia and herzegovina": "Bosnia & Herz.",
    "bosnia & herz.": "Bosnia & Herz.",
    "bosnia": "Bosnia & Herz.",
    "bih": "Bosnia & Herz.",
    "biH": "Bosnia & Herz.",
    "qatar": "Qatar",
    "switzerland": "Switzerland",
    "swotzerland": "Switzerland",   # petey typo
    "switserland": "Switzerland",
    "brazil": "Brazil",
    "morocco": "Morocco",
    "haiti": "Haiti",
    "scotland": "Scotland",
    "schotland": "Scotland",        # antoine typo
    "schot": "Scotland",
    "united states": "United States",
    "usa": "United States",
    "paraguay": "Paraguay",
    "australia": "Australia",
    "australiq": "Australia",       # alex typo
    "turkey": "Türkiye",
    "turkije": "Türkiye",
    "türkiye": "Türkiye",
    "turky": "Türkiye",
    "germany": "Germany",
    "curaçao": "Curaçao",
    "curacao": "Curaçao",
    "ivory coast": "Ivory Coast",
    "ivc": "Ivory Coast",
    "cote divoire": "Ivory Coast",
    "cote d'ivoire": "Ivory Coast",
    "côte d'ivoire": "Ivory Coast",
    "ecuador": "Ecuador",
    "netherlands": "Netherlands",
    "nederland": "Netherlands",
    "neth": "Netherlands",
    "japan": "Japan",
    "sweden": "Sweden",
    "tunisia": "Tunisia",
    "belgium": "Belgium",
    "belgie": "Belgium",
    "egypt": "Egypt",
    "iran": "Iran",
    "new zealand": "New Zealand",
    "nz": "New Zealand",
    "new zeeland": "New Zealand",   # petey typo
    "spain": "Spain",
    "cape verde": "Cape Verde",
    "cv": "Cape Verde",
    "saudi arabia": "Saudi Arabia",
    "saudi arabie": "Saudi Arabia",
    "saudi": "Saudi Arabia",
    "uruguay": "Uruguay",
    "urugay": "Uruguay",            # petey/alex typo
    "france": "France",
    "senegal": "Senegal",
    "senengal": "Senegal",          # alex typo
    "iraq": "Iraq",
    "norway": "Norway",
    "argentina": "Argentina",
    "arg": "Argentina",
    "argentin": "Argentina",        # petey typo
    "algeria": "Algeria",
    "alergia": "Algeria",           # petey typo
    "austria": "Austria",
    "austra": "Austria",            # gosia typo
    "jordan": "Jordan",
    "portugal": "Portugal",
    "porntugal": "Portugal",        # alex typo
    "portgual": "Portugal",         # petey typo
    "dr congo": "DR Congo",
    "dr. congo": "DR Congo",
    "doctor congo": "DR Congo",
    "congo": "DR Congo",
    "uzbekistan": "Uzbekistan",
    "colombia": "Colombia",
    "england": "England",
    "engeland": "England",          # alex typo
    "croatia": "Croatia",
    "ghana": "Ghana",
    "panama": "Panama",
    # Champion entries
    "spain": "Spain",
    "portugal": "Portugal",
    "netherlands": "Netherlands",
    # Top scorer entries
    "haaland": "Haaland",
    "yamal": "Yamal",
    "ronaldo": "Ronaldo",
    "olise": "Olise",
}

def normalise(name):
    if not name or str(name).strip() in ("", "nan", "None"):
        return None
    cleaned = str(name).strip()
    return TEAM_NAME_MAP.get(cleaned.lower(), cleaned)

db = SessionLocal()

try:
    users = {u.username: u for u in db.query(User).all()}
    missing = [p for p in PLAYERS if p not in users]
    if missing:
        print(f"Missing users: {missing}")
        sys.exit(1)

    wb = openpyxl.load_workbook(EXCEL_PATH, data_only=True)
    ws = wb["Predictions"]
    rows = list(ws.iter_rows(values_only=True))

    # ── GROUP RANKING PREDICTIONS ─────────────────────────────────
    print("Importing group ranking predictions...")
    group_count = 0
    group_start = 84  # Row index where Group A starts

    for g_idx, group in enumerate(GROUPS):
        row = rows[group_start + g_idx]

        for p_idx, player in enumerate(PLAYERS):
            block = BLOCKS[p_idx]
            winner    = normalise(row[block + 1]) if len(row) > block + 1 else None
            runner_up = normalise(row[block + 3]) if len(row) > block + 3 else None
            third     = normalise(row[block + 5]) if len(row) > block + 5 else None

            if not any([winner, runner_up, third]):
                continue

            user_id = users[player].id
            existing = db.query(GroupPrediction).filter(
                GroupPrediction.user_id == user_id,
                GroupPrediction.tournament_id == TOURNAMENT_ID,
                GroupPrediction.group_id == group
            ).first()

            if existing:
                if winner:    existing.first_place  = winner
                if runner_up: existing.second_place = runner_up
                if third:     existing.third_place  = third
            else:
                db.add(GroupPrediction(
                    user_id=user_id,
                    tournament_id=TOURNAMENT_ID,
                    group_id=group,
                    first_place=winner,
                    second_place=runner_up,
                    third_place=third
                ))

            print(f"  {player} Group {group}: {winner} / {runner_up} / {third}")
            group_count += 1

    db.commit()
    print(f"Group predictions done: {group_count} rows")

    # ── BONUS PREDICTIONS ─────────────────────────────────────────
    print("\nImporting bonus predictions...")
    champ_row  = rows[133]
    scorer_row = rows[134]
    bonus_count = 0

    for p_idx, player in enumerate(PLAYERS):
        block = BLOCKS[p_idx]
        champion   = normalise(champ_row[block + 2])  if len(champ_row)  > block + 2 else None
        top_scorer = normalise(scorer_row[block + 2]) if len(scorer_row) > block + 2 else None

        if not champion and not top_scorer:
            print(f"  {player}: no bonus prediction found")
            continue

        user_id = users[player].id
        existing = db.query(BonusPredictions).filter(
            BonusPredictions.user_id == user_id,
            BonusPredictions.tournament_id == TOURNAMENT_ID
        ).first()

        if existing:
            if champion:   existing.predicted_winner     = champion
            if top_scorer: existing.predicted_top_scorer = top_scorer
        else:
            db.add(BonusPredictions(
                user_id=user_id,
                tournament_id=TOURNAMENT_ID,
                predicted_winner=champion or "",
                predicted_top_scorer=top_scorer or ""
            ))

        print(f"  {player}: champion={champion}, top scorer={top_scorer}")
        bonus_count += 1

    db.commit()
    print(f"Bonus predictions done: {bonus_count} rows")
    print("\nAll done!")

except Exception as e:
    db.rollback()
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    raise
finally:
    db.close()