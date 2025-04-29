import os

# Set the database URL for local pytest runs
os.environ["DATABASE_URL"] = "postgresql://powerx:powerx@localhost:5432/powerx"
