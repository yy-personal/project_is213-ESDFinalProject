SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Database: `shipping_record`
--
CREATE DATABASE IF NOT EXISTS `shipping_record` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `shipping_record`;

-- --------------------------------------------------------

--
-- Table structure for table `shipping_record`
--

DROP TABLE IF EXISTS `shipping_record`;
CREATE TABLE IF NOT EXISTS `shipping_record` (
  `recordID` int(11) NOT NULL AUTO_INCREMENT,
  `customerID` varchar(64) NOT NULL,
  `address` varchar(255) NOT NULL, -- just wondering why we need this when we have the customerID already 
  `phone` int(11) NOT NULL, -- just wondering why we need this when we have the customerID already 
  `orderID` int(11) NOT NULL, -- feel like this should be here to link to the particular order the shipping record is related to, order MS should have code to create a record here with the orderID?
  `reqStatus` varchar(64) NOT NULL,

  PRIMARY KEY (`recordID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `shipping_record`
--

INSERT INTO `shipping_record` (`recordID`, `customerID`, `address`, `phone`, `orderID`, `reqStatus`) VALUES
('1', '10001', 'Blk 453 Ang Mo Kio Ave 10 #01-1801', '65520467', '1', 'completed'),
('2', '10002', '20 Maxwell Road 05-06 Maxwell House', '62248041', '2', 'completed'),
('3', '10003', '32 Defu Lane 10 #04-18', '62855767', '3', 'accepted'),
('4', '10004', '5 Lor Bakar Batu #04-02 MacPherson Ind Complex', '97587087', '4', 'failed'),
('5', '10005', 'Bukit Batok 233 Bukit Batok East Avenue 5 #01-51', '63240832', '5', 'unaccepted'),
('6', '10006', '269 Queen St #02-240', '63397738', '6', 'unaccepted'),
('7', '10007', 'Blk 3004 Ubi Ave 3 #03-112', '67433538', '7', 'unaccepted'),
('8', '10008', '108 Rivervale Walk #09-106', '67864746', '8', 'unaccepted'),
('9', '10009', '190 Ang Mo Kio Avenue 8 #01-02', '64513175', '9', 'unaccepted');
COMMIT;

