from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from models import PlayerBoxScore, TeamBoxScore
from faker import Faker

fake = Faker()
app = FastAPI()

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
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "name": user.name, "email": user.email}

@app.post("/add_user/")
def add_user(name: str, email: str, db: Session = Depends(get_db)):
    # Check if the user already exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user instance
    new_user = User(name=name, email=email)
    
    # Add the new user to the session
    db.add(new_user)
    db.commit()  # Commit the transaction to save to the database
    db.refresh(new_user)  # Refresh to get the updated instance with generated ID
    
    return {"message": "User added successfully", "user_id": new_user.id}

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

# Generate Dummy Data for PlayerBoxScore (to populate the database)
@app.post("/generate_dummy_player_box_scores/")
def generate_dummy_player_box_scores(num_records: int = 10, db: Session = Depends(get_db)):
    """
    Generate dummy player box score data using the Faker library and populate the database.
    - `num_records`: The number of player box score records to generate (default: 10).
    """
    dummy_player_box_scores = []
    
    for _ in range(num_records):
        game_id = fake.random_int(min=1, max=1000)
        athlete_id = fake.random_int(min=1, max=1000)
        season = fake.random_int(min=2020, max=2024)
        season_type = fake.random_int(min=1, max=2)
        game_date = fake.date_this_year().strftime('%Y-%m-%d')
        game_date_time = fake.date_this_year().strftime('%Y-%m-%d %H:%M:%S')
        athlete_display_name = fake.name()
        team_name = fake.company()
        team_location = fake.city()
        team_short_display_name = team_name[:3]  # Short name (first 3 letters of team name)
        minutes = fake.random_number(digits=2)
        field_goals_made = fake.random_int(min=0, max=10)
        field_goals_attempted = fake.random_int(min=0, max=20)
        three_point_field_goals_made = fake.random_int(min=0, max=5)
        three_point_field_goals_attempted = fake.random_int(min=0, max=10)
        free_throws_made = fake.random_int(min=0, max=10)
        free_throws_attempted = fake.random_int(min=0, max=10)
        offensive_rebounds = fake.random_int(min=0, max=5)
        defensive_rebounds = fake.random_int(min=0, max=10)
        rebounds = offensive_rebounds + defensive_rebounds
        assists = fake.random_int(min=0, max=10)
        steals = fake.random_int(min=0, max=5)
        blocks = fake.random_int(min=0, max=5)
        turnovers = fake.random_int(min=0, max=5)
        fouls = fake.random_int(min=0, max=5)
        points = (field_goals_made * 2) + (three_point_field_goals_made * 3) + free_throws_made
        starter = fake.boolean()
        ejected = fake.boolean()
        did_not_play = fake.boolean()
        active = fake.boolean()
        athlete_jersey = fake.random_int(min=0, max=99)
        athlete_short_name = athlete_display_name.split()[0][:3]  # First 3 letters of first name
        athlete_headshot_href = fake.image_url()
        athlete_position_name = fake.random_element(elements=("Guard", "Forward", "Center"))
        athlete_position_abbreviation = athlete_position_name[:3].upper()
        team_display_name = team_name
        team_uid = fake.uuid4()
        team_slug = fake.slug()
        team_logo = fake.image_url()
        team_abbreviation = team_name[:3].upper()
        team_color = fake.color_name()
        team_alternate_color = fake.color_name()
        home_away = fake.random_element(elements=("Home", "Away"))
        team_winner = fake.random_element(elements=("Yes", "No"))
        team_score = fake.random_int(min=50, max=150)
        opponent_team_id = fake.random_int(min=1, max=1000)
        opponent_team_name = fake.company()
        opponent_team_location = fake.city()
        opponent_team_display_name = opponent_team_name
        opponent_team_abbreviation = opponent_team_name[:3].upper()
        opponent_team_logo = fake.image_url()
        opponent_team_color = fake.color_name()
        opponent_team_alternate_color = fake.color_name()
        opponent_team_score = fake.random_int(min=50, max=150)

        # Create a new PlayerBoxScore instance with fake data
        dummy_player_box_scores.append(PlayerBoxScore(
            game_id=game_id,
            athlete_id=athlete_id,
            season=season,
            season_type=season_type,
            game_date=game_date,
            game_date_time=game_date_time,
            athlete_display_name=athlete_display_name,
            team_name=team_name,
            team_location=team_location,
            team_short_display_name=team_short_display_name,
            minutes=minutes,
            field_goals_made=field_goals_made,
            field_goals_attempted=field_goals_attempted,
            three_point_field_goals_made=three_point_field_goals_made,
            three_point_field_goals_attempted=three_point_field_goals_attempted,
            free_throws_made=free_throws_made,
            free_throws_attempted=free_throws_attempted,
            offensive_rebounds=offensive_rebounds,
            defensive_rebounds=defensive_rebounds,
            rebounds=rebounds,
            assists=assists,
            steals=steals,
            blocks=blocks,
            turnovers=turnovers,
            fouls=fouls,
            points=points,
            starter=str(starter),
            ejected=str(ejected),
            did_not_play=str(did_not_play),
            active=str(active),
            athlete_jersey=athlete_jersey,
            athlete_short_name=athlete_short_name,
            athlete_headshot_href=athlete_headshot_href,
            athlete_position_name=athlete_position_name,
            athlete_position_abbreviation=athlete_position_abbreviation,
            team_display_name=team_display_name,
            team_uid=team_uid,
            team_slug=team_slug,
            team_logo=team_logo,
            team_abbreviation=team_abbreviation,
            team_color=team_color,
            team_alternate_color=team_alternate_color,
            home_away=home_away,
            team_winner=team_winner,
            team_score=team_score,
            opponent_team_id=opponent_team_id,
            opponent_team_name=opponent_team_name,
            opponent_team_location=opponent_team_location,
            opponent_team_display_name=opponent_team_display_name,
            opponent_team_abbreviation=opponent_team_abbreviation,
            opponent_team_logo=opponent_team_logo,
            opponent_team_color=opponent_team_color,
            opponent_team_alternate_color=opponent_team_alternate_color,
            opponent_team_score=opponent_team_score
        ))

    # Add all the generated player box scores to the session
    db.add_all(dummy_player_box_scores)
    db.commit()  # Commit the transaction to save all records to the database
    
    return {"message": f"{num_records} dummy player box scores generated successfully"}

