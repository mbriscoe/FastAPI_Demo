from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="FastAPI Fundamentals",
    description="A beginner-friendly FastAPI project for Routing and CRUD Operations",
    version="1.0.0",
)

# TEMPORARY DATABASE
courses = {
    1: {"id": 1,
        "title": "Python Basics",
        "description": "Learn python the easy way!",
        "instructor": "Mark",
        "duration_hours": 6,
        "is_active": True,
        },
    2: {"id": 2,
        "title": "FastAPI Fundamentals",
        "description": "Build APIs with your eyes closed!",
        "instructor": "Yakup",
        "duration_hours": 12,
        "is_active": True,
        },
    3: {"id": 3,
        "title": "Data Analysis with PANDAS",
        "description": "Clean and analyse data sets!",
        "instructor": "Bill Gates",
        "duration_hours": 1,
        "is_active": False,
        },
}

next_course_id = 4

# API ROUTES


@app.get("/")
def read_root():
    return {
        "message": "Welcome to FastAPI Course API",
        "docs_url": "/docs",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


# COURSE ENDPOINTS
@app.get("/courses")
def list_courses(is_active: bool | None = None, search: str | None = None, limit: int | None = None):
    course_list = list(courses.values())

    if is_active is not None:
        course_list = [
            course for course in course_list if course["is_active"] == is_active]

    if search:
        search_lower = search.lower()
        course_list = [
            course
            for course in course_list
            if search_lower in course["title"].lower()
            or search_lower in course["description"].lower()
        ]

    if limit is not None:
        course_list = course_list[:limit]

    return {
        "message": "Courses retrieved successfully",
        "count": len(course_list),
        "data": course_list,
    }


@app.get("/courses/{course_id}")
def get_course(course_id: int):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")

    return {
        "message": "Course found successfully",
        "data": courses[course_id],
    }


@app.post("/courses", status_code=201)
def create_course(course: dict):
    global next_course_id

    new_course = {
        "id": next_course_id,
        "title": course.get("title"),
        "description": course.get("description"),
        "instructor": course.get("instructor"),
        "duration_hours": course.get("duration_hours"),
        "is_active": course.get("is_active", True)
    }

    courses[next_course_id] = new_course
    next_course_id += 1

    return {
        "message": "Course created successfully",
        "data": new_course,
    }


@app.put("/courses/{course_id}")
def update_course(course_id: int, updated_course: dict):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")

    course = courses[course_id]

    course["title"] = updated_course.get("title", course["title"])
    course["description"] = updated_course.get(
        "description", course["description"])
    course["instructor"] = updated_course.get(
        "instructor", course["instructor"])
    course["duration_hours"] = updated_course.get(
        "duration_hours", course["duration_hours"])
    course["is_active"] = updated_course.get("is_active", course["is_active"])

    return {
        "message": "Course updated successfully",
        "data": course,
    }


@app.delete("/courses/{course_id}")
def delete_course(course_id: int):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")

    deleted_course = courses.pop(course_id)

    return {
        "message": "Course deleted successfully",
        "data": deleted_course
    }
