from app import db
from models import Note, User

def test_get_notes(client):
    """Тест получения списка заметок"""
    response = client.get('/api/notes')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['items']) == 1
    assert data['items'][0]['title'] == 'Test Note'

def test_filter_notes(client):
    """Тест фильтрации по заголовку"""
    response = client.get('/api/notes?title=Test')
    assert response.status_code == 200
    assert len(response.get_json()['items']) == 1

def test_pagination(client):
    """Тест пагинации"""
    # Создаем тестового пользователя
    with client.application.app_context():
        user = User(username='test_pagination')
        db.session.add(user)
        db.session.commit()
        
        # Создаем 10 тестовых заметок
        for i in range(10):
            note = Note(
                title=f'Note {i}',
                content=f'Content {i}',
                user_id=user.id  # используем созданного пользователя
            )
            db.session.add(note)
        db.session.commit()
    
    # Проверяем пагинацию
    response = client.get('/api/notes?per_page=5')
    data = response.get_json()
    assert data['per_page'] == 5
    assert len(data['items']) == 5
    assert data['total'] == 11  # 10 новых + 1 из фикстур