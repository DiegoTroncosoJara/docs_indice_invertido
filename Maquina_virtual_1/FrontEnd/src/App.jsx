import "./index.css";

import { Results } from "./components/Results";
import { useRef, useState, useEffect } from "react";
import { useResults } from "./hooks/useResults";
import { PlusOutlined  } from '@ant-design/icons';
import { Modal } from "./components/Modal";


function App() {
  const [results, setResults] = useState([]);
  const inputRef = useRef();
  const [query, setQuery] = useState("");
  const [error, setError] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);

  useEffect(() => {
    fetchData();
  }, [query]);

  const handleSubmit = (e) => {
    e.preventDefault();
    const newQuery = inputRef.current.value;

    setQuery(newQuery);

    if (newQuery === "") {
      fetchData();
      return;
    }

    if (newQuery.length <= 3) {
      setError("La palabra debe tener más de 3 letras");
      return;
    }

    fetchData(newQuery);
    setQuery("");
    setError(null);
  };

  const fetchData = async (query) => {
    const results = await useResults(query);
    setResults(results);
  };

  const handleModalOpen = () => {
    setModalOpen(true);
  };
  
  const handleModalClose = () => {
    setModalOpen(false);
  };

  return (
    <div className="w-full min-h-screen bg-[conic-gradient(at_right,_var(--tw-gradient-stops))] from-indigo-200 via-slate-600 to-indigo-200">
      <h3 className="items-center justify-center pt-10 font-bold text-center font-patrick text-8xl text-zinc-50">
        Buscador de palabras
      </h3>
      <div className="flex items-center justify-center pt-14">
        <button
          type="submit"
          onClick={handleSubmit}
          className="px-4 py-2 font-bold text-black bg-white rounded-full hover:bg-slate-400"
        >
          Buscar
        </button>
        <input
          ref={inputRef}  
          placeholder="Computadores, nintendo, IA, etc."
          className="w-1/4 py-2 pl-3 ml-1 bg-white border rounded-lg appearance-none sm:text-md"
        />
        <button
          data-modal-target="popup-modal"
          data-modal-toggle="popup-modal"
          className="px-2 py-1 ml-2 bg-white rounded-2xl hover:bg-slate-400"
          type="button"
          onClick={handleModalOpen}
        >
          <PlusOutlined />
        </button>
        
      </div>

      {error && (
        <p className="flex items-center justify-center text-red-500">{error}</p>
      )}
      <Results json={results} />

      <Modal isOpen={modalOpen} onClose={handleModalClose} />
    </div>
  );
}

export default App;
