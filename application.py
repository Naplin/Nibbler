import sqlite3

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

menus = sqlite3.connect("menus.db")

app = Flask("__name__")


@app.route("/customer/<id>", methods=["GET"])
def customer(id):
    response = menus.execute("SELECT name, sub, items FROM menus WHERE id = ?", id)
    return response


@app.route("/restaurant", methods=["POST"])
def restaurant():
    restaurant_id = request.form.get("id")
    return redirect(("/customer/" + restaurant_id.lower()))
