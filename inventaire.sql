-- ========= Inventaire - Schéma propre (UTF-8) =========
-- Compatible MariaDB 10.4+ / MySQL 8+
-- Ce script reconstruit la base "inventaire" avec PK/FK/INDEX/TRIGGERS cohérents.

SET NAMES utf8mb4;
SET time_zone = '+00:00';
SET sql_notes = 0;
SET foreign_key_checks = 0;
SET unique_checks = 0;

DROP DATABASE IF EXISTS `inventaire`;
CREATE DATABASE `inventaire` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `inventaire`;

DROP TABLE IF EXISTS `categorie`;
CREATE TABLE `categorie` (
  `nom` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`nom`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- =======================
-- Table: produit
-- =======================
DROP TABLE IF EXISTS `produit`;
CREATE TABLE `produit` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `barcode` VARCHAR(100) DEFAULT NULL,
  `nom` VARCHAR(200) NOT NULL,
  `prix_achat` DECIMAL(12,2) NOT NULL,
  `prix_vente` DECIMAL(12,2) NOT NULL,
  `quantite` INT NOT NULL DEFAULT 0,
  `image_url` VARCHAR(500) DEFAULT NULL,
  `date_ajout` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `categorie_nom` VARCHAR(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_produit_barcode` (`barcode`),
  KEY `ix_produit_nom` (`nom`),
  KEY `ix_produit_categorie` (`categorie_nom`),
  CONSTRAINT `fk_produit_categorie_nom`
    FOREIGN KEY (`categorie_nom`) REFERENCES `categorie` (`nom`)
    ON UPDATE CASCADE
    ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- =======================
-- Table: utilisateur
-- =======================
DROP TABLE IF EXISTS `utilisateur`;
CREATE TABLE `utilisateur` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nom_complet` VARCHAR(150) NOT NULL,
  `email` VARCHAR(150) NOT NULL,
  `mot_de_passe` VARCHAR(255) NOT NULL,
  `role` ENUM('ADMIN','VENDEUR') NOT NULL DEFAULT 'VENDEUR',
  `actif` TINYINT(1) NOT NULL DEFAULT 1,
  `date_creation` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_utilisateur_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- =======================
-- Table: alerte
-- =======================
DROP TABLE IF EXISTS `alerte`;
CREATE TABLE `alerte` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `type` ENUM('REAPPRO','INFO') NOT NULL,
  `produit_id` INT DEFAULT NULL,
  `niveau` ENUM('INFO','WARN','CRIT') NOT NULL DEFAULT 'INFO',
  `message` TEXT NOT NULL,
  `resolue` TINYINT(1) NOT NULL DEFAULT 0,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `ix_alerte_prod_date` (`produit_id`, `created_at`),
  CONSTRAINT `fk_alerte_produit`
    FOREIGN KEY (`produit_id`) REFERENCES `produit` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- =======================
-- Table: dette
-- =======================
DROP TABLE IF EXISTS `dette`;
CREATE TABLE `dette` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nom_client` VARCHAR(150) NOT NULL,
  `telephone` VARCHAR(50) DEFAULT NULL,
  `montant` DECIMAL(10,2) NOT NULL,
  `date_dette` DATE NOT NULL,
  `produits_txt` TEXT DEFAULT NULL,
  `remarques` TEXT DEFAULT NULL,
  `statut` ENUM('EN_COURS','PARTIEL','PAYEE') NOT NULL DEFAULT 'EN_COURS',
  PRIMARY KEY (`id`),
  KEY `ix_dette_statut_date` (`statut`, `date_dette`),
  KEY `ix_dette_date` (`date_dette`),
  CONSTRAINT `chk_dette_montant` CHECK (`montant` > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- =======================
-- Table: paiement_dette
-- =======================
DROP TABLE IF EXISTS `paiement_dette`;
CREATE TABLE `paiement_dette` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `dette_id` INT NOT NULL,
  `montant` DECIMAL(10,2) NOT NULL,
  `date_paiement` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `ix_pay_dette` (`dette_id`),
  CONSTRAINT `fk_paiement_dette`
    FOREIGN KEY (`dette_id`) REFERENCES `dette` (`id`)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `chk_pay_montant` CHECK (`montant` > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- =======================
-- Table: vente
-- =======================
DROP TABLE IF EXISTS `vente`;
CREATE TABLE `vente` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `produit_id` INT NOT NULL,
  `quantite` INT NOT NULL,
  `total` DECIMAL(10,2) NOT NULL,
  `date_vente` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `utilisateur_id` INT NOT NULL,
  `user_name_snapshot` VARCHAR(150) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_vente_prod_date` (`produit_id`, `date_vente`),
  KEY `ix_vente_date` (`date_vente`),
  KEY `ix_vente_user_date` (`utilisateur_id`, `date_vente`),
  CONSTRAINT `fk_vente_produit`
    FOREIGN KEY (`produit_id`) REFERENCES `produit` (`id`)
    ON UPDATE CASCADE,
  CONSTRAINT `fk_vente_utilisateur`
    FOREIGN KEY (`utilisateur_id`) REFERENCES `utilisateur` (`id`)
    ON UPDATE CASCADE,
  CONSTRAINT `chk_vente_qte` CHECK (`quantite` > 0),
  CONSTRAINT `chk_vente_total` CHECK (`total` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

SET foreign_key_checks = 1;
SET unique_checks = 1;

-- =======================
-- Triggers (UTF-8, accents corrigés)
-- =======================

DELIMITER //

-- Paiement_dette : before insert
CREATE TRIGGER trg_paiement_dette_before_insert
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
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Paiement dépasse le montant de la dette';
  END IF;
END//

-- Paiement_dette : after insert
CREATE TRIGGER trg_paiement_dette_after_insert
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
END//

-- Paiement_dette : before update
CREATE TRIGGER trg_paiement_dette_before_update
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
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Paiement (mise à jour) dépasse le montant de la dette';
  END IF;
END//

-- Paiement_dette : after update
CREATE TRIGGER trg_paiement_dette_after_update
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
END//

-- Paiement_dette : after delete
CREATE TRIGGER trg_paiement_dette_after_delete
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
END//

-- Produit : before insert
CREATE TRIGGER trg_produit_before_insert
BEFORE INSERT ON produit
FOR EACH ROW
BEGIN
  IF NEW.prix_achat < 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'prix_achat doit être >= 0';
  END IF;
  IF NEW.prix_vente <= NEW.prix_achat THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'prix_vente doit être > prix_achat';
  END IF;
  IF NEW.quantite < 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'quantite doit être >= 0';
  END IF;
END//

-- Produit : before update
CREATE TRIGGER trg_produit_before_update
BEFORE UPDATE ON produit
FOR EACH ROW
BEGIN
  IF NEW.prix_achat < 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'prix_achat doit être >= 0';
  END IF;
  IF NEW.prix_vente <= NEW.prix_achat THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'prix_vente doit être > prix_achat';
  END IF;
  IF NEW.quantite < 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'quantite doit être >= 0';
  END IF;
END//

-- Vente : before insert
CREATE TRIGGER trg_vente_before_insert
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
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Quantité de vente invalide';
  END IF;

  IF NEW.quantite > stock_actuel THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Stock insuffisant';
  END IF;

  IF NEW.total IS NULL OR NEW.total < 0 THEN
    SET NEW.total = pv * NEW.quantite;
  END IF;
END//

-- Vente : after insert (décrément stock)
CREATE TRIGGER trg_vente_after_insert
AFTER INSERT ON vente
FOR EACH ROW
BEGIN
  UPDATE produit
  SET quantite = quantite - NEW.quantite
  WHERE id = NEW.produit_id;
END//

-- Vente : before update (verrous métier)
CREATE TRIGGER trg_vente_before_update
BEFORE UPDATE ON vente
FOR EACH ROW
BEGIN
  IF NEW.produit_id <> OLD.produit_id THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Modification du produit interdite sur une vente';
  END IF;
  IF NEW.quantite <> OLD.quantite THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Modification de la quantité interdite sur une vente';
  END IF;
END//

-- Vente : after delete (ré-incrémente stock)
CREATE TRIGGER trg_vente_after_delete
AFTER DELETE ON vente
FOR EACH ROW
BEGIN
  UPDATE produit
  SET quantite = quantite + OLD.quantite
  WHERE id = OLD.produit_id;
END//

DELIMITER ;

SET sql_notes = 1;
