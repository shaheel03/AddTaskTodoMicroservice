import pyodbc
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Update Connection String Here
connection_string="Driver={ODBC Driver 17 for SQL Server};Server=tcp:devopsinsidersdb.database.windows.net,1433;Database=todoapp;Uid=devopsinsider;Pwd=shivesh@1234;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30"

app = FastAPI()

# Configure CORSMiddleware to allow all origins (disable CORS for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins (use '*' for development only)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define the Task model
class Task(BaseModel):
    title: str
    description: str

# Create a table for tasks (You can run this once outside of the app)
@app.get("/")
def create_tasks_table():
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE Tasks (
                ID int NOT NULL PRIMARY KEY IDENTITY,
                Title varchar(255),
                Description text
            );
        """)
        conn.commit()  
        return "Add-Tasks API Ready."      
    except Exception as e:
        print(e)
        if "There is already an object named 'Tasks' in the database." in str(e):
            return "Add-Tasks API Ready."
        else:
            return "Error. Please check Logs."
    

# Create a new task
@app.post("/tasks")
def create_task(task: Task):
    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Tasks (Title, Description) VALUES (?, ?)", task.title, task.description)
        conn.commit()
    return task

if __name__ == "__main__":
    create_tasks_table()
