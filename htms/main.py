import os
from datetime import date as date_obj
from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr, Field
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="HRMS Lite")
templates = Jinja2Templates(directory="templates")

# --- DATABASE CONNECTION ---
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/hrms_lite")
client = AsyncIOMotorClient(MONGO_URI)
db = client.hrms_lite
employees_collection = db.employees
attendance_collection = db.attendance

# --- MODELS ---
class EmployeeModel(BaseModel):
    employee_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=2)
    email: EmailStr
    department: str = Field(..., min_length=2)

class AttendanceModel(BaseModel):
    employee_id: str
    date: str
    status: str

# --- FRONTEND ROUTE ---
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# --- API ROUTES ---

# 1. GET DASHBOARD STATS (Bonus Feature)
@app.get("/api/dashboard")
async def get_dashboard_stats():
    total_employees = await employees_collection.count_documents({})
    # Count how many marked "Present" today
    today_str = str(date_obj.today())
    present_today = await attendance_collection.count_documents({"date": today_str, "status": "Present"})
    
    return {
        "total_employees": total_employees,
        "present_today": present_today
    }

# 2. GET ALL EMPLOYEES + TOTAL PRESENT DAYS (Bonus Feature)
@app.get("/api/employees")
async def get_employees():
    employees = []
    cursor = employees_collection.find({})
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        # Bonus: Count total 'Present' days for this employee
        present_count = await attendance_collection.count_documents({
            "employee_id": doc["employee_id"], 
            "status": "Present"
        })
        doc["total_present"] = present_count
        employees.append(doc)
    return employees

# 3. ADD EMPLOYEE
@app.post("/api/employees", status_code=201)
async def add_employee(employee: EmployeeModel):
    existing = await employees_collection.find_one({
        "$or": [{"employee_id": employee.employee_id}, {"email": employee.email}]
    })
    if existing:
        raise HTTPException(status_code=400, detail="Employee ID or Email already exists")
    await employees_collection.insert_one(employee.dict())
    return {"message": "Created"}

# 4. DELETE EMPLOYEE
@app.delete("/api/employees/{employee_id}")
async def delete_employee(employee_id: str):
    res = await employees_collection.delete_one({"employee_id": employee_id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Not Found")
    await attendance_collection.delete_many({"employee_id": employee_id})
    return {"message": "Deleted"}

# 5. GET ATTENDANCE (With Optional Date Filter) (Bonus Feature)
@app.get("/api/attendance/{employee_id}")
async def get_attendance(employee_id: str, date: str = Query(None)):
    query = {"employee_id": employee_id}
    if date:
        query["date"] = date  # Filter by specific date if provided
    
    records = []
    cursor = attendance_collection.find(query).sort("date", -1)
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        records.append(doc)
    return records

# 6. MARK ATTENDANCE
@app.post("/api/attendance")
async def mark_attendance(attendance: AttendanceModel):
    await attendance_collection.update_one(
        {"employee_id": attendance.employee_id, "date": attendance.date},
        {"$set": attendance.dict()},
        upsert=True
    )
    return {"message": "Attendance marked"}