from app import create_app, db  # import create_app from the package

app = create_app()          # create the Flask app

with app.app_context():
    db.create_all()  # create tables from your models

if __name__ == "__main__":
    app.run(debug=True)      # run the app in debug mode

