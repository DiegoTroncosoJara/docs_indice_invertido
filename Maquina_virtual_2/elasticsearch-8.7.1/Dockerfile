# Utiliza la imagen base de Elasticsearch
FROM docker.elastic.co/elasticsearch/elasticsearch:8.7.1

# Copia el contenido de la carpeta "config" al directorio "/usr/share/elasticsearch/config" en el contenedor
COPY ./config /usr/share/elasticsearch/config

# Expone los puertos necesarios para Elasticsearch
EXPOSE 9200 9300

# Inicia Elasticsearch cuando se ejecute el contenedor
CMD ["elasticsearch"]
