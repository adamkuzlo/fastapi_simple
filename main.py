import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from faker import Faker

from database import get_db, initialize_database
from models import User, PlayerBoxScore, TeamBoxScore, CbbPredictions

# Constants
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SAMPLE_SPREADSHEET_ID = "1zVJZjqTlAbDUAXBisTlcs5XBoocm4lHen3t0hWt5SEA"
SAMPLE_RANGE_NAME = "predictions"

# Initialize FastAPI and Faker
app = FastAPI()
fake = Faker()

# Initialize the database
initialize_database()

def fetch_predictions_from_sheets():
    """
    Fetch data from Google Sheets and filter the required columns.
    """
    creds = None
    # Load credentials from token.json or prompt user login
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # Build Sheets API service
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()

        # Fetch data from the specified sheet and range
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
        values = result.get("values", [])

        if not values:
            return []

        # Filter required columns (indices 0, 1, 2, 3, 4, 5, 9, 10)
        selected_columns_indices = [0, 1, 2, 3, 4, 5, 9, 10]
        filtered_data = [
            [row[i] if i < len(row) else "" for i in selected_columns_indices]
            for row in values
        ]
        return filtered_data

    except HttpError as err:
        raise HTTPException(status_code=500, detail=f"Error fetching data from Google Sheets: {err}")


@app.get("/")
async def root(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Fetch all users with optional pagination.
    - `skip`: Number of records to skip (default: 0).
    - `limit`: Maximum number of records to return (default: 10).
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Fetch a user by their ID.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "name": user.name, "email": user.email}


@app.post("/add_user/")
def add_user(name: str, email: str, db: Session = Depends(get_db)):
    """
    Add a new user to the database.
    """
    # Check if the user already exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create and save the new user
    new_user = User(name=name, email=email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User added successfully", "user_id": new_user.id}


@app.get("/users/me")
async def read_user_me():
    """
    Placeholder endpoint for the current user.
    """
    return {"user_id": "the current user"}


@app.post("/cbbpredictions/fetch-and-save/")
async def fetch_and_save_predictions(db: Session = Depends(get_db)):
    """
    Fetch prediction data from Google Sheets and save to the database.
    """
    predictions = fetch_predictions_from_sheets()

    if not predictions:
        raise HTTPException(status_code=404, detail="No prediction data found.")

    for row in predictions[1:]:
        print(row)
        if len(row) < 8:  # Ensure row has enough columns
            continue
        new_prediction = CbbPredictions(
            game_date=row[0],  # Ensure this is formatted as a valid date
            game_id=row[1],
            away_team_full_name=row[2],
            home_team_full_name=row[3],
            prediction_alternate=float(row[4]) if row[4] else None,
            prediction_use=float(row[5]) if row[5] else None,
            book_line=float(row[6]) if row[6] else None,
            edge_v4=float(row[7]) if row[7] else None,
        )
        db.add(new_prediction)

    db.commit()
    return {"message": "Predictions fetched and saved successfully!"}

from typing import Optional
from sqlalchemy import and_

@app.get("/cbbpredictions/")
def get_filtered_predictions(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    lowest_book_line: Optional[float] = None,
    highest_book_line: Optional[float] = None,
    db: Session = Depends(get_db),
):
    """
    Get filtered predictions based on query parameters.
    - `start_date`: Filter predictions with game_date >= start_date.
    - `end_date`: Filter predictions with game_date <= end_date.
    - `lowest_book_line`: Filter predictions with book_line >= lowest_book_line.
    - `highest_book_line`: Filter predictions with book_line <= highest_book_line.
    """
    # Start a query on the CbbPredictions model
    query = db.query(CbbPredictions)
    
    # Apply filters based on provided parameters
    if start_date:
        query = query.filter(CbbPredictions.game_date >= start_date)
    if end_date:
        query = query.filter(CbbPredictions.game_date <= end_date)
    if lowest_book_line is not None:
        query = query.filter(CbbPredictions.book_line >= lowest_book_line)
    if highest_book_line is not None:
        query = query.filter(CbbPredictions.book_line <= highest_book_line)

    # Execute the query and fetch results
    predictions = query.all()
    
    # Convert results to a list of dictionaries for easier JSON serialization
    result = [
        {
            "no": prediction.no,
            "game_date": prediction.game_date,
            "game_id": prediction.game_id,
            "away_team_full_name": prediction.away_team_full_name,
            "home_team_full_name": prediction.home_team_full_name,
            "prediction_alternate": prediction.prediction_alternate,
            "prediction_use": prediction.prediction_use,
            "book_line": prediction.book_line,
            "edge_v4": prediction.edge_v4,
        }
        for prediction in predictions
    ]

    return {"filtered_predictions": result}