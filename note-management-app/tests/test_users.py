def test_create_user(client):
    response = client.post('/api/users', json={'username': 'newuser'})
    assert response.status_code == 201
    assert response.get_json()['username'] == 'newuser'
