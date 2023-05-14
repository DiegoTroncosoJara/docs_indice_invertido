import "./index.css";

import { Results } from "./components/Results";
import { useRef, useState} from "react";
import { useResults } from "./hooks/useResults";




function App() {
  // hook para obtener busqueda y modificar busqueda
  const [search, updateSearch] = useState('')
  // hook para obtener resultados. Llama a los endpoint
  const {results, getResults} = useResults({search})
  const inputRef = useRef()



  const handleSubmit = (event) => {
    event.preventDefault()
    getResults()
  }

  const handleChange = ( event ) => {
    updateSearch(event.target.value)
  }
  
  return (
    <div className="w-full min-h-screen bg-cyan-600">
        <h3 className="items-center justify-center pt-10 font-bold text-center text-8xl text-zinc-50">
            BUSCADOR DE PALABRAS
        </h3>
        <form className="flex items-center justify-center pt-14" onSubmit={handleSubmit}>
            <input ref={inputRef} onChange={handleChange} value={search} placeholder="Computadores, nintendo, IA, etc." className="w-1/4 py-2 pl-3 ml-1 bg-white border rounded-lg appearance-none sm:text-md"></input>
            <button type="submit"className="px-4 py-2 font-bold text-black bg-white rounded-full hover:bg-slate-400">
                Buscar
            </button>
        </form>
        <Results json={results}/>
    </div>
  );
}

export default App;
