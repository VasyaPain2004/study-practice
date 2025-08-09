def test_get_notes_with_tag(client):
    response = client.get('/api/notes?tag=important')
    assert response.status_code == 200
    assert len(response.get_json()['items']) == 1

def test_create_tag(client):
    response = client.post('/api/tags', json={'name': 'urgent'})
    assert response.status_code == 201
    assert response.get_json()['name'] == 'urgent'