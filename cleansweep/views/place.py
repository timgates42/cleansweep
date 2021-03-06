from flask import (abort, render_template, session, url_for, redirect, request, flash)

from ..app import app
from ..models import db
from .. import forms
from ..view_helpers import require_permission
from .. import helpers

@app.route("/")
def home():
    if session.get('user'):
        return redirect(url_for("dashboard"))
    else:
        # There's nothing on home page yet. Better redirect users straight to the login page.
        return redirect(url_for("login"))
        # return render_template("home.html")

@app.route("/<place:place>")
def place(place):
    return render_template("place.html", place=place)

@app.route("/<place:place>/stats")
@require_permission("read")
def stats(place):
    return render_template("admin/stats.html", place=place)

@app.route("/<place:place>/stats/<name>")
@require_permission("read")
def detailed_stats(place, name):
    from cleansweep import stats
    stat = stats.get_stat(place, name)
    if not stat:
        abort(404)
    return render_template("stats/view.html", place=place, stat=stat)
