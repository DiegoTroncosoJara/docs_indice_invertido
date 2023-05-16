import "./index.css";

import { Results } from "./components/Results";
import { useRef, useState, useEffect } from "react";
import { useResults } from "./hooks/useResults";

function App() {
  // const { results } = useResults();
  const [results, setResults] = useState([]);

  const inputRef = useRef();
  const [query, setQuery] = useState("");
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      setResults(await useResults());
    };
    fetchData();
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();

    const fetchData = async () => {
      setResults(await useResults(newQuery));
    };

    const newQuery = inputRef.current.value;
    setQuery(newQuery);
    console.log("newQuery: ", newQuery);
    if (newQuery == "") {
      // Si no hay nada en el input, se muestran todos los resultados
      fetchData();
      return;
    }

    if (newQuery.length <= 3) {
      setError("La palabra debe tener más de 3 letras");
      return;
    }

    fetchData();
    setQuery("");
    setError(null);
  };

  console.log("results: ", results);
  return (
    <div className="w-full min-h-screen bg-cyan-600">
      <h3 className="items-center justify-center pt-10 font-bold text-center text-8xl text-zinc-50">
        BUSCADOR DE PALABRAS
      </h3>
      <form className="flex items-center justify-center pt-14">
        <input
          type="submit"
          onClick={handleSubmit}
          className="px-4 py-2 font-bold text-black bg-white rounded-full hover:bg-slate-400"
        ></input>
        <input
          ref={inputRef}
          placeholder="Computadores, nintendo, IA, etc."
          className="w-1/4 py-2 pl-3 ml-1 bg-white border rounded-lg appearance-none sm:text-md"
        ></input>
      </form>
      {error && (
        <p className="flex items-center justify-center text-red-500">{error}</p>
      )}
      <Results json={results} />
    </div>
  );
}

export default App;
