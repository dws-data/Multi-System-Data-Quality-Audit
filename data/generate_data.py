import pandas as pd
import numpy as np
import random
from datetime import date, timedelta

random.seed(42)
np.random.seed(42)

# ── Core population ───────────────────────────────────────────────────────────
N = 15_000
ids = [f"{i:05d}" for i in range(1, N + 1)]

first_names_m = [
    "James","Oliver","Harry","Jack","George","Noah","Charlie","Jacob","Alfie","Freddie",
    "Muhammad","Thomas","Oscar","William","Henry","Edward","Ethan","Joshua","Lucas","Mason",
    "Daniel","Matthew","Joseph","Samuel","Benjamin","Alexander","Ryan","Nathan","Adam","Luke",
    "Owen","Dylan","Liam","Sebastian","Theo","Reuben","Elliot","Toby","Dominic","Patrick",
    "Callum","Cameron","Connor","Kieran","Marcus","Leon","Joel","Jude","Felix","Hugo",
    "Max","Finn","Rory","Ellis","Emre","Tariq","Rohan","Arjun","Kai","Zac",
    "Ibrahim","Yusuf","Omar","Ali","Hassan","Bilal","Aiden","Cian","Rhys","Niall"
]
first_names_f = [
    "Olivia","Amelia","Isla","Ava","Emily","Isabella","Mia","Poppy","Ella","Grace",
    "Sophia","Lily","Freya","Sophie","Evie","Charlotte","Alice","Millie","Jessica","Layla",
    "Hannah","Eleanor","Georgia","Zoe","Chloe","Natalie","Rebecca","Laura","Sarah","Kate",
    "Imogen","Harriet","Bethany","Abigail","Molly","Phoebe","Amber","Jasmine","Ellie","Rosa",
    "Priya","Aisha","Fatima","Zara","Nadia","Leila","Yasmin","Seren","Niamh","Aoife",
    "Megan","Cerys","Siobhan","Erin","Roisin","Anna","Clara","Madeleine","Pippa","Verity",
    "Harriet","Claudia","Isobel","Cara","Nadia","Miriam","Leah","Naomi","Ruth","Maya"
]
last_names    = [
    "Smith","Jones","Williams","Taylor","Brown","Davies","Evans","Wilson","Thomas","Roberts",
    "Johnson","Lewis","Walker","Robinson","Wood","Thompson","White","Watson","Jackson","Harris",
    "Martin","Clarke","Hall","Turner","Ahmed","Khan","Patel","Ali","Singh","Chen",
    "Hughes","Price","Edwards","Morgan","Ward","Cooper","Richardson","Cox","Howard","Mitchell",
    "Collins","Shaw","James","Brooks","Graham","Stewart","Murray","Reid","Campbell","Ross",
    "Hussain","Mahmood","Rahman","Islam","Begum","Kaur","Shah","Sharma","Gupta","Kumar",
    "Park","Kim","Lee","Wong","Chan","Ng","Lam","Ho","Cheung","Yip",
    "Murphy","O'Brien","Walsh","Ryan","O'Sullivan","McCarthy","Doherty","Byrne","Flynn","Brady",
    "Andersson","Nielsen","Hansen","Petersen","Larsen","Svensson","Berg","Lindqvist","Holm","Eriksson",
    "Ferrari","Romano","Ricci","Greco","Esposito","Bianchi","Fontana","Costa","Mancini","Conti",
    "Okafor","Osei","Mensah","Owusu","Asante","Diallo","Toure","Diop","Ndiaye","Bah",
    "Hassan","Abdi","Omar","Mohamed","Hussein","Yusuf","Ibrahim","Farah","Warsame","Jama"
]

genders     = np.random.choice(["M","F"], N)
first_names = [random.choice(first_names_m if g == "M" else first_names_f) for g in genders]
last_names_ = [random.choice(last_names) for _ in range(N)]

def random_dob():
    start = date(1990, 1, 1)
    return start + timedelta(days=random.randint(0, (date(2007, 12, 31) - start).days))

dobs = [random_dob() for _ in range(N)]

# Nationality — ~70% GBR, rest international (proportional to N)
nat_pool = (["GBR"] * int(N*0.70) + ["CHN"] * int(N*0.08) + ["IND"] * int(N*0.05) +
            ["NGA"] * int(N*0.03) + ["USA"] * int(N*0.02) + ["PAK"] * int(N*0.02) +
            ["MYS"] * int(N*0.02) + ["ITA"] * int(N*0.02) + ["DEU"] * int(N*0.02) +
            ["ZWE"] * int(N*0.02) + ["IRN"] * int(N*0.02))[:N]
random.shuffle(nat_pool)
nationalities = nat_pool

domiciles = [
    random.choice(["England"] * 8 + ["Wales", "Scotland", "Northern Ireland"])
    if n == "GBR" else "Overseas"
    for n in nationalities
]

