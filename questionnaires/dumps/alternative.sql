CREATE DATABASE  IF NOT EXISTS `questionnaires` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `questionnaires`;
-- MySQL dump 10.13  Distrib 5.6.13, for osx10.6 (i386)
--
-- Host: localhost    Database: questionnaires
-- ------------------------------------------------------
-- Server version	5.6.17

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `questionnaires_alternative`
--

DROP TABLE IF EXISTS `questionnaires_alternative`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `questionnaires_alternative` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_id` int(11) NOT NULL,
  `score` smallint(6) NOT NULL,
  `description` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `questionnaires_answer_25110688` (`question_id`),
  CONSTRAINT `question_id_refs_id_fd6121cf` FOREIGN KEY (`question_id`) REFERENCES `questionnaires_question` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `questionnaires_alternative`
--

LOCK TABLES `questionnaires_alternative` WRITE;
/*!40000 ALTER TABLE `questionnaires_alternative` DISABLE KEYS */;
INSERT INTO `questionnaires_alternative` VALUES (1,1,-2,'90 million'),(2,1,-1,'150 million'),(3,1,2,'210 million'),(4,2,-1,'Protestant Christianity'),(5,2,2,'Roman Catholicism'),(6,2,0,'Spiritism'),(7,2,-1,'No religion'),(8,3,-1,'Black'),(9,3,1,'Mixed race'),(10,3,-2,'Asian'),(11,3,2,'White'),(12,4,-2,'Salsa'),(13,4,-2,'Tango'),(14,4,2,'Samba'),(15,5,2,'Angra'),(16,5,2,'Sepultura'),(17,5,-2,'Gorgoroth'),(18,5,2,'Krisiun'),(19,5,-2,'Gorod'),(20,6,-2,'Spanish'),(21,6,-2,'French'),(22,6,2,'Portuguese'),(23,6,-2,'Portuguese and Spanish'),(24,6,-2,'Brazilian'),(25,7,0,'Republic'),(26,7,2,'Monarchy'),(27,7,-1,'Theocracy');
/*!40000 ALTER TABLE `questionnaires_alternative` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-04-23 15:50:07
