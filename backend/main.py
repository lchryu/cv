from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import json
import os

app = FastAPI(title="CV Admin API", version="1.0.0")

# CORS để frontend có thể gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong production nên chỉ định domain cụ thể
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = "data/cv_data.json"

def load_data():
    """Load CV data from JSON file"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data):
    """Save CV data to JSON file"""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Pydantic models for request validation
class PersonalInfo(BaseModel):
    name: str
    title: str
    phone: str
    email: str
    github: str
    gpa: str

class KeyCourse(BaseModel):
    name: str
    score: str

class Experience(BaseModel):
    title: str
    description: str

class Project(BaseModel):
    name: str
    role: str
    description: str
    technologies: str = ""
    features: str = ""
    team: str = ""
    github: str = ""
    demo: str = ""

class Education(BaseModel):
    university: str
    major: str
    gpa: str

# API Endpoints
@app.get("/")
async def root():
    return {"message": "CV Admin API is running!"}

@app.get("/api/cv-data")
async def get_cv_data():
    """Get all CV data"""
    return load_data()

@app.put("/api/personal-info")
async def update_personal_info(personal_info: PersonalInfo):
    """Update personal information"""
    data = load_data()
    data["personal_info"] = personal_info.dict()
    save_data(data)
    return {"message": "Personal info updated successfully"}

@app.put("/api/introduction")
async def update_introduction(introduction: dict):
    """Update introduction text"""
    data = load_data()
    data["introduction"] = introduction["text"]
    save_data(data)
    return {"message": "Introduction updated successfully"}

@app.put("/api/key-courses")
async def update_key_courses(courses: List[KeyCourse]):
    """Update key courses"""
    data = load_data()
    data["key_courses"] = [course.dict() for course in courses]
    save_data(data)
    return {"message": "Key courses updated successfully"}

@app.put("/api/teaching-experience")
async def update_teaching_experience(experiences: List[Experience]):
    """Update teaching experience"""
    data = load_data()
    data["teaching_experience"] = [exp.dict() for exp in experiences]
    save_data(data)
    return {"message": "Teaching experience updated successfully"}

@app.put("/api/skills")
async def update_skills(skills: List[str]):
    """Update skills list"""
    data = load_data()
    data["skills"] = skills
    save_data(data)
    return {"message": "Skills updated successfully"}

@app.put("/api/projects")
async def update_projects(projects: List[Project]):
    """Update projects"""
    data = load_data()
    data["projects"] = [project.dict() for project in projects]
    save_data(data)
    return {"message": "Projects updated successfully"}

@app.put("/api/education")
async def update_education(education: Education):
    """Update education"""
    data = load_data()
    data["education"] = education.dict()
    save_data(data)
    return {"message": "Education updated successfully"}

@app.put("/api/interests")
async def update_interests(interests: List[str]):
    """Update interests list"""
    data = load_data()
    data["interests"] = interests
    save_data(data)
    return {"message": "Interests updated successfully"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)