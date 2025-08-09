import pytest
from app import app, db
from models import User, Note, Tag

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Тестовые данные
            user = User(username='testuser')
            db.session.add(user)
            db.session.commit()

            note = Note(title='Test Note', content='Content', user_id=user.id)
            db.session.add(note)

            tag = Tag(name='important')
            db.session.add(tag)
            note.tags.append(tag)
            
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()