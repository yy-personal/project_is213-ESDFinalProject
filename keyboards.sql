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
-- Database: `keyboards`
--
CREATE DATABASE IF NOT EXISTS `keyboards` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `keyboards`;

-- --------------------------------------------------------

--
-- Table structure for table `keyboards`
--

DROP TABLE IF EXISTS `keyboards`;
CREATE TABLE IF NOT EXISTS `keyboards` (
  `itemID` int(11) NOT NULL,
  `itemName` varchar(64) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `quantity` int(11) DEFAULT NULL,
  `photo_url` varchar(64) NOT NULL,
  `category` varchar(64) NOT NULL,


  PRIMARY KEY (`itemID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `keyboards`
--

INSERT INTO `keyboards` (`itemID`, `itemName`, `price`, `quantity`, `photo_url`, `category`) VALUES
('1','Razer Pro Type Ultra','159.50',13, 'img/razer_pro_type_ultra.jpg', 'keyboard'),
('2','Corsair K95 RGB Platinum XT','199.99',14, 'img/corsair_k95_gb_platinum_xt.jpg', 'keyboard'),
('3','Asus ROG Falchion Wireless Gaming Keyboard','159.99',8, 'img/asus_rog_falchion.jpg', 'keyboard'),
('4','Corsair K70 RGB TKL Champion Series Gaming Keyboard','139.99',20, 'img/corsair_k70.jpg', 'keyboard'),
('5','Fnatic Streak65 Gaming Keyboard','109.99',18, 'img/fnatic_streak65.jpg', 'keyboard'),
('6','Matias Ergo Pro Ergonomic Keyboard','220',5, 'img/matias_ergo.jpg', 'keyboard'),
('7','Kinesis TKO Gaming Keyboard','175',8, 'img/kinesis_tko.jpg', 'keyboard'),
('8','Drop ENTR Mechnical Keyboard','90',4, 'img/drop_entr.jpg', 'keyboard'),
('9','Das Keyboard 4C TKL','139',6, 'img/das_keyboard.jpg', 'keyboard'),
('10','Realforce 4 Keyboard','111',0, 'img/realforce_4.jpg', 'keyboard'),

('11','Alpaca Linear','8',10, 'img/s_alpaca_linear.jpg', 'switch'),
('12','Mauve Linear ','9.50',21, 'img/s_mauve_linear.jpg', 'switch'),
('13','Lavender Linear','8',34, 'img/s_lavender_linear.jpg', 'switch'),
('14','Lilac Linear','8',23, 'img/s_lilac_linear.jpg', 'switch'),
('15','OP Black','9.50',23, 'img/s_opblack.jpg', 'switch'),

('16','CannonCaps 407','115',43, 'img/k_407.jpg', 'keycaps'),
('17','CannonCaps Hydrangea','95',12, 'img/k_hydrangea.jpg', 'keycaps'),
('18','NicePBT Type 6','115',43, 'img/k_type6.jpg', 'keycaps'),
('19','CannonCaps City Sunset','105',53, 'img/k_city_sunset.jpg', 'keycaps'),
('20','NicePBT Retro Mizu','124',43, 'img/k_retro_mizu.jpg', 'keycaps');


COMMIT;

/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
