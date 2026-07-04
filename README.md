# Automated Weather ETL Pipeline (Dockerized)

## 📌 Project Overview

This project is an end-to-end **ETL (Extract, Transform, Load) pipeline** that retrieves historical weather data from the **Open-Meteo API**, processes it using Python, and loads it into a **PostgreSQL database running in Docker**.

The pipeline is fully containerized using **Docker Compose**, making it easy to run in any environment with a single command.

---

## ⚙️ Architecture

The system consists of two main services:

- **PostgreSQL database container**
- **ETL container (Python-based pipeline)**

Workflow:


Open-Meteo API → Extract (Python) → Transform (cleaning/formatting) → Load → PostgreSQL


Docker Compose orchestrates both services and ensures the database is ready before the ETL job runs.

---

## 🚀 Features

- Pulls historical weather data from Open-Meteo API
- Cleans and transforms raw JSON data into structured tabular format
- Stores processed data in PostgreSQL
- Fully containerized (no local Python/Postgres setup required)
- Automatic database readiness check before ETL execution
- Re-runnable pipeline (batch ETL job)

---

## 🗂 Project Structure


automated_etl_project/
│
├── src/
│ ├── extract.py # Fetches weather data from Open-Meteo API
│ ├── transform.py # Cleans and transforms raw data into structured format (Parquet/DataFrame)
│ ├── load.py # Loads transformed data into PostgreSQL
│
├── sql_scripts/
│ └── init.sql # (Optional) SQL initialization scripts for DB setup
│
├── docker-compose.yml # Defines PostgreSQL + ETL services
├── Dockerfile # Builds ETL container environment
├── requirements.txt # Python dependencies
└── README.md # Project documentation
