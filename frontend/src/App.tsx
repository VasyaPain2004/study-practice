import { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

type noteType = {
  id: number;
  title: string;
  content: string;
};

const App: React.FC = () => {
  const [notes, setNotes] = useState<noteType[] | null>([]);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");

  const API_URL = "http://localhost:5000/api/notes";

  useEffect(() => {
    fetchNotes();
  }, []);

  const fetchNotes = async () => {
    try {
      const response = await axios.get(API_URL);
      setNotes(response.data);
    } catch (error) {
      console.error("Ошибка при загрузке заметок:", error);
    }
  };

  const deleteNote = async (id: number) => {
    try {
      await axios.delete(`${API_URL}/${id}`);
      fetchNotes(); 
    } catch (error) {
      console.error("Ошибка при удалении:", error);
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!title || !content) return;

    try {
      await axios.post(API_URL, { title, content });
      setTitle("");
      setContent("");
      fetchNotes();
    } catch (error) {
      console.error("Ошибка при добавлении:", error);
    }
  };

  return (
    <div className="wrapper">
      <h1 className="title">Мои заметки</h1>

      <form className="form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Заголовок"
          className="input"
        />
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="Текст заметки"
          className="textarea"
        />
        <button className="btn-submit">
          Добавить заметку
        </button>
      </form>

      {notes && notes.length > 0 ? (
        notes.map((note) => (
          <div key={note.id} className="note">
            <h3 className="note-title">{note.title}</h3>
            <p className="note-content">{note.content}</p>
            <button onClick={() => deleteNote(note.id)} className="btn-delete">
              Удалить
            </button>
          </div>
        ))
      ) : (
        <h3>Заметок пока что нет</h3>
      )}
    </div>
  );
};

export default App;