programmes = [
    ("BSC_COMPSCI", "BSc Computer Science"),
    ("BSC_BUS",     "BSc Business Management"),
    ("BA_ENG",      "BA English Literature"),
    ("BSC_PSYCH",   "BSc Psychology"),
    ("MENG_CIVIL",  "MEng Civil Engineering"),
    ("BSC_NURS",    "BSc Nursing"),
    ("BA_HIST",     "BA History"),
    ("BSC_MATHS",   "BSc Mathematics"),
    ("MSC_DATA",    "MSc Data Science"),
    ("MBA",         "MBA Business Administration"),
]
prog_idx   = np.random.randint(0, len(programmes), N)
prog_codes = [programmes[i][0] for i in prog_idx]
prog_names = [programmes[i][1] for i in prog_idx]

statuses_srs = list(np.random.choice(
    ["Active", "Withdrawn", "Suspended", "Deferred"],
    N, p=[0.82, 0.10, 0.04, 0.04]
))

fee_status = ["Home" if n == "GBR" else "Overseas" for n in nationalities]

def random_enrol_date():
    year = random.choice([2022, 2023, 2024, 2025])
    return date(year, 9, random.randint(15, 30))

enrol_dates = [random_enrol_date() for _ in range(N)]
end_dates   = [date(d.year + random.choice([3, 4]), 6, 30) for d in enrol_dates]


# ── SRS ───────────────────────────────────────────────────────────────────────
srs = pd.DataFrame({
    "student_id":       [f"SRS{i}" for i in ids],
    "first_name":       first_names,
    "last_name":        last_names_,
    "date_of_birth":    dobs,
    "nationality":      nationalities,
    "domicile":         domiciles,
    "programme_code":   prog_codes,
    "programme_name":   prog_names,
    "enrolment_status": statuses_srs,
    "fee_status":       fee_status,
    "enrolment_date":   enrol_dates,
    "expected_end_date":end_dates,
})

# DQ-1  Missing nationality (~10%) — HESA compliance risk
n_missing_nat = int(N * 0.10)
srs.loc[random.sample(range(N), n_missing_nat), "nationality"] = None

# DQ-2  Duplicate student records ~0.5% (migration artefact — same person, two IDs)
n_dupes = int(N * 0.005)
dupes = srs.sample(n_dupes, random_state=1).copy()
dupes["student_id"] = [f"SRS{i:05d}" for i in range(N + 1, N + 1 + n_dupes)]
srs = pd.concat([srs, dupes], ignore_index=True)

srs.to_csv("srs.csv", index=False)
print(f"SRS:     {len(srs):>4} rows")


# ── Finance ───────────────────────────────────────────────────────────────────
fin_status_map = {"Active":"Enrolled","Withdrawn":"Inactive",
                  "Suspended":"Suspended","Deferred":"Deferred"}

finance = pd.DataFrame({
    "student_ref":       [f"FIN{i}" for i in ids],          # different ID prefix
    "first_name":        first_names,
    "last_name":         last_names_,
    "date_of_birth":     dobs,
    "fee_status":        ["H" if f == "Home" else "O" for f in fee_status],  # different coding
    "tuition_fee_amount":[9250 if f == "Home"
                          else random.choice([15000,18000,21000,24000])
                          for f in fee_status],
    "bursary_flag":      np.random.choice(["Y","N"], N, p=[0.15,0.85]),
    "payment_status":    np.random.choice(["Paid","Partial","Outstanding"], N, p=[0.65,0.20,0.15]),
    "enrolment_status":  [fin_status_map[s] for s in statuses_srs],
    "academic_year":     "2025/26",
})

# DQ-3  DOB mismatches ~1% (day/month transposition — data-entry errors)
n_dob_mismatch = int(N * 0.01)
for idx in random.sample(range(N), n_dob_mismatch):
    d = dobs[idx]
    if d.month <= 12 and d.day <= 12:
        finance.loc[idx, "date_of_birth"] = date(d.year, d.day, d.month)
    else:
        finance.loc[idx, "date_of_birth"] = date(d.year + 1, d.month, d.day)

# DQ-4  Ghost records ~3% — students in Finance but not in SRS
#        (withdrawn students whose SRS record was purged but Finance was not cleaned up)
n_ghosts = int(N * 0.03)
ghost_ids = [f"{i:05d}" for i in range(N + 1 + n_dupes, N + 1 + n_dupes + n_ghosts)]
ghost_rows = pd.DataFrame({
    "student_ref":       [f"FIN{i}" for i in ghost_ids],
    "first_name":        [random.choice(first_names_m + first_names_f) for _ in range(n_ghosts)],
    "last_name":         [random.choice(last_names) for _ in range(n_ghosts)],
    "date_of_birth":     [random_dob() for _ in range(n_ghosts)],
    "fee_status":        np.random.choice(["H","O"], n_ghosts),
    "tuition_fee_amount":np.random.choice([9250,15000,18000], n_ghosts),
    "bursary_flag":      np.random.choice(["Y","N"], n_ghosts),
    "payment_status":    np.random.choice(["Paid","Partial","Outstanding"], n_ghosts),
    "enrolment_status":  "Inactive",
    "academic_year":     "2025/26",
})
finance = pd.concat([finance, ghost_rows], ignore_index=True)

