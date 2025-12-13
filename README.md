# Workout Data Pipeline
*End-to-end Python + SQL ETL pipeline for tracking multi-user workouts with a normalized relational schema.*

I originally built this project because I wanted a simple, reliable way to track workouts for myself and my grandma.
What started as a small personal tool turned into a project that taught me how to think like a data engineer: how to design schemas, validate data, automate workflows, and build something structured enough that even non-technical people can use

# What This Project Does

* Tracks workouts in a normalized SQLite schema

* Logs exercises, sets, reps, weights,dates, and users

* Uses Python scripts to:

            * validate new entries

            * load structured data

            * refresh weekly summaries

* Builds an analysis-ready view (WorkoutDetails) that joins workouts + set data

* Keeps multi-user data organized, consistent, and easy to report on

# Database Schema
![Workout Database Schema](Workout_schema.png)

I designed the schema to be normalized, easy to query, and scalable enough to support dashboards 

## Tables

* Person

* Workout

* SetTable

## View

* WorkoutDetails (joins Workout + SetTable into a clean analysis-ready table)

### Parent-> Child Relationship

* Workout = one workout session

* SetTable = the sets performed within that session

This keeps the data base clean and queries predictable.
 [ Workout ]-> [ SetTable]

# Technologies Used

* SQLite: lightweight and perfect for personal data tracking

* Python: ETL, validation, loading, and automation

* SQL: queries, views, schema design

# Why I Built It This Way

I wanted this to feel like a real, structured data system rather than a one-off notebook script. So I focused on:

* Clean, normalized schema design

* Predictable naming conventions

* Data validation (especially important when tracking grandma’s sets!)

* Reproducible workflows

* A structure that could power a dashboard or small app

This project helped bridge the gap between academic exercises and real-world data engineering. More importantly, it’s something my grandma and I actually use; which pushed me to care about data quality, reliability, and clarity in a very real way.


# How to Run the Project


Clone the repo:
git clone <repo-url>


Install requirements (if added in the future):
pip install -r requirements.txt


Run the ETL script:
python run_etl.py


Open workout.db in any SQLite viewer to explore the tables.
