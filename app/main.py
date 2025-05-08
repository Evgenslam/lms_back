import uvicorn
from fastapi import FastAPI

# from app.security import create_access_token
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin

from app.admin.views import LessonAdmin, TextbookAdmin, UserAdmin, UserLessonAdmin
from app.contents.router import router as router_contents
from app.database import engine
from app.textbooks.models import Lesson, Textbook, UserLesson, UserTextbook
from app.textbooks.router import router as router_textbooks
from app.users.models import User

# from app.crud import create_user, authenticate_user, update_user_progress, get_user_progress
# from app.users.schemas import ProgressUpdate, UserCreate, UserLogin, UserRegisterDTO
from app.users.router import router as router_users

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],  # Change this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],  # Allows OPTIONS, GET, POST, etc.
    allow_headers=["*"],
)

app.include_router(router_users)
app.include_router(router_textbooks)
app.include_router(router_contents)

admin = Admin(app, engine)


admin.add_view(UserAdmin)
admin.add_view(TextbookAdmin)
admin.add_view(LessonAdmin)
admin.add_view(UserLessonAdmin)


if __name__ == "__main__":
    uvicorn.run(app="app.main:app", reload=True)


# TODO: add versioning of DB with config
# TODO: start using git
# TODO: change this line Running upgrade 3fc40b2db86d -> 5df63a50e9d9, add unique and composite constraints
# TODO: use api/v1, core structure
# TODO: add response_models to all routers


# @router.post("/register")
# async def register_user(user_data: UserRegisterDTO):
#     existing_user = await CRUDUser.get_one_or_none(email=user_data.email)
#     if existing_user:
#         raise EmailAlreadyExistsException
#     hashed_password = get_password_hash(user_data.password)
#     print(hashed_password)
#     try:
#         await CRUDUser.add(username = user_data.username, email=user_data.email, hashed_password=hashed_password)
#     except:
#         raise UsernameAlreadyExistsException

# @router.get('/all')
# async def get_all_cameras(user: User = Depends(get_current_user)):
#     if user:
#         return await CRUDCamera.get_all()
#
# @app.post("/login")
# def login(user: UserLogin, db: Session = Depends(get_db)):
#     db_user = authenticate_user(db, user.username, user.password)
#     if not db_user:
#         raise HTTPException(status_code=400, detail="Invalid credentials")
#     token = create_access_token({"sub": db_user.username})
#     return {"access_token": token}

# @app.get("/progress")
# def get_progress(token: str, db: Session = Depends(get_db)):
#     return get_user_progress(db, token)

# @app.post("/progress")
# def update_progress(progress: ProgressUpdate, token: str, db: Session = Depends(get_db)):
#     return update_user_progress(db, token, progress.progress)
