# Multi-System Data Quality Audit

An end-to-end data quality audit across three interconnected systems, from SQL profiling and issue identification through to a structured presentation of findings and recommendations. The scenario simulates a pre-migration audit in a higher education context, with regulatory compliance (HESA returns) as the underlying business driver.

---

## Scenario

A university holds student records across three separate systems that have grown misaligned over time. Before a major system transformation can proceed, the data quality issues must be identified, categorised, and prioritised.

| System | Contents |
|---|---|
| Student Record System (SRS) | Master record: ID, name, DOB, programme, enrolment status, nationality |
| Finance System | Fee status, tuition liability, bursary flags |
| Learning Management System (LMS) | Module enrolments, login and engagement data |

The data is synthetic and was generated to replicate realistic data quality issues. Each system uses its own identifier format (SRS00001, FIN00001, s00001), with no shared key across systems. This inconsistency is itself a data quality issue.

---

## Tech Stack

- **DuckDB:** in-process SQL analytical database
- **Python:** data generation and notebook environment
- **Jupyter Notebook:** analysis workbook
- **SQL:** profiling, validation, cross-system joins

---

## Data Quality Issues Identified

| ID | System | Issue | Scale | Category |
|---|---|---|---|---|
| DQ-1 | SRS | Missing nationality | ~10% (1,500 rows) | Completeness, HESA compliance risk |
| DQ-2 | SRS | Duplicate student records | ~0.5% (75 rows) | Uniqueness, migration artefact |
| DQ-3 | Finance | DOB mismatches vs SRS | ~1% (150 rows) | Accuracy, day/month transposition |
| DQ-4 | Finance | Ghost records not in SRS | ~3% (450 rows) | Consistency, purge process failure |
| DQ-5 | Finance | Fee-status conflicts vs SRS | ~2% (300 rows) | Consistency, HESA funding risk |
| DQ-6 | LMS | Students with no account | ~6% (900 rows) | Completeness, onboarding failure |
| DQ-7 | LMS | Withdrawn students still active | ~50% of withdrawn (739 rows) | Consistency, deactivation process failure |
| DQ-8 | LMS | Null account_status | ~4% (564 rows) | Completeness, incomplete migration |

---

## Project Structure

```
multi-system-data-quality-audit/
├── data/
│   ├── srs.csv                  # Student Record System
│   ├── finance.csv              # Finance System
│   ├── lms.csv                  # Learning Management System
│   └── generate_data.py         # Synthetic data generator
├── notebooks/
│   └── student_dq_analysis.ipynb  # Main analysis workbook
├── screenshots/                 # Query outputs and visualisations
├── Student Data Quality Analysis.pptx  # Presentation
└── README.md
```

---

## Analysis Overview

The notebook covers:

1. **Data landscape:** row counts and field inventory across all three systems
2. **Null rate profiling:** completeness check per field per system
3. **Duplicate checks:** duplicate IDs and duplicate persons
4. **Value distribution analysis:** enrolment status, fee status, programme, nationality, login activity
5. **Cross-system analysis:** ID linkage, population overlaps, fee-status conflicts *(in progress)*
6. **Issue register:** structured summary of all findings with severity and category *(in progress)*

---

## Key Findings (Completed Sections)

- Every inactive LMS account has a null last login date (1,287 records). Nulls are not random, they follow account status exactly.
- 564 records have a null account_status in LMS despite most having a login date, likely an incomplete migration.
- Fee-status field uses inconsistent values across SRS and Finance (e.g. Home vs H, Overseas vs O).
- Nationality field in SRS has a ~10% null rate, a direct HESA compliance risk.

---

## Screenshots

Selected query outputs from the analysis:

| | |
|---|---|
| ![Row counts](screenshots/row_count.png) | ![Field inventory](screenshots/Field_inventory.png) |
| ![Issue register](screenshots/issue_reg.png) | ![Account status distribution](screenshots/account_status_value_distribution.png) |
| ![Finance not in SRS](screenshots/finance_not_in_srs.png) | ![Last login nulls](screenshots/last_login_and_account_nulls.png) |

---

## How to Run

1. Clone the repo
2. Install dependencies: `pip install duckdb jupyter`
3. Open `notebooks/student_dq_analysis.ipynb` and run cells in order

The CSVs in `data/` are loaded directly into DuckDB at runtime. No database setup required.
