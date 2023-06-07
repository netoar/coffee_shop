import os
import traceback

from flask import Flask, jsonify, request, abort
from flask_cors import CORS

from database.models import setup_db, db_drop_and_create_all, Drink

from auth.auth import requires_auth


app = Flask(__name__)
setup_db(app)
CORS(app)

with app.app_context():
    db_drop_and_create_all()

"""
@TODO uncomment the following line to initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
"""

# ROUTES
"""
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
"""


@app.route("/drinks", methods=["GET"])
def get_drinks():
    drink = Drink()
    all_drinks = drink.get_all_drinks()
    if all_drinks == []:
        abort(404)
    return jsonify({"success": True, "drinks": [drink.long() for drink in all_drinks]},
    200)


"""
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
"""


@app.route("/drinks-detail", methods=["GET"])
@requires_auth("get:drinks-detail")
def get_drinks_detail(jwt):
    drink = Drink()
    drinks_detail = drink.get_drink_detail()
    if drinks_detail == []:
        abort(404)
    return (
            jsonify({"success": True, "drinks": [drink.long() for drink in drinks_detail]}),
            200
        )

"""
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
"""

@app.route("/drinks", methods=["POST"])
@requires_auth("post:drinks")
def create_drinks(jwt):
    body = request.get_json()
    title = body.get("title")
    recipe = body.get("recipe")
    drink = Drink.create_new_drink(title, recipe)
    all_drinks = drink.get_all_drinks()
    if drink == []:
        abort(404)
    return (
            jsonify({"success": True, "drinks": [drink.long() for drink in all_drinks]}),
            200
        )


"""
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
"""

"""
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
"""


@app.errorhandler(404)
def not_found(error):
    return (
        jsonify({"success": False, "error": 404,
                 "message": "Not found"}),
        404,
    )

