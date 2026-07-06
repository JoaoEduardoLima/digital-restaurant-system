from app import create_app
from app.db import close_db

app = create_app()
app.teardown_appcontext(close_db)
