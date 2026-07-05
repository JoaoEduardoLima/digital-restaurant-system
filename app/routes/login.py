from flask import Blueprint, session, render_template, request, redirect
from app.services.queries import get_user_by_username
from werkzeug.security import check_password_hash

login_bp = Blueprint("login", __name__)
logout_bp = Blueprint("logout", __name__)

@login_bp.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return "must provide username", 403
            
        elif not request.form.get("password"):
            return "must provide password", 403

        # Query database for username
        get_user = get_user_by_username(request.form.get("username"))

        # Ensure username exists and password is correct
        if not get_user or not check_password_hash(
            get_user["password"], request.form.get("password")
        ):
            return "invalid username and/or password", 403

        session["user_id"] = get_user["id"]

        return redirect("/restaurant/kitchen")

    else:
        return render_template("login.html")

@logout_bp.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/login")