import { useState } from 'react';
import './App.css';

function TodoItem({ todo, toggleDone, deleteTodo, addNewComment }) {
  const [newComment, setNewComment] = useState("");

  return (
    <li className="todo-item">
      <div className="todo-content">
        <span 
          className={todo.done ? "done-text" : ""}
          onClick={() => toggleDone(todo.id)}
          style={{ cursor: 'pointer' }}
          role="button" // เพิ่ม role ให้เทสมองเห็นเป็นปุ่มกด
        >
          {todo.done ? "✅ " : "⬜ "} 
          {todo.title}
        </span>
        <button className="delete-btn" onClick={() => deleteTodo(todo.id)}>
          Delete
        </button>
      </div>

      <div className="comment-section">
        {/* เพิ่มเงื่อนไข TDD: ถ้าไม่มี comment ให้แสดง No comments ถ้ามีให้แสดงจำนวน */}
        {(!todo.comments || todo.comments.length === 0) ? (
          <p className="no-comments-text">No comments</p>
        ) : (
          <>
            <p className="comment-count-text">{todo.comments.length} comments</p>
            <ul className="comment-list">
              {todo.comments.map((comment) => (
                <li key={comment.id}>💬 {comment.message}</li>
              ))}
            </ul>
          </>
        )}
        
        <div className="add-comment">
          <input
            type="text"
            placeholder="Add a comment..."
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
          />
          <button onClick={() => {
            addNewComment(todo.id, newComment);
            setNewComment(""); 
          }}>
            Send
          </button>
        </div>
      </div>
    </li>
  );
}

export default TodoItem;