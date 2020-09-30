from flaskr import create_app
from models import setup_db

# Creating an app instance
app = create_app()


# Setting up SQLAlchemy
setup_db(app)


# Setting the entry point for the app
if __name__ == '__main__':
    app.run()
