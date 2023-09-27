from flask import Flask, request, jsonify
from markupsafe import escape
from faker import Faker
import requests

app = Flask(__name__)


@app.route("/")
def index():
    name = request.args.get("name", "")
    return f"Hello {escape(name)}"


@app.route('/requirements')
def show_req():
    try:
        file = open('requirements.txt', 'r')
        content = file.read()
        return content.replace(" ","\n")
    except FileNotFoundError:
        return "File 'requirements.txt' not found", 404


@app.route('/users/generate')
def gen_users():
    num = request.args.get("num", "")

    if num == "":
        how_many = 100
    else:
        how_many = int(num)

    fake = Faker()
    names_emails = {}
    for i in range(how_many):
        names_emails[fake.name()] = fake.email()

    return jsonify(names_emails)


@app.route('/mean')
def avg_hw():
    # try:
    file = open('hw.csv', 'r')
    data = file.read()

    lines = data.split("\n")

    avg_h = 0
    avg_w = 0
    count = 0

    for line in lines:
        param = line.split(", ")

        if param[0].isdigit():
            avg_h += float(param[1])  # sum height in inch
            avg_w += float(param[2])  # sum weight in
            count += 1

        else:
            continue
    avg_height_cm = avg_h / count * 2.54
    avg_weight_kg = avg_w / count * 0.453592
    return str(round(avg_weight_kg))  # str(round(avg_height_cm))  #  str(avg_weight_kg), str(avg_height_cm)


@app.route('/space')
def api_view():
    r = requests.get("http://api.open-notify.org/astros.json")
    astro = r.json()
    return str(astro["number"])


# @app.route('/path/<path:subpath>')
# def show_subpath(subpath):
#     # show the subpath after /path/
#     return f'Subpath {escape(subpath)}'
#


if __name__ == "__main__":
    app.run(debug=True)
