import { Results } from "./Results";
import json from "../db/obj.json";
export function Search() {
  return (
    <div className="min-h-screen bg-cyan-600">
      <h3 className="items-center justify-center pt-10 font-bold text-center text-8xl text-zinc-50">
        BUSCADOR DE PALABRAS
      </h3>
      <div className="flex items-center justify-center pt-14">
        <button className="px-4 py-2 font-bold text-black bg-white rounded-full hover:bg-slate-100">
          Buscar
        </button>
        <input className="py-2 pl-3 ml-1 bg-white border rounded-lg appearance-none pr-52 sm:text-md"></input>
      </div>
      <Results json={json} />
    </div>
  );
}
