from flask import Flask, jsonify, render_template, redirect, url_for, request
import requests
def api_request():
    response = requests.get ('http://api.open-notify.org/astros.json')
    data = response.json()
    return data.get ("people", [])