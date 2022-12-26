-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jan 14, 2019 at 06:42 AM
-- Server version: 5.7.19
-- PHP Version: 7.1.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `book`
--
CREATE DATABASE IF NOT EXISTS `ESDProject_accounts` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `ESDProject_accounts`;

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `accounts`;
CREATE TABLE IF NOT EXISTS `accounts` (
  `customer_id` char(8) NOT NULL,
  `name` varchar(64) NOT NULL,
  `email` varchar(64) NOT NULL,
  `address` varchar(100) NOT NULL,
  `phone_number` char(8) NOT NULL,
  `points` int NOT NULL,
  

  PRIMARY KEY (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `book`
--

INSERT INTO `accounts` (`customer_id`, `name`, `email`, `address`, `phone_number`, `points`) VALUES
('10001', 'Kenny Teh', 'kennyteh@supermail.com', '12, Teh Road, Singapore 101010', 92123322, 200),
('10002', 'John', 'john@supermail.com', '122, Jon Road, Singapore 123089', 92122213, 400),
('10003', 'Mee Lok', 'mee@supermail.com', '300, Mee Road, Singapore 303030', 92568974, 50),
('10004', 'Janey', 'janey@supermail.com', '95, Kopi Lane, Singapore 202020', 92129988, 0);

COMMIT;


