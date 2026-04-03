from http import HTTPStatus
from models import TodoItem, db
import pytest

def create_todo(title='Sample todo', done=False):
    todo = TodoItem(title=title, done=done)
    db.session.add(todo)
    db.session.commit()
    return todo

@pytest.fixture
def sample_todo_items(app_context):
    todo1 = create_todo(title='Todo 1', done=False)
    todo2 = create_todo(title='Todo 2', done=True)
    return [todo1, todo2]

def test_get_empty_todo_items(client):
    response = client.get('/api/todos/')
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == []

def test_get_sample_todo_items(client, sample_todo_items):
    response = client.get('/api/todos/')
    assert response.status_code == HTTPStatus.OK
    assert len(response.get_json()) == 2

def test_toggle_todo_item(client, sample_todo_items):
    item1 = sample_todo_items[0]
    response = client.patch(f'/api/todos/{item1.id}/toggle/')
    assert response.status_code == HTTPStatus.OK
    assert response.get_json()['done'] is True