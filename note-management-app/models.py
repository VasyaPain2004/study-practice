from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

note_tags = db.Table(
    'note_tags',
    db.Column('note_id', db.Integer, db.ForeignKey('note.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class User(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    notes    = db.relationship('Note', backref='author', lazy=True)

    def to_dict(self):
        return {'id': self.id, 'username': self.username}

class Tag(db.Model):
    id    = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(50), unique=True, nullable=False)
    notes = db.relationship('Note', secondary=note_tags, back_populates='tags')

    def to_dict(self):
        return {'id': self.id, 'name': self.name}

class Note(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    title      = db.Column(db.String(100), nullable=False)
    content    = db.Column(db.Text, nullable=False)
    user_id    = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tags       = db.relationship('Tag', secondary=note_tags, back_populates='notes')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'user': self.author.to_dict(),
            'tags': [t.to_dict() for t in self.tags]
        }
