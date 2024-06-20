from app import create_app, db

app = create_app()

# Bind SQLAlchemy instance to the app context
app.app_context().push()

# Create all tables
db.create_all()

print("Tables created successfully!")
