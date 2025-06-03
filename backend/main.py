# main.py

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from crud import get_all_attendance, get_all_employees
from models import AttendanceLogItem, EmployeeDetailsItem
from typing import List
from datetime import datetime, timedelta
from collections import defaultdict

app = FastAPI()

# Allow requests from Angular frontend (adjust if hosted elsewhere)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your Angular app domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/attendance", response_model=List[AttendanceLogItem])
def attendance():
    return get_all_attendance()

@app.get("/employees", response_model=List[EmployeeDetailsItem])
def employees():
    return get_all_employees()

@app.get("/attendance/stats")
def attendance_stats():
    attendance = get_all_attendance()
    employees = get_all_employees()

    total_employees = len(employees)
    
    today = datetime.now().date()
    todays_attendance = sum(
        1 for entry in attendance if datetime.fromisoformat(entry["Timestamp"]).date() == today
    )

    attendance_rate = (todays_attendance / total_employees) * 100 if total_employees > 0 else 0

    return {
        "totalEmployees": total_employees,
        "todaysAttendance": todays_attendance,
        "attendanceRate": round(attendance_rate, 2),
    }

@app.get("/attendance/recent", response_model=List[AttendanceLogItem])
def recent_attendance_logs(limit: int = 5):
    attendance = sorted(get_all_attendance(), key=lambda x: x["Timestamp"], reverse=True)
    return attendance[:limit]

@app.get("/attendance/by-date")
def attendance_by_date_range(
    start_date: str = Query(...),
    end_date: str = Query(...)
):
    """
    Get attendance data for a specific date range.
    For dashboard chart visualization - returns aggregated count by date.
    """
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
    except ValueError:
        return {"error": "Invalid date format. Use ISO 8601 format."}

    attendance = get_all_attendance()
    grouped = defaultdict(int)

    for entry in attendance:
        ts = datetime.fromisoformat(entry["Timestamp"])
        if start <= ts <= end:
            date_str = ts.date().isoformat()
            grouped[date_str] += 1

    # Format data as an array for charts
    result = [{"date": date, "count": count} for date, count in grouped.items()]
    result.sort(key=lambda x: x["date"])
    return result

@app.get("/attendance/by-date/records", response_model=List[AttendanceLogItem])
def attendance_records_by_date_range(
    start_date: str = Query(...),
    end_date: str = Query(...)
):
    """
    Get detailed attendance records for a specific date range.
    For attendance page table view - returns individual attendance records.
    """
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
    except ValueError:
        return {"error": "Invalid date format. Use ISO 8601 format."}

    attendance = get_all_attendance()
    filtered_records = []

    for entry in attendance:
        ts = datetime.fromisoformat(entry["Timestamp"])
        if start <= ts <= end:
            filtered_records.append(entry)
    
    # Sort by timestamp descending (newest first)
    filtered_records.sort(key=lambda x: x["Timestamp"], reverse=True)
    return filtered_records