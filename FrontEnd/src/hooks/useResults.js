import axios from 'axios';

import json from "../db/obj.json";


const  obtener_busqueda = async(results) => {
  
  
  await axios.get("http://0.0.0.0:8000/api/elasticsearch/search?q=pcfactory").then(response => {
    // La respuesta del servidor está disponible en 'response.data'
    console.log(response.data);
    if(response.success === true){
      console.log(response.data)
      return  response.data;

    }
    
  })
  .catch(error => {
    console.log("un error... ")
    console.error(error);
  });

}


const obtener_busqueda2 = async(results) => { 
  fetch('http://0.0.0.0:8000/api/elasticsearch/search?q=pcfactory')
  .then(response => response.json())
  .then(data => {
    // Manipular los datos de respuesta
    console.log(data);
  })
  .catch(error => {
    // Manejar errores
    console.error(error);
  });


}

export function useResults (){
    const results = json
    obtener_busqueda2(results)
    //const data = obtener_busqueda(results);
    //console.log(results)



    const mappedResults = results?.map(res => ({
      id: res.id,
      title: res.title,
      content: res.content,
      url: res.url
    }))
    return {results: mappedResults}
  }