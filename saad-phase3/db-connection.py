from sqlalchemy import create_engine

# Connection string
connection_string = "postgresql://postgres:pgsql@localhost:5432/anime-recommendation"

try:
    # Create an engine
    engine = create_engine(connection_string)
    
    # Test the connection
    with engine.connect() as connection:
        print("Connection to the PostgreSQL database was successful!")
except Exception as e:
    print(f"Error connecting to the database: {e}")
