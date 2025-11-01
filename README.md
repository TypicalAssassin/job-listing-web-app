# Job Listing Web App

A full-stack web application that scrapes actuarial job listings.

# Prerequisites

Make sure you have the following installed:

Python 3.10.0

Node.js v22.16.0

MySQL 8.0 (installed and running)

# -> 1. Setup Database ----------------------------
Access MySQL

mysql -u root -p

In MySQL shell

CREATE DATABASE job_listing_db;

EXIT;

# -> 2. Setup Backend ----------------------------
cd backend

python -m venv myenv

myenv\Scripts\activate

pip install -r requirements.txt


Create a .env file inside the backend directory with the following content:

DB_USER=root

DB_PASSWORD=your_actual_db_password

DB_HOST=localhost

DB_PORT=3306

DB_NAME=job_listing_db


Then run:

python app.py

You should see:

Database tables created successfully!


Keep this terminal running.

# -> 3. Setup Frontend ----------------------------

Open a new terminal and run:

cd frontend

npm install

Create a .env file inside the frontend directory with the following content:

REACT_APP_API_BASE_URL=http://localhost:5000/api

Then run:

npm start


Your browser will open automatically at:
http://localhost:3000

Keep this terminal running as well.

# -> 4. Run Scraper ----------------------------

Open another new terminal (use the same Python virtual environment you created earlier):

cd Scraper

..\backend\myenv\Scripts\activate

python scrape.py


This will scrape est: 300 actuarial jobs from actuarylist.com and store them in the database.

# Access the App

Visit your frontend in the browser:

http://localhost:3000

# Notes:

The backend API runs at http://127.0.0.1:5000

The frontend (React) runs at http://localhost:3000

Make sure MySQL is running before starting the backend or scraper.