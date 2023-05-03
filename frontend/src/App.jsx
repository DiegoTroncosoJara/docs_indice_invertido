import "./index.css";

import { Results } from "./components/Results";
import { useRef, useState } from "react";
import { useResults } from "./hooks/useResults";



function App() {
  const {results} = useResults()
  const inputRef = useRef()
  const [query, setQuery] = useState('')
  const [error, setError] = useState(null)


  const handleClick = () => {
    const newQuery = inputRef.current.value 
    setQuery(newQuery)
    console.log("newQuery: ", newQuery);
    if (newQuery == ''){
        setError('No se ha ingresado una palabra')
        return
      }
  
    if (newQuery.length <= 3){
      setError('La palabra debe tener más de 3 letras')
      return
    }
  
    setError(null)
  }

  
  
  return (
    <div className="w-full min-h-screen bg-cyan-600">
        <h3 className="items-center justify-center pt-10 font-bold text-center text-8xl text-zinc-50">
            BUSCADOR DE PALABRAS
        </h3>
        <div className="flex items-center justify-center pt-14">
            <button onClick={handleClick}  className="px-4 py-2 font-bold text-black bg-white rounded-full hover:bg-slate-400">
                Buscar
            </button>
            <input ref={inputRef} placeholder="Computadores, nintendo, IA, etc." className="w-1/4 py-2 pl-3 ml-1 bg-white border rounded-lg appearance-none sm:text-md"></input>
        </div>
        {error && <p className="flex items-center justify-center text-red-500">{error}</p>}
        <Results json={results}/>
    </div>
  );
}

export default App;
