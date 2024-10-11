#!/usr/bin/env python3

from flask import request, session, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, Recipe


class Signup(Resource):
    pass

    def post(self):
        data = request.get_json() if request.is_json else request.form
        if "username" not in data or "password" not in data:
            return {"error": "Missing required fields"}, 422
        try:
            user = User(
                username=data["username"],
                image_url=data["image_url"],
                bio=data["bio"],
            )
            user.password_hash = data["password"]
            db.session.add(user)
            db.session.commit()
            session["user_id"] = user.id
            return make_response(user.to_dict(), 201)
        except IntegrityError:
            return {"error": "Username already exists"}, 422
        except Exception as e:
            print(str(e))
            return make_response({"error": str(e)}, 422)


class CheckSession(Resource):
    def get(self):
        if session["user_id"]:
            user = User.query.filter_by(id=session["user_id"]).first()
            return make_response(user.to_dict(), 200)
        else:
            return make_response({"error": "You are not logged in"}, 401)


class Login(Resource):
    pass


class Logout(Resource):
    pass


class RecipeIndex(Resource):
    pass


api.add_resource(Signup, "/signup", endpoint="signup")
api.add_resource(CheckSession, "/check_session", endpoint="check_session")
api.add_resource(Login, "/login", endpoint="login")
api.add_resource(Logout, "/logout", endpoint="logout")
api.add_resource(RecipeIndex, "/recipes", endpoint="recipes")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
