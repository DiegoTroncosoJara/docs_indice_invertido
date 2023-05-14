
import { searchResults } from "../services/results";


import { useState } from "react";


export function useResults ({ search }){
  const [responseResults, setResponseResults] = useState([])

  const getResults = async () => {
    const newResults = await searchResults({search})
    setResponseResults(newResults)
    // console.log("useResults.js search: ", search);
    // setResponseResults(json)

  }


  return {results: responseResults, getResults}
}