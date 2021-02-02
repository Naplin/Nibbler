import sqlite3
import random

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

menus = sqlite3.connect("menus.db")
users = sqlite3.connect("users.db")

app = Flask("__name__")


@app.route("/customer/<rid>")
def customer(rid):
    restaurant_name = users.execute("SELECT rname FROM restaurants WHERE rid = ?", rid).fetchall()
    response = menus.execute("SELECT id, mname, msub, mitems FROM menus WHERE rid = ?", rid).fetchall().append(rid)
    response.append(restaurant_name[0][0])
    return response


@app.route("/menuchange", methods=["POST"])
def menuchange():
    restaurant_id = request.form.get("rid")
    menu_id = request.form.get("mid")
    menu_name = request.form.get("mname")
    menu_sub = request.form.get("msub")
    menu_content = request.form.get("mitems")

    existing = menus.execute("SELECT mname, msub, item, price FROM menus JOIN mcontent ON menus.id = mcontent.mid WHERE id=?", menu_id).fetchall()

    if existing:
        if menu_name != existing[0][0]:
            menus.execute("UPDATE menus SET mname=? WHERE id=?", (menu_name, menu_id))
        if menu_sub != existing[0][1]:
            menus.execute("UPDATE menus SET msub=? WHERE id=?", (menu_sub, menu_id))
        if menu_content != existing[0][2]:
            menus.execute("DELETE FROM mcontent WHERE mid=?", menu_id)
            for item in menu_content:
                menus.execute("INSERT INTO mcontent (item, price, mid) VALUES (?, ?, ?)", (item["name"], item["price"], menu_id))
    else:
        menu_data = (menu_name, menu_sub, menu_content, restaurant_id)
        menus.execute("INSERT INTO menus (mname, msub, mitems, rid) VALUES (?, ?, ?, ?)", menu_data)

    return redirect("/customer/" + restaurant_id.lower())


@app.route("/register", methods=["POST"])
def register():

    restaurant_id = ""
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ids = users.execute("SELECT rid FROM restaurants").fetchall()
    fids = []

    for element in ids:
        fids.append(element[0])

    while restaurant_id in fids:
        for i in range(1, 5):
            randnm = random.randint(0, 35)
            if randnm<10:
                restaurant_id += str(randnm)
            else:
                restaurant_id += alphabet[randnm - 10]

    users.execute("INSERT INTO restaurants (rname, )")

    return redirect("/customer/" + restaurant_id)


menus.close()
users.close()
