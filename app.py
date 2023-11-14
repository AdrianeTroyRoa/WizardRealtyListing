from flask import Flask 

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello! <h1>World!</h1>"

@app.route("/<name>")
def user(name):
    return "Hello user" + name

if __name__ == "__main__":
    app.run()
