import { Card } from "./Card";

function ListOfResults({ json }) {
  return (
    // <div className="grid grid-cols-4 gap-4 pt-10 justify-items-center">
    //   {
    //     json.map(obj => (
    //     <Card url={obj.url} title={obj.title} key={obj.id}> {obj.content} </Card>
    //     ))
    //   }
    // </div>
    <div className="container mx-auto">
      <div className="grid grid-cols-1 gap-4 pt-10 md:grid-cols-2 lg:grid-cols-4">
        {json.map((obj) => (
          <Card url={obj.url} title={obj.title} key={obj.id}>
            {obj.content}
          </Card>
        ))}
      </div>
    </div>
  );
}

function NoResults() {
  return <h1>No se encontraron resultados para esta búsqueda.</h1>;
}

export function Results({ json }) {
  const hasResults = json?.length > 0;

  return hasResults ? <ListOfResults json={json} /> : <NoResults />;
}
