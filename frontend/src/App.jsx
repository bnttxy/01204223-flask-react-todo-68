import { useState, useEffect } from 'react';
import './App.css';

const TODOLIST_API_URL = 'http://127.0.0.1:5000/api/todos/';

function App() {
  const [todoList, setTodoList] = useState([]);
  const [newTodo, setNewTodo] = useState("");
  
  // State สำหรับเก็บข้อความ Comment ของแต่ละ Todo (Key=ID, Value=Message)
  const [newComments, setNewComments] = useState({});

  async function fetchTodoList() {
    try {
      const response = await fetch(TODOLIST_API_URL);
      const data = await response.json();
      setTodoList(data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  }

  useEffect(() => {
    fetchTodoList();
  }, []);

  async function addNewTodo() {
    if (newTodo.trim() === "") return;
    try {
      const response = await fetch(TODOLIST_API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: newTodo }),
      });
      if (response.ok) {
        setNewTodo("");
        await fetchTodoList();
      }
    } catch (error) {
      console.error("Error adding todo:", error);
    }
  }

  async function toggleDone(id) {
    try {
      const response = await fetch(`${TODOLIST_API_URL}${id}/toggle/`, {
        method: 'PATCH',
      });
      if (response.ok) await fetchTodoList();
    } catch (error) {
      console.error("Error toggling todo:", error);
    }
  }

  async function deleteTodo(id) {
    try {
      const response = await fetch(`${TODOLIST_API_URL}${id}/`, {
        method: 'DELETE',
      });
      if (response.ok) await fetchTodoList();
    } catch (error) {
      console.error("Error deleting todo:", error);
    }
  }

  async function addNewComment(todoId) {
    const message = newComments[todoId];
    if (!message || message.trim() === "") return;

    try {
      const response = await fetch(`${TODOLIST_API_URL}${todoId}/comments/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message }),
      });

      if (response.ok) {
        setNewComments({ ...newComments, [todoId]: "" }); // Clear input
        await fetchTodoList(); // Reload to show new comment
      }
    } catch (error) {
      console.error("Error adding comment:", error);
    }
  }

  return (
    <div className="App">
      <h1>Todo List + Comments</h1>
      
      <div className="add-todo">
        <input
          type="text"
          placeholder="New task..."
          value={newTodo}
          onChange={(e) => setNewTodo(e.target.value)}
        />
        <button onClick={addNewTodo}>Add Task</button>
      </div>

      <ul className="todo-list">
        {todoList.map((todo) => (
          <li key={todo.id} className="todo-item">
            <div className="todo-content">
              <span 
                className={todo.done ? "done-text" : ""}
                onClick={() => toggleDone(todo.id)}
                style={{ cursor: 'pointer' }}
              >
                {todo.done ? "✅ " : "⬜ "} 
                {todo.title}
              </span>
              <button className="delete-btn" onClick={() => deleteTodo(todo.id)}>
                Delete
              </button>
            </div>

            {/* ส่วนแสดง Comments */}
            <div className="comment-section">
              {todo.comments && todo.comments.length > 0 && (
                <ul className="comment-list">
                  {todo.comments.map((comment) => (
                    <li key={comment.id}>💬 {comment.message}</li>
                  ))}
                </ul>
              )}
              
              {/* ส่วน Input เพิ่ม Comment */}
              <div className="add-comment">
                <input
                  type="text"
                  placeholder="Add a comment..."
                  value={newComments[todo.id] || ""}
                  onChange={(e) =>
                    setNewComments({ ...newComments, [todo.id]: e.target.value })
                  }
                />
                <button onClick={() => addNewComment(todo.id)}>Send</button>
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;