# this is the file to run
from flask_app import create_app

# creating the flask application
app = create_app()

if __name__ == '__main__':
    app.run(debug = True)