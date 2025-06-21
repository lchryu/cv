from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
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
    profile_image: str = ""

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
    return {"message": "CV Admin API is running!", "version": "1.0.1", "features": ["profile_image_support"]}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "profile_image_support": True}

@app.get("/api/cv-data")
async def get_cv_data():
    """Get all CV data"""
    return load_data()

@app.put("/api/personal-info")
async def update_personal_info(personal_info: PersonalInfo):
    """Update personal information including profile image"""
    try:
        data = load_data()
        personal_dict = personal_info.dict()
        
        # Log for debugging
        if personal_dict.get('profile_image'):
            print(f"📸 Received profile image: {len(personal_dict['profile_image'])} characters")
        
        data["personal_info"] = personal_dict
        save_data(data)
        
        return {
            "message": "Personal info updated successfully", 
            "profile_image_updated": bool(personal_dict.get('profile_image'))
        }
    except Exception as e:
        print(f"❌ Error updating personal info: {e}")
        raise HTTPException(status_code=500, detail=f"Error updating personal info: {str(e)}")

@app.put("/api/profile-image")
async def update_profile_image(image_data: dict):
    """Update only profile image"""
    try:
        if "profile_image" not in image_data:
            raise HTTPException(status_code=400, detail="Missing profile_image field")
        
        data = load_data()
        if "personal_info" not in data:
            data["personal_info"] = {}
            
        data["personal_info"]["profile_image"] = image_data["profile_image"]
        save_data(data)
        
        print(f"📸 Profile image updated: {len(image_data['profile_image'])} characters")
        
        return {
            "message": "Profile image updated successfully",
            "image_size": len(image_data["profile_image"])
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error updating profile image: {e}")
        raise HTTPException(status_code=500, detail=f"Error updating profile image: {str(e)}")

@app.delete("/api/profile-image")
async def delete_profile_image():
    """Delete profile image"""
    try:
        data = load_data()
        if "personal_info" in data and "profile_image" in data["personal_info"]:
            del data["personal_info"]["profile_image"]
            save_data(data)
            return {"message": "Profile image deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="No profile image found")
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error deleting profile image: {e}")
        raise HTTPException(status_code=500, detail=f"Error deleting profile image: {str(e)}")

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)