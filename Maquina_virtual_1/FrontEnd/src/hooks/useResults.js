
const getSearchResponse= async (query) => {
  const data = await fetch(
    `http://localhost:8000/api/elasticsearch/search?q=${query}`
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
      return data.data;
    default:
      return [];
  }
};

const getAllResults= async () => {
  const data = await fetch(`http://localhost:8000/api/elasticsearch/search`)
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
      return data.data;
    default:
      return [];
  }
};

// hook que entrega resultados a partir de una busqueda
export async function useResults(query) {
  let results;

  if (query === undefined || query === null || query === "") {
    results = await getAllResults();
  } else {
    results = await getSearchResponse(query);
  }

  const mappedResults = results?.map((res) => ({
    id: res.link,
    title: res.maintitle,
    content: res.content,
    url: res.link,
  }));

  return mappedResults;
}
