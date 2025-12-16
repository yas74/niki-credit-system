# Niki – Staff Credit & Loan System

Niki is a backend system for managing staff loans based on performance scoring, eligibility rules, and limited shared credit.

This project is built as a **portfolio project** to explore real-world backend system design around financial logic, fairness, and internal tooling.

---

## What Niki Does

Niki allows staff members to:

- Accumulate scores based on defined criteria
- See their total score and how it’s calculated
- Request loans based on eligibility and limits
- Repay loans gradually through monthly salary deductions
- Track loan status, repayments, and remaining balance

At the same time, the system enforces clear rules around who can borrow, how much, and when.

---

## Core Ideas

- **Loans, not handouts**  
  Money is borrowed and repaid in small monthly installments, preserving dignity and responsibility.

- **Motivation through scoring**  
  Performance-related criteria contribute to a score that directly affects loan eligibility and limits.

- **Fairness and transparency**  
  Scores, rules, limits, and loan status are visible and predictable for everyone.

---

## Competition Model

Niki operates with a **limited shared credit pool**.

When multiple people are eligible, those with higher scores can access loans sooner.  
This introduces controlled competition without removing clarity or fairness.

---

## Key Features

- Weighted scoring system with configurable criteria
- Eligibility rules for loan access and limits
- Monthly installment-based repayment logic
- Loan request and approval workflow
- Full visibility into scores, loans, and repayment status
- Admin-defined rules and thresholds

---

## Tech Stack

- **Backend:** Python (FastAPI)
- **Database:** MongoDB
- **Architecture:** API-first, domain-oriented design
- **Auth:** Token-based authentication (planned)
- **Status:** Early design & development phase

---

## Project Status

This project is currently in **active design and early implementation**.  
The focus is on:

- Data modeling
- Core business rules
- Clean and maintainable backend structure

---

## Author

Built by **Yasaman Rohani** as a backend-focused portfolio project.
