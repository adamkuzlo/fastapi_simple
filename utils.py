from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Function to generate random player box score data
def generate_player_box_score(game_id, athlete_id):
    return {
        'game_id': game_id,
        'season': random.choice([2024, 2025]),
        'season_type': random.choice([1, 2]),  # 1 for regular season, 2 for playoffs
        'game_date': fake.date_this_year(),
        'game_date_time': fake.time(),
        'athlete_id': athlete_id,
        'athlete_display_name': fake.name(),
        'team_id': random.randint(1, 30),
        'team_name': fake.company(),
        'team_location': fake.city(),
        'team_short_display_name': fake.word(),
        'minutes': round(random.uniform(10.0, 40.0), 1),
        'field_goals_made': random.randint(0, 15),
        'field_goals_attempted': random.randint(0, 20),
        'three_point_field_goals_made': random.randint(0, 10),
        'three_point_field_goals_attempted': random.randint(0, 15),
        'free_throws_made': random.randint(0, 10),
        'free_throws_attempted': random.randint(0, 10),
        'offensive_rebounds': random.randint(0, 5),
        'defensive_rebounds': random.randint(0, 10),
        'rebounds': random.randint(0, 15),
        'assists': random.randint(0, 10),
        'steals': random.randint(0, 5),
        'blocks': random.randint(0, 5),
        'turnovers': random.randint(0, 5),
        'fouls': random.randint(0, 5),
        'points': random.randint(0, 30),
        'starter': random.choice(['Yes', 'No']),
        'ejected': random.choice([None, 'Yes']),
        'did_not_play': random.choice([None, 'Yes']),
        'active': random.choice(['Yes', 'No']),
        'athlete_jersey': random.randint(1, 99),
        'athlete_short_name': fake.first_name(),
        'athlete_headshot_href': fake.image_url(),
        'athlete_position_name': random.choice(['Guard', 'Forward', 'Center']),
        'athlete_position_abbreviation': random.choice(['PG', 'SG', 'SF', 'PF', 'C']),
        'team_display_name': fake.company(),
        'team_uid': fake.uuid4(),
        'team_slug': fake.slug(),
        'team_logo': fake.image_url(),
        'team_abbreviation': fake.word().upper(),
        'team_color': fake.color(),
        'team_alternate_color': fake.color(),
        'home_away': random.choice(['Home', 'Away']),
        'team_winner': random.choice(['Yes', 'No']),
        'team_score': random.randint(80, 130),
        'opponent_team_id': random.randint(1, 30),
        'opponent_team_name': fake.company(),
        'opponent_team_location': fake.city(),
        'opponent_team_display_name': fake.company(),
        'opponent_team_abbreviation': fake.word().upper(),
        'opponent_team_logo': fake.image_url(),
        'opponent_team_color': fake.color(),
        'opponent_team_alternate_color': fake.color(),
        'opponent_team_score': random.randint(80, 130)
    }

# Generate multiple rows of data
def generate_data(num_rows=30):
    data = []
    game_id = 1
    for athlete_id in range(1, num_rows + 1):
        data.append(generate_player_box_score(game_id, athlete_id))
        game_id += 1
    return data

# Format the data into SQL INSERT statements
def generate_sql_inserts(data):
    sql_inserts = []
    for row in data:
        sql = f"INSERT INTO `player_box_score` ({', '.join(row.keys())}) VALUES ({', '.join([str(v) if v is not None else 'NULL' for v in row.values()])});"
        sql_inserts.append(sql)
    return sql_inserts

# Generate 30 rows of data
data = generate_data(30)

# Generate SQL statements
sql_statements = generate_sql_inserts(data)

# Print SQL insert statements
for statement in sql_statements:
    print(statement)
