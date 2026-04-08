import TodoItem from './TodoItem.jsx';
import { useState, useEffect } from 'react';
import './App.css';

// เปลี่ยน URL เป็นแบบ Relative สำหรับทำ Deployment ขึ้น Server
const TODOLIST_API_URL = '/api/todos/';

function App() {
  const [todoList, setTodoList] = useState([]);
  const [newTodo, setNewTodo] = useState("");

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

  async function addNewComment(todoId, newComment) {
    if (!newComment || newComment.trim() === "") return;

    try {
      const response = await fetch(`${TODOLIST_API_URL}${todoId}/comments/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: newComment }),
      });

      if (response.ok) {
        await fetchTodoList();
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
          <TodoItem 
            key={todo.id} 
            todo={todo}
            toggleDone={toggleDone}
            deleteTodo={deleteTodo}
            addNewComment={addNewComment}
          />
        ))}
      </ul>
    </div>
  );
}

export default App;