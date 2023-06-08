-- -------------------------------------------------------------
-- TablePlus 5.3.6(496)
--
-- https://tableplus.com/
--
-- Database: documentos
-- Generation Time: 2023-05-09 10:03:45.4920
-- -------------------------------------------------------------


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


CREATE TABLE `descarga_estado` (
  `id` int NOT NULL AUTO_INCREMENT,
  `descarga_iniciada` datetime DEFAULT NULL,
  `error` tinyint(1) DEFAULT NULL,
  `descarga_completada` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `documentos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `link` varchar(255) DEFAULT NULL,
  `hora_desc` time DEFAULT NULL,
  `path` varchar(255) DEFAULT NULL,
  `ultima_desc` time DEFAULT NULL,
  `id_esclavo` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `documentos` (`id`, `link`, `hora_desc`, `path`, `ultima_desc`, `id_esclavo`) VALUES
(1, 'https://www.pcfactory.cl/', '16:30:00', '/Users/basti/Desktop/Primer_Semestre_2023/distribuidos/docs_indice_invertido/code/scraping_dato/esclavo0/data/www.pcfactory.cl_25.txt', '08:12:23', 0),
(2, 'https://www.falabella.com/', '17:00:00', '/Users/basti/Desktop/Primer_Semestre_2023/distribuidos/docs_indice_invertido/code/scraping_dato/esclavo1/data/www.falabella.com_26.txt', '08:12:23', 1),
(3, 'https://www.uach.cl/', '17:00:00', '/Users/basti/Desktop/Primer_Semestre_2023/distribuidos/docs_indice_invertido/code/scraping_dato/esclavo2/data/www.uach.cl_20.txt', '08:12:23', 2),
(4, 'https://www.solotodo.cl/', '13:00:00', '/Users/basti/Desktop/Primer_Semestre_2023/distribuidos/docs_indice_invertido/code/scraping_dato/esclavo0/data/www.solotodo.cl_24.txt', '08:12:24', 0),
(5, 'https://www.uchile.cl/', '12:00:00', '/Users/basti/Desktop/Primer_Semestre_2023/distribuidos/docs_indice_invertido/code/scraping_dato/esclavo1/data/www.uchile.cl_22.txt', '08:12:24', 1),
(6, 'https://www.youtube.com/', '17:23:00', '/Users/basti/Desktop/Primer_Semestre_2023/distribuidos/docs_indice_invertido/code/scraping_dato/esclavo2/data/www.youtube.com_24.txt', '08:12:24', 2),
(7, 'https://www.pcfactory.cl/producto/43968-gear-desktop-intel-pentium-gold-g6405-4gb-1tb', '11:00:00', '/Users/basti/Desktop/Primer_Semestre_2023/distribuidos/docs_indice_invertido/code/scraping_dato/esclavo0/data/www.pcfactory.cl_85.txt', '08:12:26', 0);

-- INSERT INTO `documentos` (`id`, `link`, `hora_desc`, `path`, `ultima_desc`, `id_esclavo`) VALUES
-- (1, 'https://www.pcfactory.cl/', '16:30:00', '/home/alex/Desktop/info288/proyecto/docs_indice_invertido/Maquina_Virtual_5.0/Descarga_Tramo_0/data/www.pcfactory.cl_25.txt', '08:12:23', 0),
-- (2, 'https://www.falabella.com/', '17:00:00', '/home/alex/Desktop/info288/proyecto/docs_indice_invertido/Maquina_virtual_5.1/Descarga_tramo_1/data/www.falabella.com_26.txt', '08:12:23', 1);


-- /home/alex/Desktop/info288/proyecto/docs_indice_invertido/Maquina_Virtual_5.0/Descarga_Tramo_0/data
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;