from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/<name>")
def user(name):
    return render_template("pages.html", page_name=name)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
