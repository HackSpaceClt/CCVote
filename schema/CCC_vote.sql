SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `ccvote` DEFAULT CHARACTER SET latin1 ;
USE `ccvote` ;

-- -----------------------------------------------------
-- Table `ccvote`.`groupData`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ccvote`.`groupData` ;

CREATE  TABLE IF NOT EXISTS `ccvote`.`groupData` (
  `groupID` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Unique group ID number' ,
  `groupName` TINYTEXT NOT NULL ,
  `groupMotionMaint` TINYINT(4) NOT NULL COMMENT 'Allowed to maintain motions' ,
  `groupRunReports` TINYINT(4) NOT NULL COMMENT 'Allowed to run reporting' ,
  `groupVoter` TINYINT(4) NOT NULL COMMENT 'Allowed to cast votes' ,
  `groupAdmin` TINYINT(4) NOT NULL COMMENT 'Allowed to perform admin functions' ,
  PRIMARY KEY (`groupID`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1
COMMENT = 'User permission groups';


-- -----------------------------------------------------
-- Table `ccvote`.`logData`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ccvote`.`logData` ;

CREATE  TABLE IF NOT EXISTS `ccvote`.`logData` (
  `logID` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Allows precise sequencing' ,
  `userID` BIGINT(20) NOT NULL COMMENT 'The user taking the action' ,
  `logAction` VARCHAR(20) NOT NULL COMMENT 'The type action' ,
  `details` TEXT NOT NULL COMMENT 'More information' ,
  PRIMARY KEY (`logID`) )
ENGINE = ARCHIVE
DEFAULT CHARACTER SET = latin1
COMMENT = 'insert only historical log.';


-- -----------------------------------------------------
-- Table `ccvote`.`userData`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ccvote`.`userData` ;

CREATE  TABLE IF NOT EXISTS `ccvote`.`userData` (
  `userID` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'User unique ID.' ,
  `userName` VARCHAR(20) NOT NULL COMMENT 'User Full name.' ,
  `userFullName` VARCHAR(120) NOT NULL COMMENT 'User full name' ,
  `userPwHash` VARCHAR(80) NOT NULL COMMENT 'Password hash' ,
  `userStatus` VARCHAR(10) NOT NULL COMMENT 'locked, logged_out, or logged_in' ,
  `userLastLogin` DATETIME NOT NULL COMMENT 'Date of last login' ,
  `userLastHost` VARCHAR(14) NOT NULL COMMENT 'IP of last login' ,
  `groupID` BIGINT(20) UNSIGNED NOT NULL COMMENT 'Group the user belongs to.' ,
  PRIMARY KEY (`userID`) ,
  INDEX `fk_users_groupData` (`groupID` ASC) ,
  CONSTRAINT `fk_users_groupData`
    FOREIGN KEY (`groupID` )
    REFERENCES `ccvote`.`groupData` (`groupID` ))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1
COMMENT = 'User specific data';


-- -----------------------------------------------------
-- Table `ccvote`.`motionData`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ccvote`.`motionData` ;

CREATE  TABLE IF NOT EXISTS `ccvote`.`motionData` (
  `motionID` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Unique motion id' ,
  `motionCreateTime` DATETIME NOT NULL COMMENT 'when the motion was created' ,
  `motionParent` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'parent motion (used for recalls)' ,
  `motionVoteStart` DATETIME NOT NULL COMMENT 'Voting windows open time' ,
  `motionVoteEnd` DATETIME NOT NULL COMMENT 'Voting window close time' ,
  `motionClerkID` BIGINT(20) UNSIGNED NOT NULL COMMENT 'Clerk who created the motion' ,
  `motionDescription` VARCHAR(50) NOT NULL COMMENT 'Short name or title' ,
  `motionComment` TEXT NOT NULL COMMENT 'Extended comments or notes' ,
  `motionStatus` VARCHAR(10) NOT NULL COMMENT 'new open closed withdrawn canceled' ,
  PRIMARY KEY (`motionID`) ,
  INDEX `fk_motionData_userData` (`motionClerkID` ASC) ,
  CONSTRAINT `fk_motionData_userData`
    FOREIGN KEY (`motionClerkID` )
    REFERENCES `ccvote`.`userData` (`userID` ))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1
COMMENT = 'Motion specific data';


-- -----------------------------------------------------
-- Table `ccvote`.`voteData`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ccvote`.`voteData` ;

CREATE  TABLE IF NOT EXISTS `ccvote`.`voteData` (
  `voteID` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Unique vote id and sequence' ,
  `motionID` BIGINT(20) UNSIGNED NOT NULL COMMENT 'motion this vote is on' ,
  `userID` BIGINT(20) UNSIGNED NOT NULL COMMENT 'user casting the vote' ,
  `voteTime` DATETIME NOT NULL COMMENT 'time the vote was cast' ,
  `vote` VARCHAR(10) NOT NULL COMMENT 'pro con abstain' ,
  PRIMARY KEY (`voteID`) ,
  INDEX `fk_voteData_motionData` (`motionID` ASC) ,
  INDEX `fk_voteData_userData` (`userID` ASC) ,
  CONSTRAINT `fk_voteData_motionData`
    FOREIGN KEY (`motionID` )
    REFERENCES `ccvote`.`motionData` (`motionID` ),
  CONSTRAINT `fk_voteData_userData`
    FOREIGN KEY (`userID` )
    REFERENCES `ccvote`.`userData` (`userID` ))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1
COMMENT = 'Voting record';



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
