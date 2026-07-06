from app import create_app
from app.db import close_connection

app = create_app()

app.teardown_appcontext(close_connection)

if __name__ == "__main__":
    # app.run(debug=True)
    app.run()
