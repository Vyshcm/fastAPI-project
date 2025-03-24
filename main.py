from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Initialize FastAPI
app = FastAPI()

# Configure templates folder
templates = Jinja2Templates(directory="templates")

# In-memory list to store user data
users = []

# Serve HTML page
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "users": users})

# GET - Retrieve all users
@app.get("/users/")
def get_users():
    return users

# POST - Add a new user
@app.post("/users/")
def create_user(name: str, id: int):
    users.append({"name": name, "id": id})
    return {"message": "User added successfully", "user": {"name": name, "id": id}}

# PUT - Update user details by ID
@app.put("/users/{user_id}")
def update_user(user_id: int, name: str):
    for user in users:
        if user["id"] == user_id:
            user["name"] = name
            return {"message": "User updated successfully", "user": user}
    raise HTTPException(status_code=404, detail="User not found")

# PATCH - Partially update user details
@app.patch("/users/{user_id}")
def patch_user(user_id: int, name: str = None):
    for user in users:
        if user["id"] == user_id:
            if name:
                user["name"] = name
            return {"message": "User updated partially", "user": user}
    raise HTTPException(status_code=404, detail="User not found")

# DELETE - Delete a user by ID
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            users.remove(user)
            return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")
