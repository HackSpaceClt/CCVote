-- MySQL dump 10.13  Distrib 5.1.60, for redhat-linux-gnu (x86_64)
--
-- Host: localhost    Database: CCC_vote
-- ------------------------------------------------------
-- Server version	5.1.60

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
-- Table structure for table `groupData`
--

DROP TABLE IF EXISTS `groupData`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `groupData` (
  `groupID` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'Unique group ID number',
  `groupMotionMaint` tinyint(4) NOT NULL COMMENT 'Allowed to maintain motions',
  `groupRunReports` tinyint(4) NOT NULL COMMENT 'Allowed to run reporting',
  `groupVoter` tinyint(4) NOT NULL COMMENT 'Allowed to cast votes',
  `groupAdmin` tinyint(4) NOT NULL COMMENT 'Allowed to perform admin functions',
  PRIMARY KEY (`groupID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='User permission groups';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `groupData`
--

LOCK TABLES `groupData` WRITE;
/*!40000 ALTER TABLE `groupData` DISABLE KEYS */;
/*!40000 ALTER TABLE `groupData` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logData`
--

DROP TABLE IF EXISTS `logData`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `logData` (
  `logID` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'Allows precise sequencing',
  `userID` bigint(20) unsigned NOT NULL COMMENT 'The user taking the action',
  `logAction` varchar(20) NOT NULL COMMENT 'The type action',
  `details` text NOT NULL COMMENT 'More information',
  PRIMARY KEY (`logID`),
  KEY `fk_logData_userData` (`userID`),
  CONSTRAINT `fk_logData_userData` FOREIGN KEY (`userID`) REFERENCES `userData` (`userID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='insert only historical log.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logData`
--

LOCK TABLES `logData` WRITE;
/*!40000 ALTER TABLE `logData` DISABLE KEYS */;
/*!40000 ALTER TABLE `logData` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `motionData`
--

DROP TABLE IF EXISTS `motionData`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `motionData` (
  `motionID` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'Unique motion id',
  `motionCreateTime` datetime NOT NULL COMMENT 'when the motion was created',
  `motionParent` bigint(20) unsigned NOT NULL DEFAULT '0' COMMENT 'parent motion (used for recalls)',
  `motionVoteStart` datetime NOT NULL COMMENT 'Voting windows open time',
  `motionVoteEnd` datetime NOT NULL COMMENT 'Voting window close time',
  `motionClerkID` bigint(20) unsigned NOT NULL COMMENT 'Clerk who created the motion',
  `motionDescription` varchar(50) NOT NULL COMMENT 'Short name or title',
  `motionComment` text NOT NULL COMMENT 'Extended comments or notes',
  `motionStatus` varchar(10) NOT NULL COMMENT 'new open closed withdrawn canceled',
  PRIMARY KEY (`motionID`),
  KEY `fk_motionData_userData` (`motionClerkID`),
  CONSTRAINT `fk_motionData_userData` FOREIGN KEY (`motionClerkID`) REFERENCES `userData` (`userID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Motion specific data';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `motionData`
--

LOCK TABLES `motionData` WRITE;
/*!40000 ALTER TABLE `motionData` DISABLE KEYS */;
/*!40000 ALTER TABLE `motionData` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userData`
--

DROP TABLE IF EXISTS `userData`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userData` (
  `userID` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'User unique ID.',
  `userName` varchar(20) NOT NULL COMMENT 'User Full name.',
  `userFullName` varchar(120) NOT NULL COMMENT 'User full name',
  `userPwHash` varchar(80) NOT NULL COMMENT 'Password hash',
  `userStatus` varchar(10) NOT NULL COMMENT 'locked, logged_out, or logged_in',
  `userLastLogin` datetime NOT NULL COMMENT 'Date of last login',
  `userLastHost` varchar(14) NOT NULL COMMENT 'IP of last login',
  `groupID` bigint(20) unsigned NOT NULL COMMENT 'Group the user belongs to.',
  PRIMARY KEY (`userID`),
  KEY `fk_users_groupData` (`groupID`),
  CONSTRAINT `fk_users_groupData` FOREIGN KEY (`groupID`) REFERENCES `groupData` (`groupID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='User specific data';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userData`
--

LOCK TABLES `userData` WRITE;
/*!40000 ALTER TABLE `userData` DISABLE KEYS */;
/*!40000 ALTER TABLE `userData` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `voteData`
--

DROP TABLE IF EXISTS `voteData`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `voteData` (
  `voteID` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'Unique vote id and sequence',
  `motionID` bigint(20) unsigned NOT NULL COMMENT 'motion this vote is on',
  `userID` bigint(20) unsigned NOT NULL COMMENT 'user casting the vote',
  `voteTime` datetime NOT NULL COMMENT 'time the vote was cast',
  `vote` varchar(10) NOT NULL COMMENT 'pro con abstain',
  PRIMARY KEY (`voteID`),
  KEY `fk_voteData_motionData` (`motionID`),
  KEY `fk_voteData_userData` (`userID`),
  CONSTRAINT `fk_voteData_motionData` FOREIGN KEY (`motionID`) REFERENCES `motionData` (`motionID`),
  CONSTRAINT `fk_voteData_userData` FOREIGN KEY (`userID`) REFERENCES `userData` (`userID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Voting record';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `voteData`
--

LOCK TABLES `voteData` WRITE;
/*!40000 ALTER TABLE `voteData` DISABLE KEYS */;
/*!40000 ALTER TABLE `voteData` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-09-15 11:23:33