# DQ-5  Fee-status mismatches ~2% vs SRS (Home in SRS → O in Finance, or vice versa)
n_fee_mismatch = int(N * 0.02)
for idx in random.sample(range(N), n_fee_mismatch):
    finance.loc[idx, "fee_status"] = "O" if finance.loc[idx, "fee_status"] == "H" else "H"

finance.to_csv("finance.csv", index=False)
print(f"Finance: {len(finance):>4} rows")


# ── LMS ───────────────────────────────────────────────────────────────────────
# Programme names differ from SRS — free-text, inconsistent capitalisation/ordering
lms_prog_map = {
    "BSC_COMPSCI":"Computer Science BSc",
    "BSC_BUS":    "Business Management BSc",
    "BA_ENG":     "English Literature BA",
    "BSC_PSYCH":  "Psychology (BSc)",
    "MENG_CIVIL": "Civil Engineering MEng",
    "BSC_NURS":   "Nursing BSc",
    "BA_HIST":    "History BA",
    "BSC_MATHS":  "Mathematics BSc",
    "MSC_DATA":   "Data Science MSc",
    "MBA":        "MBA",
}

# DQ-6  ~6% of students never set up in LMS (deferred + some late enrolments)
n_not_in_lms  = int(N * 0.06)
deferred_idx  = [i for i in range(N) if statuses_srs[i] == "Deferred"]
extras_needed = max(0, n_not_in_lms - len(deferred_idx))
other_idx     = [i for i in range(N) if i not in deferred_idx]
not_in_lms    = set(deferred_idx + random.sample(other_idx, extras_needed))
in_lms        = [i for i in range(N) if i not in not_in_lms]

lms = pd.DataFrame({
    "lms_id":         [f"s{ids[i]}" for i in in_lms],   # different ID prefix again
    "username":       [f"{first_names[i][0].lower()}{last_names_[i].lower()}"
                       f"{random.randint(1000000,9999999)}@university.ac.uk" for i in in_lms],
    "programme":      [lms_prog_map.get(prog_codes[i], prog_codes[i]) for i in in_lms],
    "modules_enrolled":np.random.randint(4, 9, len(in_lms)),
    "last_login_date":[(date(2026,5,1) - timedelta(days=random.randint(0,30))).isoformat()
                       if statuses_srs[i] == "Active" else None for i in in_lms],
    "account_status": ["Active" if statuses_srs[i] == "Active" else "Inactive" for i in in_lms],
})

# DQ-7  ~50% of withdrawn students still Active in LMS (deactivation process not followed)
withdrawn_in_lms = [j for j, i in enumerate(in_lms) if statuses_srs[i] == "Withdrawn"]
n_still_active   = int(len(withdrawn_in_lms) * 0.50)
for j in random.sample(withdrawn_in_lms, n_still_active):
    lms.loc[j, "account_status"]  = "Active"
    lms.loc[j, "last_login_date"] = (date(2026,5,1) - timedelta(days=random.randint(0,60))).isoformat()

# DQ-8  ~4% null account_status values (incomplete LMS migration records)
n_null_status = int(len(in_lms) * 0.04)
lms.loc[random.sample(range(len(in_lms)), n_null_status), "account_status"] = None

lms.to_csv("lms.csv", index=False)
print(f"LMS:     {len(lms):>4} rows")

print("\nDQ issues seeded:")
print(f"  DQ-1  SRS:     {n_missing_nat} missing nationality values (~10%, HESA compliance)")
print(f"  DQ-2  SRS:     {n_dupes} duplicate student records (~0.5%, migration artefact)")
print(f"  DQ-3  Finance: {n_dob_mismatch} DOB mismatches vs SRS (~1%, day/month transposition)")
print(f"  DQ-4  Finance: {n_ghosts} ghost records not present in SRS (~3%)")
print(f"  DQ-5  Finance: {n_fee_mismatch} fee-status mismatches vs SRS (~2%)")
print(f"  DQ-6  LMS:     {n_not_in_lms} students with no LMS account (~6%, never set up)")
print(f"  DQ-7  LMS:     {n_still_active} withdrawn students still Active in LMS (~50% of withdrawn)")
print(f"  DQ-8  LMS:     {n_null_status} null account_status values (~4%)")
