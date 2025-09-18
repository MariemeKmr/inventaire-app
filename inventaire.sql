-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: inventaire
-- ------------------------------------------------------
-- Server version	10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alerte`
--
CREATE DATABASE IF NOT EXISTS `inventaire` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `inventaire`;
DROP TABLE IF EXISTS `alerte`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alerte` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` enum('REAPPRO','INFO') NOT NULL,
  `produit_id` int(11) DEFAULT NULL,
  `niveau` enum('INFO','WARN','CRIT') NOT NULL DEFAULT 'INFO',
  `message` text NOT NULL,
  `resolue` tinyint(1) NOT NULL DEFAULT 0,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `ix_alerte_prod_date` (`produit_id`,`created_at`),
  CONSTRAINT `fk_alerte_produit` FOREIGN KEY (`produit_id`) REFERENCES `produit` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alerte`
--

LOCK TABLES `alerte` WRITE;
/*!40000 ALTER TABLE `alerte` DISABLE KEYS */;
/*!40000 ALTER TABLE `alerte` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categorie`
--

DROP TABLE IF EXISTS `categorie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `categorie` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nom` (`nom`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categorie`
--

LOCK TABLES `categorie` WRITE;
/*!40000 ALTER TABLE `categorie` DISABLE KEYS */;
/*!40000 ALTER TABLE `categorie` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dette`
--

DROP TABLE IF EXISTS `dette`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dette` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nom_client` varchar(150) NOT NULL,
  `telephone` varchar(50) DEFAULT NULL,
  `montant` decimal(10,2) NOT NULL,
  `date_dette` date NOT NULL,
  `produits_txt` text DEFAULT NULL,
  `remarques` text DEFAULT NULL,
  `statut` enum('EN_COURS','PARTIEL','PAYEE') NOT NULL DEFAULT 'EN_COURS',
  PRIMARY KEY (`id`),
  KEY `ix_dette_statut_date` (`statut`,`date_dette`),
  KEY `ix_dette_date` (`date_dette`),
  CONSTRAINT `chk_dette_montant` CHECK (`montant` > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dette`
--

LOCK TABLES `dette` WRITE;
/*!40000 ALTER TABLE `dette` DISABLE KEYS */;
/*!40000 ALTER TABLE `dette` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `historique`
--

DROP TABLE IF EXISTS `historique`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `historique` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type_action` varchar(50) NOT NULL,
  `utilisateur_id` int(11) DEFAULT NULL,
  `utilisateur_email` varchar(150) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `date_action` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `fk_hist_user` (`utilisateur_id`),
  KEY `ix_historique_date` (`date_action`),
  CONSTRAINT `fk_hist_user` FOREIGN KEY (`utilisateur_id`) REFERENCES `utilisateur` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historique`
--

LOCK TABLES `historique` WRITE;
/*!40000 ALTER TABLE `historique` DISABLE KEYS */;
/*!40000 ALTER TABLE `historique` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `paiement_dette`
--

DROP TABLE IF EXISTS `paiement_dette`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `paiement_dette` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dette_id` int(11) NOT NULL,
  `montant` decimal(10,2) NOT NULL,
  `date_paiement` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `ix_pay_dette` (`dette_id`),
  CONSTRAINT `fk_paiement_dette` FOREIGN KEY (`dette_id`) REFERENCES `dette` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `chk_pay_montant` CHECK (`montant` > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `paiement_dette`
--

LOCK TABLES `paiement_dette` WRITE;
/*!40000 ALTER TABLE `paiement_dette` DISABLE KEYS */;
/*!40000 ALTER TABLE `paiement_dette` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ZERO_IN_DATE,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER trg_paiement_dette_before_insert
BEFORE INSERT ON paiement_dette
FOR EACH ROW
BEGIN
  DECLARE due DECIMAL(10,2);
  DECLARE deja_paye DECIMAL(10,2);

  SELECT montant INTO due FROM dette WHERE id = NEW.dette_id FOR UPDATE;
  IF due IS NULL THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Dette inexistante';
  END IF;

  SELECT IFNULL(SUM(montant),0) INTO deja_paye
  FROM paiement_dette
  WHERE dette_id = NEW.dette_id;

  IF (deja_paye + NEW.montant) > due THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Paiement d�passe le montant de la dette';
  END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ZERO_IN_DATE,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER trg_paiement_dette_after_insert
AFTER INSERT ON paiement_dette
FOR EACH ROW
BEGIN
  DECLARE due DECIMAL(10,2);
  DECLARE total_paye DECIMAL(10,2);

  SELECT montant INTO due FROM dette WHERE id = NEW.dette_id;
  SELECT IFNULL(SUM(montant),0) INTO total_paye
  FROM paiement_dette
  WHERE dette_id = NEW.dette_id;

  IF total_paye = due THEN
    UPDATE dette SET statut = 'PAYEE' WHERE id = NEW.dette_id;
  ELSEIF total_paye > 0 AND total_paye < due THEN
    UPDATE dette SET statut = 'PARTIEL' WHERE id = NEW.dette_id;
  ELSE
    UPDATE dette SET statut = 'EN_COURS' WHERE id = NEW.dette_id;
  END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ZERO_IN_DATE,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER trg_paiement_dette_before_update
BEFORE UPDATE ON paiement_dette
FOR EACH ROW
BEGIN
  DECLARE due DECIMAL(10,2);
  DECLARE autres DECIMAL(10,2);

  SELECT montant INTO due FROM dette WHERE id = NEW.dette_id FOR UPDATE;

  SELECT IFNULL(SUM(montant),0) INTO autres
  FROM paiement_dette
  WHERE dette_id = NEW.dette_id AND id <> OLD.id;

  IF (autres + NEW.montant) > due THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Paiement (maj) d�passe le montant de la dette';
  END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ZERO_IN_DATE,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER trg_paiement_dette_after_update
AFTER UPDATE ON paiement_dette
FOR EACH ROW
BEGIN
  DECLARE due DECIMAL(10,2);
  DECLARE total_paye DECIMAL(10,2);

  SELECT montant INTO due FROM dette WHERE id = NEW.dette_id;
  SELECT IFNULL(SUM(montant),0) INTO total_paye
  FROM paiement_dette
  WHERE dette_id = NEW.dette_id;

  IF total_paye = due THEN
    UPDATE dette SET statut = 'PAYEE' WHERE id = NEW.dette_id;
  ELSEIF total_paye > 0 AND total_paye < due THEN
    UPDATE dette SET statut = 'PARTIEL' WHERE id = NEW.dette_id;
  ELSE
    UPDATE dette SET statut = 'EN_COURS' WHERE id = NEW.dette_id;
  END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ZERO_IN_DATE,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER trg_paiement_dette_after_delete
AFTER DELETE ON paiement_dette
FOR EACH ROW
BEGIN
  DECLARE due DECIMAL(10,2);
  DECLARE total_paye DECIMAL(10,2);

  SELECT montant INTO due FROM dette WHERE id = OLD.dette_id;
  SELECT IFNULL(SUM(montant),0) INTO total_paye
  FROM paiement_dette
  WHERE dette_id = OLD.dette_id;

  IF total_paye = due THEN
    UPDATE dette SET statut = 'PAYEE' WHERE id = OLD.dette_id;
  ELSEIF total_paye > 0 AND total_paye < due THEN
    UPDATE dette SET statut = 'PARTIEL' WHERE id = OLD.dette_id;
  ELSE
    UPDATE dette SET statut = 'EN_COURS' WHERE id = OLD.dette_id;
  END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `produit`
--

DROP TABLE IF EXISTS `produit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `produit` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `barcode` varchar(100) DEFAULT NULL,
  `nom` varchar(200) NOT NULL,
  `prix_achat` decimal(10,2) NOT NULL,
  `prix_vente` decimal(10,2) NOT NULL,
  `quantite` int(11) NOT NULL DEFAULT 0,
  `image_url` varchar(500) DEFAULT NULL,
  `date_ajout` datetime NOT NULL DEFAULT current_timestamp(),
  `categorie_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `barcode` (`barcode`),
  KEY `ix_produit_nom` (`nom`),
  KEY `ix_produit_categorie` (`categorie_id`),
  CONSTRAINT `fk_produit_categorie` FOREIGN KEY (`categorie_id`) REFERENCES `categorie` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `chk_prix_valides` CHECK (`prix_achat` >= 0 and `prix_vente` > `prix_achat`),
  CONSTRAINT `chk_quantite_nonneg` CHECK (`quantite` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produit`
--

LOCK TABLES `produit` WRITE;
/*!40000 ALTER TABLE `produit` DISABLE KEYS */;
/*!40000 ALTER TABLE `produit` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ZERO_IN_DATE,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER trg_produit_before_insert
BEFORE INSERT ON produit
FOR EACH ROW
BEGIN
  IF NEW.prix_achat < 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'prix_achat doit �tre >= 0';
  END IF;
  IF NEW.prix_vente <= NEW.prix_achat THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'prix_vente doit �tre > prix_achat';
  END IF;
  IF NEW.quantite < 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'quantite doit �tre >= 0';
  END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ZERO_IN_DATE,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER trg_produit_before_update
BEFORE UPDATE ON produit
FOR EACH ROW
BEGIN
  IF NEW.prix_achat < 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'prix_achat doit �tre >= 0';
  END IF;
  IF NEW.prix_vente <= NEW.prix_achat THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'prix_vente doit �tre > prix_achat';
  END IF;
  IF NEW.quantite < 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'quantite doit �tre >= 0';
  END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `utilisateur`
--

DROP TABLE IF EXISTS `utilisateur`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `utilisateur` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nom_complet` varchar(150) NOT NULL,
  `email` varchar(150) NOT NULL,
  `mot_de_passe` varchar(255) NOT NULL,
  `role` enum('ADMIN','VENDEUR') NOT NULL DEFAULT 'VENDEUR',
  `actif` tinyint(1) NOT NULL DEFAULT 1,
  `date_creation` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `utilisateur`
--

LOCK TABLES `utilisateur` WRITE;
/*!40000 ALTER TABLE `utilisateur` DISABLE KEYS */;
/*!40000 ALTER TABLE `utilisateur` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vente`
--

DROP TABLE IF EXISTS `vente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vente` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `produit_id` int(11) NOT NULL,
  `quantite` int(11) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `date_vente` datetime NOT NULL DEFAULT current_timestamp(),
  `utilisateur_id` int(11) NOT NULL,
  `user_name_snapshot` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_vente_prod_date` (`produit_id`,`date_vente`),
  KEY `ix_vente_date` (`date_vente`),
  KEY `ix_vente_user_date` (`utilisateur_id`,`date_vente`),
  CONSTRAINT `fk_vente_produit` FOREIGN KEY (`produit_id`) REFERENCES `produit` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_vente_utilisateur` FOREIGN KEY (`utilisateur_id`) REFERENCES `utilisateur` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `chk_vente_qte` CHECK (`quantite` > 0),
  CONSTRAINT `chk_vente_total` CHECK (`total` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vente`
--

LOCK TABLES `vente` WRITE;
/*!40000 ALTER TABLE `vente` DISABLE KEYS */;
/*!40000 ALTER TABLE `vente` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ZERO_IN_DATE,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER trg_vente_before_insert
BEFORE INSERT ON vente
FOR EACH ROW
BEGIN
  DECLARE stock_actuel INT;
  DECLARE pv DECIMAL(10,2);

  
  SELECT quantite, prix_vente INTO stock_actuel, pv
  FROM produit
  WHERE id = NEW.produit_id
  FOR UPDATE;

  IF stock_actuel IS NULL THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Produit inexistant';
  END IF;

  IF NEW.quantite <= 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Quantit� de vente invalide';
  END IF;

  IF NEW.quantite > stock_actuel THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Stock insuffisant';
  END IF;

  
  IF NEW.total IS NULL OR NEW.total < 0 THEN
    SET NEW.total = pv * NEW.quantite;
  END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ZERO_IN_DATE,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER trg_vente_after_insert
AFTER INSERT ON vente
FOR EACH ROW
BEGIN
  
  UPDATE produit
  SET quantite = quantite - NEW.quantite
  WHERE id = NEW.produit_id;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ZERO_IN_DATE,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER trg_vente_before_update
BEFORE UPDATE ON vente
FOR EACH ROW
BEGIN
  IF NEW.produit_id <> OLD.produit_id THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Modification du produit interdite sur une vente';
  END IF;
  IF NEW.quantite <> OLD.quantite THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Modification de la quantit� interdite sur une vente';
  END IF;
  
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ZERO_IN_DATE,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER trg_vente_after_delete
AFTER DELETE ON vente
FOR EACH ROW
BEGIN
  UPDATE produit
  SET quantite = quantite + OLD.quantite
  WHERE id = OLD.produit_id;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-09-15 20:50:02
