# HRMS Lite - Full Stack Assessment

## 📌 Project Overview
HRMS Lite is a lightweight Human Resource Management System designed to help administrators manage employee records and track daily attendance. The application features a clean, responsive user interface and a robust RESTful API backend.

**Key Features:**
- **Employee Management:** Add, view, and delete employees with validation (unique ID/Email).
- **Attendance Tracking:** Mark daily attendance (Present/Absent) and view history.
- **Dashboard:** Real-time summary of total employees and daily attendance stats.
- **Filtering:** Filter attendance history by specific dates.

## 🛠️ Tech Stack
- **Backend:** Python (FastAPI)
- **Database:** MongoDB (Motor Async Driver)
- **Frontend:** HTML5, Jinja2 Templates, JavaScript (Fetch API)
- **Styling:** Pico.css (Minimalist Responsive Framework)
- **Deployment:** Vercel (Serverless)

## 🚀 Steps to Run Locally

1. **Clone the Repository**
   ```bash
   git clone [https://github.com/rk17-max/Employee_management.git](https://github.com/rk17-max/Employee_management.git)
   cd Employee_management


2.Set Up Virtual Environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

3.Install dependencies
pip install -r requirements.txt

4.Configure Environment Variables Create a .env file in the root directory and add your MongoDB connection string:
MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority

5.Run the Server
uvicorn main:app --reload
