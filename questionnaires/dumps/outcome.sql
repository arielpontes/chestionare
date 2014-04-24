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
-- Table structure for table `questionnaires_outcome`
--

DROP TABLE IF EXISTS `questionnaires_outcome`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `questionnaires_outcome` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `questionnaire_id` int(11) NOT NULL,
  `title` varchar(30) NOT NULL,
  `message` longtext NOT NULL,
  `minimum_score` smallint(6) NOT NULL DEFAULT '-32768',
  PRIMARY KEY (`id`),
  KEY `questionnaires_outcome_dfaab653` (`questionnaire_id`),
  CONSTRAINT `questionnaire_id_refs_id_d7193fa2` FOREIGN KEY (`questionnaire_id`) REFERENCES `questionnaires_questionnaire` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `questionnaires_outcome`
--

LOCK TABLES `questionnaires_outcome` WRITE;
/*!40000 ALTER TABLE `questionnaires_outcome` DISABLE KEYS */;
INSERT INTO `questionnaires_outcome` VALUES (1,3,'Mandou muito!','Congrats, você mandou muito! (You did very well)',10),(2,3,'Hum… mais ou menos…','Well, you did ok… let\'s hope it goes better next time.',5),(3,3,'Putz…','Sorry, hope you do better next time!',0),(4,3,'Que M***','Sorry, but you really know sh** about Brazil.',-32768);
/*!40000 ALTER TABLE `questionnaires_outcome` ENABLE KEYS */;
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
