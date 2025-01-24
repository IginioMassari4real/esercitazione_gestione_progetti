from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

def get_people_in_space():
    url = "http://api.open-notify.org/astros.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        people = [{"name": person["name"], "craft": person["craft"]} for person in data["people"]]
        return people
    except requests.RequestException as e:
        raise Exception(f"Errore durante la chiamata all'API: {e}")

@app.route('/')
def home():
    try:
        people_in_space = get_people_in_space()
        return render_template('home.html', people=people_in_space)
    except Exception as e:
        return f"Errore: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)
