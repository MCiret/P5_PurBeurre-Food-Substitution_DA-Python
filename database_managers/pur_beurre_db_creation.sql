-- MySQL Script generated by MySQL Workbench
-- lun. 01 mars 2021 15:51:51 CET
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema pur_beurre_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema pur_beurre_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `pur_beurre_db` DEFAULT CHARACTER SET utf8 ;
USE `pur_beurre_db` ;

-- -----------------------------------------------------
-- Table `pur_beurre_db`.`store`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pur_beurre_db`.`store` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pur_beurre_db`.`food`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pur_beurre_db`.`food` (
  `barcode` BIGINT(15) NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  `nutri_score` CHAR(1) NOT NULL,
  `url_openfoodfacts` TEXT NOT NULL,
  `quantity` VARCHAR(15) NULL,
  `compared_to_category` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`barcode`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pur_beurre_db`.`category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pur_beurre_db`.`category` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pur_beurre_db`.`food_store`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pur_beurre_db`.`food_store` (
  `store_id` INT NOT NULL,
  `food_barcode` BIGINT(15) NOT NULL,
  PRIMARY KEY (`store_id`, `food_barcode`),
  INDEX `fk_store_food_food_idx` (`food_barcode` ASC),
  INDEX `fk_store_food_store_idx` (`store_id` ASC),
  CONSTRAINT `fk_store_food_store`
    FOREIGN KEY (`store_id`)
    REFERENCES `pur_beurre_db`.`store` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_store_food_food`
    FOREIGN KEY (`food_barcode`)
    REFERENCES `pur_beurre_db`.`food` (`barcode`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pur_beurre_db`.`food_category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pur_beurre_db`.`food_category` (
  `food_barcode` BIGINT(15) NOT NULL,
  `category_id` INT NOT NULL,
  PRIMARY KEY (`food_barcode`, `category_id`),
  INDEX `fk_food_category_category_idx` (`category_id` ASC),
  INDEX `fk_food_category_food_idx` (`food_barcode` ASC),
  CONSTRAINT `fk_food_category_food`
    FOREIGN KEY (`food_barcode`)
    REFERENCES `pur_beurre_db`.`food` (`barcode`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_food_category_category`
    FOREIGN KEY (`category_id`)
    REFERENCES `pur_beurre_db`.`category` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pur_beurre_db`.`bookmark`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pur_beurre_db`.`bookmark` (
  `food_barcode` BIGINT(15) NOT NULL,
  `substitute_barcode` BIGINT(15) NOT NULL,
  PRIMARY KEY (`food_barcode`, `substitute_barcode`),
  INDEX `fk_bookmark_food2_idx` (`substitute_barcode` ASC),
  CONSTRAINT `fk_bookmark_food1`
    FOREIGN KEY (`food_barcode`)
    REFERENCES `pur_beurre_db`.`food` (`barcode`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_bookmark_food2`
    FOREIGN KEY (`substitute_barcode`)
    REFERENCES `pur_beurre_db`.`food` (`barcode`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
