import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient

# App factory
def create_app():
    app = Flask(__name__)
    client = MongoClient(
        "mongodb+srv://haininhhoang94:trangtrinh1811@microblog-application.cnt6v.mongodb.net/test?authSource=admin&replicaSet=atlas-ytu7u2-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true"
    )
    app.db = client.microblog

    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert({"content": entry_content, "date": formatted_date})

        entries_with_date = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d"),
            )
            for entry in app.db.entries.find({})
        ]
        return render_template("home.html", entries=entries_with_date)

    return app
