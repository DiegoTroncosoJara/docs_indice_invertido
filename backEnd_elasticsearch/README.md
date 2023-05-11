# Integración FastAPI, Uvicorn y Elasticsearch

## Instalación FastAPI y Uvicorn

- **FastAPI** creación de API's
- **Uvicorn** servidor ASGI

```bash
pip install fastapi
pip install "uvicorn[standard]"
```

## Ejecución - FastAPI y Uvicorn

**PORT: 8000**

```bash
uvicorn main:app --reload
```

## Ejecución - Elasticsearch

**DEFAULT PORT: 9200**

**PATH: elasticsearch-8.7.0**

```bash
./bin/elasticsearch
```

## Endpoints

### GET /api/elasticsearch/create

Este endpoint crea el índice. Si el índice ya existe, te lo hace saber.

### GET /api/elasticsearch/refresh

Este endpoint refresca el índice, y lee los archivos de **data** para indexarlos. Si archivo (ej: ripley.html) ya existe, te lo muestra en un arreglo de `already_exists`, de lo contrario lo indexa y aparecerá en `successfully_indexed`.

### GET /api/elasticsearch/search?q={query}

Este endpoint busca en el índice, según el query que se le pase. Si no se le pasa query, retorna un "error".

### POST /api/elasticsearch/linkPath_scrapper

```json
{
  "linkPath_scrapper": "/home/alex/Desktop/info288/proyecto/docs_indice_invertido/scraping/esclavo0/data/www.pcfactory.cl_85.txt"
}
```
