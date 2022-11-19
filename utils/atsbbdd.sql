-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: localhost    Database: atsbbdd
-- ------------------------------------------------------
-- Server version	8.0.27

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `candidatos`
--

DROP TABLE IF EXISTS `candidatos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `candidatos` (
  `idcandidato` int NOT NULL AUTO_INCREMENT,
  `nombrecandidato` varchar(45) NOT NULL,
  `apellidocandidato` varchar(45) NOT NULL,
  `telefono` int DEFAULT NULL,
  `mail` varchar(45) DEFAULT NULL,
  `linkedin` varchar(45) DEFAULT NULL,
  `rol` varchar(45) DEFAULT NULL,
  `idEstado` int NOT NULL,
  PRIMARY KEY (`idcandidato`),
  KEY `idestado_idx` (`idEstado`),
  CONSTRAINT `idestado_estadosid` FOREIGN KEY (`idEstado`) REFERENCES `estados` (`estadosid`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `candidatos`
--

LOCK TABLES `candidatos` WRITE;
/*!40000 ALTER TABLE `candidatos` DISABLE KEYS */;
INSERT INTO `candidatos` VALUES (1,'Camila','Carbone',1566855759,'paulacamilacarbone@gmail.com','www.linkedin.com/paulacarbone',NULL,1),(2,'Cristina ','Otero',1212121212,'cristina@hotmail.com','www.linkedin.com/cristinaotero',NULL,1),(3,'Vero','Balsamo',12345,'veritobalsamo@email.com','www.linkedin.com/vero',NULL,1);
/*!40000 ALTER TABLE `candidatos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `candidatos_estados`
--

DROP TABLE IF EXISTS `candidatos_estados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `candidatos_estados` (
  `idestadocandidato` int NOT NULL AUTO_INCREMENT,
  `fecha` datetime NOT NULL,
  `idcandidato` int NOT NULL,
  `estadoid` int NOT NULL,
  PRIMARY KEY (`idestadocandidato`),
  UNIQUE KEY `idestadousuario_UNIQUE` (`idestadocandidato`),
  KEY `candidatos_estados_candidatos_idx` (`idcandidato`),
  KEY `candidatos_estados_estados_idx` (`estadoid`),
  CONSTRAINT `candidatos_estados_candidato` FOREIGN KEY (`idcandidato`) REFERENCES `candidatos` (`idcandidato`) ON DELETE CASCADE,
  CONSTRAINT `candidatos_estados_estados` FOREIGN KEY (`estadoid`) REFERENCES `estados` (`estadosid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `candidatos_estados`
--

LOCK TABLES `candidatos_estados` WRITE;
/*!40000 ALTER TABLE `candidatos_estados` DISABLE KEYS */;
INSERT INTO `candidatos_estados` VALUES (1,'2022-05-14 13:00:00',1,1),(2,'2022-07-20 15:50:00',2,1),(3,'2022-11-01 10:35:00',3,1);
/*!40000 ALTER TABLE `candidatos_estados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estados`
--

DROP TABLE IF EXISTS `estados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estados` (
  `estadosid` int NOT NULL,
  `estadoNombre` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`estadosid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estados`
--

LOCK TABLES `estados` WRITE;
/*!40000 ALTER TABLE `estados` DISABLE KEYS */;
INSERT INTO `estados` VALUES (1,'Contactado'),(2,'No interesado'),(3,'Entrevista HR'),(4,'Entrevista Técnica'),(5,'Oferta'),(6,'Contratado');
/*!40000 ALTER TABLE `estados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  `apellido` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  `usuario` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'leonor','perez','leop','12345');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-11-19 19:15:34
