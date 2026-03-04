# Data Engineering Project #1 — Online Retail



Dit project bouwt een end‑to‑end data‑engineering pipeline op basis van de **Online Retail II** dataset.  

De workflow volgt de **Medallion‑architectuur** (Bronze → Silver → Gold) 

en maakt gebruik van **Python**, **MySQL**, **SQL‑modellering**, **incremental loads** 

en **CI/CD via GitHub Actions**.



## 🔧 Technologieën

- Python (Pandas, SQLAlchemy)  

- MySQL (XAMPP)  

- SQL (CTE’s, CASE, joins, stored procedures)  

- GitHub Actions (CI/CD)  

- Windows Task Scheduler  

- VS Code  



## 📂 Projectstructuur





## 🔄 Pipeline Overzicht

1. **Bronze:** ruwe Excel‑bestanden (gesplitst per jaar).  

2. **Silver:** Python ETL voor cleaning, standaardisatie en validatie → MySQL.  

3. **Gold:** star schema (fact + dimensions) + business KPI’s.  

4. **Incremental loads:** nieuwe bestanden worden verwerkt via stored procedures.  

5. **CI/CD:** automatische checks via GitHub Actions.  

6. **Scheduling:** pipeline kan lokaal automatisch draaien.



## 🎯 Doel

Het doel van dit project is het opzetten van een complete, lokaal draaiende data‑engineering workflow 

die moderne technieken combineert en geschikt is als portfolio‑onderdeel.

