from models import User, TodoItem, Comment, db

def test_check_correct_password():
    user = User()
    user.set_password("testpassword")
    assert user.check_password("testpassword") == True

def test_check_incorrect_password():
    user = User()
    user.set_password("testpassword")
    assert user.check_password("testpassword") == False

def test_empty_todoitem(app_context):
    assert TodoItem.query.count() == 0

def test_todo_to_dict_includes_nested_comments(app_context):
    todo = TodoItem(title='Todo with comments', done=True)
    comment = Comment(message='Nested', todo=todo)
    db.session.add_all([todo, comment])
    db.session.commit()
    
    test_todo = TodoItem.query.get(todo.id)
    assert len(test_todo.comments) == 1