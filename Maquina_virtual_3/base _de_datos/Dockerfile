FROM mysql:latest

# Copiar el archivo SQL a la carpeta "docker-entrypoint-initdb.d"
# para que se ejecute automáticamente al iniciar el contenedor
COPY documentos.sql /docker-entrypoint-initdb.d/

# Definir las variables de entorno para configurar la base de datos
ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=documentos

# Opcional: Configurar el puerto en el que escucha MySQL
# Por defecto, MySQL utiliza el puerto 3306
# EXPOSE 3306

# Opcional: Definir otros ajustes de configuración de MySQL
# COPY my.cnf /etc/mysql/my.cnf

# Opcional: Añadir cualquier otro archivo o configuración necesario

# Comando CMD para iniciar el servidor MySQL
CMD ["mysqld"]
