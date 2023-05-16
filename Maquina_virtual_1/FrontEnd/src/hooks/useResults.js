import axios from "axios";

import json from "../db/obj.json";

const obtener_busqueda = async (results) => {
  await axios
    .get("http://localhost:8000/api/elasticsearch/search?q=pcfactory")
    .then((response) => {
      // La respuesta del servidor está disponible en 'response.data'
      console.log(response.data);
      if (response.success === true) {
        console.log(response.data);
        return response.data;
      }
    })
    .catch((error) => {
      console.log("un error... ");
      console.error(error);
    });
};

const obtener_busqueda2 = async (query) => {
  console.log('FETCHING FROM "obtener_busqueda2 (QUERY)"');
  const data = await fetch(
    `http://0.0.0.0:8000/api/elasticsearch/search?q=${query}}`
  )
    .then((response) => response.json())
    .then((data) => {
      // Manipular los datos de respuesta
      return data;
    })
    .catch((error) => {
      // Manejar errores
      console.error(error);
    });

  switch (data?.success) {
    case true:
      console.log("data.success === true");
      console.log(data.data);
      return data.data;
    default:
      return [];
  }
};

const obtener_busqueda_default = async () => {
  console.log('FETCHING FROM "obtener_busqueda_default"');
  const data = await fetch(`http://0.0.0.0:8000/api/elasticsearch/search`)
    .then((response) => response.json())
    .then((data) => {
      // Manipular los datos de respuesta
      return data;
    })
    .catch((error) => {
      // Manejar errores
      console.error(error);
    });

  switch (data?.success) {
    case true:
      console.log("data.success === true");
      return data.data;
    default:
      return [];
  }
};

export async function useResults(query) {
  // const results = json;

  let results;
  if (query === undefined || query === null || query === "") {
    results = await obtener_busqueda_default();
  } else {
    results = await obtener_busqueda2(query);
  }
  console.log("FROM useResults: results: ", results);

  const mappedResults = results?.map((res) => ({
    id: res.link,
    title: res.maintitle,
    content: res.content,
    url: res.link,
  }));

  return mappedResults;
}
