from fastapi import FastAPI
from app.routes import router
from app.db_conenct import engine, Base

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include the API routes
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI User Authentication API"}