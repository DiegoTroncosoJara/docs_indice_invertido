
const getSearchResponse= async (query) => {
  const data = await fetch(
    `http://0.0.0.0:8000/api/elasticsearch/search?q=${query}`
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

const getMultiWordSearchResponse= async (query) => {

  let multi_searchs =  query.join("+");

  const data = await fetch(
    `http://0.0.0.0:8000/api/elasticsearch/search?q=${multi_searchs}`
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

  // Si no hay palabras en el buscador se muestran todos los resultados
  if (query === undefined || query === null || query === "") {
    results = await getAllResults();
  } else {
    let arr_words = query.split(' ');

    // Se muestran varias busquedas
    if(arr_words > 1){
      results = await getMultiWordSearchResponse(arr_words);
    
    // Se muestra una busqueda
    }else{
      results = await getSearchResponse(arr_words);
    }
  }
  console.log("results: ", results);
  const mappedResults = results?.map((res) => ({
    id: res.link,
    title: res.maintitle,
    content: res.content,
    url: res.link,
  }));

  return mappedResults;
}
