from fastapi import FastAPI

from routers import users, section

app = FastAPI()

app.include_router(users.router, prefix="/user")
app.include_router(section.router, prefix="/section")

# cd "C:\Users\User\OneDrive\Desktop\studapp"
