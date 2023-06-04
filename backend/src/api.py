import os
import traceback

from flask import Flask, jsonify
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
def get_drinks_detail(payload):
    try:
        selection = Drink.query.order_by(Drink.id).all()

        return (
            jsonify({"success": True, "drinks": [drink.long() for drink in selection]}),
            200,
        )

    except Exception as e:
        print("Error while doing something:", e)
        traceback.print_exc()


"""
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
"""

""" @app.route("/drinks", methods=["POST"])
@requires_auth("post:drinks")
def create_drinks(payload):
    body = request.get_json()
    new_title = body.get("title")
    new_recipe = body.get("recipe")

    try:
        new_drink = Drink(title=new_title, recipe=json.dumps(new_recipe))
        new_drink.insert()

        return jsonify({"success": True, "drinks": [new_drink.long()]}), 200

    except:
        abort(401)
 """

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

""" @app.route("/drinks/<int:id>", methods=["PATCH"])
@requires_auth("patch:drinks")
def update_drinks(playload, id):
    try:
        body = request.get_json()
        new_title = body.get("title", None)
        new_recipe = body.get("recipe", None)

        drink = Drink.query.filter(Drink.id == id).one_or_none()

        if drink is None:
            abort(404)

        drink.title = new_title
        drink.recipe = json.dumps(new_recipe)

        drink.update()

        return jsonify({"success": "True", "drinks": [drink.long()]})

    except Exception as e:
        print("Error while doing something:", e)
        traceback.print_exc()
        abort(401) """

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

""" @app.route("/drinks/<int:id>", methods=["DELETE"])
@requires_auth("delete:drinks")
def delete_drink(payload, id):
    try:
        drink = Drink.query.filter(Drink.id == id).one_or_none()

        if drink is None:
            abort(404)

        drink.delete()

        return jsonify({"success": "True", "delete": id}), 200
    except:
        abort(401)
 """

# Error Handling
"""
Example error handling for unprocessable entity
"""

""" 
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({"success": False, "error": 422, "message": "unprocessable"}), 422
 """

"""
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

"""

""" @app.errorhandler(404)
def unprocessable(error):
    return (
        jsonify({"success": False, "error": 404, "message": "resource not found"}),
        404,
    ) """

"""
@TODO implement error handler for 404
    error handler should conform to general task above
"""

""" @app.errorhandler(401)
def unprocessable(error):
    return (
        jsonify({"success": False, "error": 401, "message": "resource not found"}),
        401,
    ) """

"""
@TODO implement error handler for AuthError
    error handler should conform to general task above
"""

""" @app.errorhandler(AuthError)
def auth_error(error):
    return (
        jsonify(
            {
                "success": False,
                "error": error.status_code,
                "message": error.error["description"],
            }
        ),
        error.status_code,
    ) """


@app.errorhandler(404)
def not_found(error):
    return (
        jsonify({"success": False, "error": 404,
                 "message": "Not found"}),
        404,
    )

