from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from flask_migrate import Migrate

# --- Config ---
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(app, model_class=Base)
migrate = Migrate(app, db)

# --- Models ---

class TodoItem(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    done: Mapped[bool] = mapped_column(default=False)
    
    # Relationship: One-to-Many (1 Todo มีหลาย Comment)
    # cascade="all, delete" = ถ้าลบ Todo ให้ลบ Comment ทั้งหมดของมันด้วย
    comments: Mapped[list["Comment"]] = relationship(back_populates="todo", cascade="all, delete")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "done": self.done,
            # ส่งรายการ comments กลับไปหา frontend ด้วย
            "comments": [comment.to_dict() for comment in self.comments]
        }

class Comment(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    message: Mapped[str] = mapped_column(String(250))
    
    # Foreign Key เชื่อมกับ TodoItem
    todo_id: Mapped[int] = mapped_column(ForeignKey('todo_item.id', ondelete="CASCADE"))
    
    # Relationship ย้อนกลับ
    todo: Mapped["TodoItem"] = relationship(back_populates="comments")

    def to_dict(self):
        return {
            "id": self.id,
            "message": self.message,
            "todo_id": self.todo_id
        }

# --- Routes (API) ---

@app.route('/api/todos/', methods=['GET'])
def get_todos():
    todos = TodoItem.query.all()
    return jsonify([todo.to_dict() for todo in todos])

@app.route('/api/todos/', methods=['POST'])
def add_todo():
    data = request.get_json()
    if 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
        
    todo = TodoItem(title=data['title'], done=data.get('done', False))
    db.session.add(todo)
    db.session.commit()
    return jsonify(todo.to_dict())

@app.route('/api/todos/<int:id>/toggle/', methods=['PATCH'])
def toggle_todo(id):
    todo = TodoItem.query.get_or_404(id)
    todo.done = not todo.done
    db.session.commit()
    return jsonify(todo.to_dict())

@app.route('/api/todos/<int:id>/', methods=['DELETE'])
def delete_todo(id):
    todo = TodoItem.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted successfully'})

@app.route('/api/todos/<int:todo_id>/comments/', methods=['POST'])
def add_comment(todo_id):
    todo = TodoItem.query.get_or_404(todo_id)
    data = request.get_json()
    
    if not data or 'message' not in data:
        return jsonify({'error': 'Message is required'}), 400

    comment = Comment(message=data['message'], todo_id=todo.id)
    db.session.add(comment)
    db.session.commit()
    
    return jsonify(comment.to_dict())

if __name__ == '__main__':
    app.run(debug=True)