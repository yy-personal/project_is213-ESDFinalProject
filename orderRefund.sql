SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Database: `orderRefund`
--
CREATE DATABASE IF NOT EXISTS `orderRefund` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `orderRefund`;

-- --------------------------------------------------------

--
-- Table structure for table `orderRefund`
--

DROP TABLE IF EXISTS `orderRefund`;
CREATE TABLE IF NOT EXISTS `orderRefund` (
  `refundID` int(11) NOT NULL AUTO_INCREMENT,
  `customerID` varchar(64) NOT NULL,
  `address` varchar(255) NOT NULL,
  `phone` int(11) NOT NULL,
  `orderID` int(11) NOT NULL,
  `itemID` int(11) NOT NULL,
  `reqStatus` varchar(64) NOT NULL,

  PRIMARY KEY (`refundID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `orderRefund`
--

INSERT INTO `orderRefund` (`refundID`, `customerID`, `address`, `phone`, `orderID`, `itemID`, `reqStatus`) VALUES
('1', '10001', '12, Teh Road, Singapore 101010', 92123322, '1', '1', 'completed'),
('2', '10002', '122, Jon Road, Singapore 123089', 92122213, '2', '5', 'completed'),
('3', '10003', '300, Mee Road, Singapore 303030', 92568974, '3', '9', 'completed'),
('4', '10004', '95, Kopi Lane, Singapore 202020', 92129988, '3', '10', 'failed');
COMMIT;

