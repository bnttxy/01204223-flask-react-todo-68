from http import HTTPStatus
from main import TodoItem, db

def create_todo(title='Sample todo', done=False):
    todo = TodoItem(title=title, done=done)
    db.session.add(todo)
    db.session.commit()
    return todo

def test_get_empty_todo_items(client):
    """ทดสอบกรณีที่ยังไม่มีข้อมูลในระบบ"""
    response = client.get('/api/todos/')
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == []

def test_get_sample_todo_items(client, app_context):
    """ทดสอบกรณีที่มีข้อมูลอยู่ในระบบ"""
    todo1 = create_todo(title='Todo 1', done=False)
    todo2 = create_todo(title='Todo 2', done=True)
    
    response = client.get('/api/todos/')
    assert response.status_code == HTTPStatus.OK
    
    data = response.get_json()
    assert len(data) == 2
    assert data[0]['title'] == 'Todo 1'