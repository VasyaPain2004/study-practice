from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from models import db, Note, User, Tag
import os

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    with app.app_context():
        db_dir = os.path.join(os.path.dirname(__file__), 'instance')
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
        
        try:
            db.create_all()
            print("Таблицы созданы/проверены")
        except Exception as e:
            print(f"Ошибка при создании таблиц: {e}")


@app.route("/api/notes", methods=["GET"])
def get_notes():
    title = request.args.get("title")
    user_id = request.args.get("user_id", type=int)
    tag_name = request.args.get("tag")

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 2, type=int)

    query = Note.query

    if title:
        query = query.filter(Note.title.ilike(f"%{title}%"))

    if user_id:
        query = query.filter_by(user_id=user_id)

    if tag_name:
        query = query.join(Note.tags).filter(Tag.name == tag_name)

    paginated = query.order_by(Note.id.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify(
        {
            "total": paginated.total,
            "page": paginated.page,
            "pages": paginated.pages,
            "per_page": paginated.per_page,
            "items": [note.to_dict() for note in paginated.items],
        }
    )


@app.route("/api/notes", methods=["POST"])
def create_note():
    data = request.json
    new_note = Note(title=data["title"], content=data["content"])
    db.session.add(new_note)
    db.session.commit()
    return jsonify(new_note.to_dict()), 201


@app.route("/api/notes/<int:id>", methods=["GET"])
def get_note(id):
    note = Note.query.get_or_404(id)
    return jsonify(note.to_dict())


@app.route("/api/notes/<int:id>", methods=["PUT"])
def update_note(id):
    note = Note.query.get_or_404(id)
    data = request.json
    note.title = data.get("title", note.title)
    note.content = data.get("content", note.content)
    db.session.commit()
    return jsonify(note.to_dict())


@app.route("/api/notes/<int:id>", methods=["DELETE"])
def delete_note(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return "", 204


@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.json
    user = User(username=data["username"])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@app.route("/api/tags", methods=["POST"])
def create_tag():
    data = request.json
    tag = Tag(name=data["name"])
    db.session.add(tag)
    db.session.commit()
    return jsonify(tag.to_dict()), 201


if __name__ == "__main__":
    app.run(debug=True)
