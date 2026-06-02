from fastapi import FastAPI, HTTPException
from typing import Literal
from pydantic import BaseModel, EmailStr, Field

# Create main object
app = FastAPI(title="FastAPI Fundamentals - Tutorial 3")

#Create in-memory data store
courses = {
    1: {
        "id": 1,
        "title": "Python Basics",
        "description": "Learn the basics of Python programming",
        "level": "beginner",
        "duration_minutes": 60,
        "tags": ["python", "programming"],
        "instructor": {
            "name": "Ayesha Khan",
            "email": "ayesha@example.com",
        },
    },
    2: {
        "id": 2,
        "title": "API Development",
        "description": "Learn how APIs work with backend applications",
        "level": "intermediate",
        "duration_minutes": 90,
        "tags": ["api", "backend"],
        "instructor": {
            "name": "Bilal Ahmed",
            "email": "bilal@example.com",
        },
    },
}

next_course_id = 3

# Create instructor pydantic model
class Instructor(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=50,
        examples=["Mark Briscoe"],
    )
    email: EmailStr = Field(
        examples=["mark@mcmw.co.uk"]
    )


# Create course pydantic model
class CourseCreate(BaseModel):
    title: str = Field(
        min_length=3,
        max_length=100,
        examples=["FastAPI Fundamentals"],
    )
    description: str = Field(
        min_length=10,
        max_length=100,
        examples=["Learn how build APIs with FastAPI"]
    )
    level: Literal["beginner", "intermediate", "advanced"] = Field(
        examples=["beginner"]
    )
    duration_minutes: int = Field(
        gt=0,
        le=600,
        examples=[90],
    )
    tags: list[str] = Field(
        default=[],
        examples=[["fastapi","python", "backend"]],
    )
    instructor: Instructor

# Create a response model
class CourseResponse(BaseModel):
    id: int
    title: str
    description: str
    level: str
    duration_minutes: int
    tags: list[str]
    instructor_name: str


def format_course_response(course: dict) -> CourseResponse:
    return CourseResponse(
        id=course["id"],
        title=course["title"],
        description=course["description"],
        level=course["level"],
        duration_minutes=course["duration_minutes"],
        tags=course.get("tags", []),
        instructor_name=course.get("instructor", {}).get("name", "Notassigned"),
    )



# root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Welcome to the FastAPI course API",
        "docs_url": "/docs",
    }


# get courses endpoint
@app.get("/courses", response_model=list[CourseResponse])
def get_courses(level: str | None = None):

    course_list= list(courses.values())

    if level:
        course_list = [
            course for course in course_list 
            if course["level"].lower() == level.lower()
        ]

    return [format_course_response(course) for course in course_list]
    

# get single course endpoint
@app.get("/courses/{course_id}", response_model=CourseResponse)
def get_course(course_id: int):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")

    return format_course_response(courses[course_id])


# post endpoint
@app.post("/courses", response_model=CourseResponse, status_code=201)
def create_course(course: CourseCreate):
    global next_course_id

    course_data = course.model_dump()
    course_data["id"] = next_course_id

    courses[next_course_id] = course_data
    next_course_id +=1

    return format_course_response(course_data)


# put endpoint
@app.put("/courses/{course_id}", response_model=CourseResponse)
def update_course(course_id: int, update_course: CourseCreate):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")

    course_data = update_course.model_dump()
    course_data["id"] = course_id

    courses[course_id] = course_data

    return format_course_response(course_data)

# delete endpoint
@app.delete("/courses/{course_id}")
def delete_course(course_id: int):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")

    deleted_course = courses.pop(course_id)

    return {
        "message": "Course deleted successfully",
        "deleted_course": format_course_response(deleted_course),
    }


