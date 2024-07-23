# server/app.py

from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

# ========================= USERS ============================

@app.route('/users' , methods=["GET", "POST"])
def users():
    
    if request.method == 'GET':
        users = [user.to_dict() for user in User.query.all()]
        return make_response(jsonify(users), 200)

    elif request.method == 'POST':
        new_user = User(
            name = request.form.get("name"),            
        )
        db.session.add(new_user)
        db.session.commit()

        return make_response(jsonify(new_user.to_dict()), 201)
    
@app.route('/users/<int:id>' , methods=["GET", "DELETE", 'PATCH'])
def user_by_id(id):
    user = User.query.filter(User.id == id).first()

    if not user:
        return make_response(jsonify({"error": "User not found"})), 404
    
    elif request.method == 'GET':
        return make_response(jsonify(user.to_dict()), 200)
    
    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()

        return make_response(jsonify({"message": "User deleted"}), 200)

    elif request.method == 'PATCH':
        for attr in request.form:
            setattr(user, attr, request.form.get(attr))
        db.session.add(user)
        db.session.commit()

        return make_response(jsonify(user.to_dict()), 200)



# =================== GAMES =====================
# start building your API here
@app.route('/games')
def games():

    games = [game.to_dict() for game in Game.query.all()]

    response = make_response(
        games,
        200
    )

    return response

@app.route('/games/<int:id>', methods=["GET", "DELETE"] )
def game_by_id(id):
    game = Game.query.filter(Game.id == id).first()

    if not game:
        return make_response(jsonify({"error": "Game not found"}), 404)

    if request.method == 'GET':
        return make_response(jsonify(game.to_dict()) , 200)

    elif request.method == 'DELETE':
        db.session.delete(game)
        db.session.commit()
        return make_response(jsonify({"message": "Game deleted"}), 200)
    


@app.route('/games/users/<int:id>')
def game_users_by_id(id):
    game = Game.query.filter(Game.id == id).first()


    # use association proxy to get users for a game
    users = [user.to_dict(rules=("-reviews",)) for user in game.users]
    response = make_response(
        users,
        200
    )

    return response


# ======================== REVIEWS ================================
@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'GET':
        reviews = [reviews.to_dict() for reviews in Review.query.all() ]
        return make_response(jsonify(reviews), 200)

    elif request.method == 'POST':
        new_review = Review(
            score=request.form.get("score"),
            comment=request.form.get("comment"),
            game_id=request.form.get("game_id"),
            user_id=request.form.get("user_id"),
        )
        db.session.add(new_review)
        db.session.commit()
        return make_response(jsonify(new_review.to_dict()), 201)
    
    

@app.route('/reviews/<int:id>' , methods=["GET", "DELETE", 'PATCH'])
def review_by_id(id):
    review = Review.query.filter(Review.id==id).first()

    if not review:
        return make_response(jsonify({"error": "Review not found"}), 404)
    
    elif request.method == 'GET':
        return make_response(jsonify(review.to_dict()), 200)

    elif request.method == 'DELETE':
        db.session.delete(review)
        db.session.commit()
        return make_response(jsonify({"message": "Review deleted"}), 200)

    elif request.method == 'PATCH':
        for attr in request.form:
            setattr(review, attr, request.form.get(attr))
        db.session.add(review)
        db.session.commit()
        return make_response(jsonify(review.to_dict()), 200)
    

if __name__ == '__main__':
    app.run(port=5555, debug=True)