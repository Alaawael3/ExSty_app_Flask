from Exsty_app import create_app
from flask import current_app
from Exsty_app import db

app = create_app()

with current_app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
