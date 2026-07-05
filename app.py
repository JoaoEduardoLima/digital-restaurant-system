from app import create_app
from app.db import close_db

app = create_app()

app.teardown_appcontext(close_db)

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)