@app.post("/generate_dummy_team_box_scores/")
def generate_dummy_team_box_scores(num_records: int = 10, db: Session = Depends(get_db)):
    """
    Generate dummy team box score data using the Faker library and populate the database.
    - `num_records`: Number of records to generate (default: 10).
    """
    dummy_team_box_scores = []
    
    for _ in range(num_records):
        # Generate dummy data for the team box score
        game_id = fake.random_int(min=1, max=1000)
        season = fake.random_int(min=2020, max=2024)
        season_type = fake.random_int(min=1, max=2)  # 1 = Regular, 2 = Postseason
        game_date = fake.date_this_year().strftime('%Y-%m-%d')
        game_date_time = fake.date_this_year().strftime('%Y-%m-%d %H:%M:%S')
        
        team_id = fake.random_int(min=1, max=1000)
        team_uid = fake.uuid4()
        team_slug = fake.slug()
        team_location = fake.city()
        team_name = fake.company()
        team_abbreviation = team_name[:3]
        team_display_name = team_name
        team_short_display_name = team_name[:3]
        team_color = fake.color_name()
        team_alternate_color = fake.color_name()
        team_logo = fake.image_url()
        team_home_away = fake.random_element(elements=["Home", "Away"])
        team_score = fake.random_int(min=50, max=150)
        team_winner = fake.random_element(elements=["Yes", "No"])
        
        # Generate other team statistics
        assists = fake.random_int(min=0, max=30)
        blocks = fake.random_int(min=0, max=10)
        defensive_rebounds = fake.random_int(min=0, max=20)
        fast_break_points = fake.random_int(min=0, max=15)
        field_goal_pct = round(fake.random_number(digits=2) / 100, 2)
        field_goals_made = fake.random_int(min=0, max=10)
        field_goals_attempted = fake.random_int(min=0, max=20)
        flagrant_fouls = fake.random_int(min=0, max=5)
        fouls = fake.random_int(min=0, max=10)
        free_throw_pct = round(fake.random_number(digits=2) / 100, 2)
        free_throws_made = fake.random_int(min=0, max=10)
        free_throws_attempted = fake.random_int(min=0, max=20)
        largest_lead = fake.random_int(min=0, max=30)
        offensive_rebounds = fake.random_int(min=0, max=20)
        points_in_paint = fake.random_int(min=0, max=40)
        steals = fake.random_int(min=0, max=10)
        team_turnovers = fake.random_int(min=0, max=15)
        technical_fouls = fake.random_int(min=0, max=3)
        three_point_field_goal_pct = round(fake.random_number(digits=2) / 100, 2)
        three_point_field_goals_made = fake.random_int(min=0, max=10)
        three_point_field_goals_attempted = fake.random_int(min=0, max=20)
        total_rebounds = offensive_rebounds + defensive_rebounds
        total_technical_fouls = fake.random_int(min=0, max=3)
        total_turnovers = team_turnovers + fake.random_int(min=0, max=10)
        turnover_points = fake.random_int(min=0, max=15)
        turnovers = team_turnovers
        
        opponent_team_id = fake.random_int(min=1, max=1000)
        opponent_team_uid = fake.uuid4()
        opponent_team_slug = fake.slug()
        opponent_team_location = fake.city()
        opponent_team_name = fake.company()
        opponent_team_abbreviation = opponent_team_name[:3]
        opponent_team_display_name = opponent_team_name
        opponent_team_short_display_name = opponent_team_name[:3]
        opponent_team_color = fake.color_name()
        opponent_team_alternate_color = fake.color_name()
        opponent_team_logo = fake.image_url()
        opponent_team_score = fake.random_int(min=50, max=150)

        # Create a new TeamBoxScore object
        team_box_score = TeamBoxScore(
            game_id=game_id,
            season=season,
            season_type=season_type,
            game_date=game_date,
            game_date_time=game_date_time,
            team_id=team_id,
            team_uid=team_uid,
            team_slug=team_slug,
            team_location=team_location,
            team_name=team_name,
            team_abbreviation=team_abbreviation,
            team_display_name=team_display_name,
            team_short_display_name=team_short_display_name,
            team_color=team_color,
            team_alternate_color=team_alternate_color,
            team_logo=team_logo,
            team_home_away=team_home_away,
            team_score=team_score,
            team_winner=team_winner,
            assists=assists,
            blocks=blocks,
            defensive_rebounds=defensive_rebounds,
            fast_break_points=fast_break_points,
            field_goal_pct=field_goal_pct,
            field_goals_made=field_goals_made,
            field_goals_attempted=field_goals_attempted,
            flagrant_fouls=flagrant_fouls,
            fouls=fouls,
            free_throw_pct=free_throw_pct,
            free_throws_made=free_throws_made,
            free_throws_attempted=free_throws_attempted,
            largest_lead=largest_lead,
            offensive_rebounds=offensive_rebounds,
            points_in_paint=points_in_paint,
            steals=steals,
            team_turnovers=team_turnovers,
            technical_fouls=technical_fouls,
            three_point_field_goal_pct=three_point_field_goal_pct,
            three_point_field_goals_made=three_point_field_goals_made,
            three_point_field_goals_attempted=three_point_field_goals_attempted,
            total_rebounds=total_rebounds,
            total_technical_fouls=total_technical_fouls,
            total_turnovers=total_turnovers,
            turnover_points=turnover_points,
            turnovers=turnovers,
            opponent_team_id=opponent_team_id,
            opponent_team_uid=opponent_team_uid,
            opponent_team_slug=opponent_team_slug,
            opponent_team_location=opponent_team_location,
            opponent_team_name=opponent_team_name,
            opponent_team_abbreviation=opponent_team_abbreviation,
            opponent_team_display_name=opponent_team_display_name,
            opponent_team_short_display_name=opponent_team_short_display_name,
            opponent_team_color=opponent_team_color,
            opponent_team_alternate_color=opponent_team_alternate_color,
            opponent_team_logo=opponent_team_logo,
            opponent_team_score=opponent_team_score
        )

        # Append the dummy team box score to the list
        dummy_team_box_scores.append(team_box_score)
    
    # Add all records to the session and commit to the database
    if db:
        db.add_all(dummy_team_box_scores)
        db.commit()
    
    return {"message": f"{num_records} dummy team box scores generated successfully"}