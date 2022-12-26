SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

/* Database: 'order' */
CREATE DATABASE IF NOT EXISTS `order` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `order`;


/*Table structure for 'ORDER' */

DROP TABLE IF EXISTS `order_item`;

DROP TABLE IF EXISTS `order`;
CREATE TABLE IF NOT EXISTS `order` (
    `order_id` int(11) NOT NULL AUTO_INCREMENT,
    `customer_id` int(10) NOT NULL,
    `phone` int(10) NOT NULL ,
    `address` varchar(100) NOT NULL ,
    `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `status` varchar(10) NOT NULL DEFAULT 'CART',
    `fulfill_status` varchar(12) NOT NULL DEFAULT 'UNFULFILLED',
    PRIMARY KEY (`order_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

/*Insert data into 'ORDER'*/
INSERT INTO `order` (`order_id`, `customer_id`,`phone`, `address`,  `created` ,`status` , `fulfill_status`) VALUES
(1, '1001', 92345578 , '789 Yishun Ring Rd #01-34' , '2022-03-22 02:14:55', 'NEW' , 'UNFULFILLED'),
(2, '1002', 92345794 , '100 Hundred Rd #10-00' , '2022-10-36 10:20:30', 'NEW' , 'UNFULFILLED'),
(3, '1003', 92123322 , '12, Teh Road, Singapore 101010' , '2022-04-01 11:20:13', 'NEW','UNFULFILLED');



/*Table structure for 'ORDER_ITEM' */
CREATE TABLE IF NOT EXISTS `order_item` (
    `item_id` int(11) NOT NULL ,
    `order_id` int(11) NOT NULL,
    `item_name` varchar(100) NOT NULL,
    `quantity` int(11) NOT NULL,
    `price` decimal(10,2) NOT NULL,
    `refund_status` varchar(10) NOT NULL DEFAULT 'NIL',
    `photo_url` varchar(64) NOT NULL,
    PRIMARY KEY (`item_id`),
    KEY `FK_order_id` (`order_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

/*Insert values into 'ORDER_ITEM'*/
INSERT INTO `order_item` (`item_id`, `order_id`, `item_name`, `quantity`, `price`, `photo_url`) VALUES
(5, 1, 'Fnatic Streak65 Gaming Keyboard', 1, '109.99', 'img/fnatic_streak65.jpg'),
(2, 1, 'Corsair K95 RGB Platinum XT', 1, '199.99', 'img/corsair_k70.jpg'),
(9, 2, 'Das Keyboard 4C TKL', 2, '139', 'img/das_keyboard.jpg'),
(7, 3,'Kinesis TKO Gaming Keyboard', 1, '175', 'img/kinesis_tko.jpg'),
(1, 2, 'Razer Pro Type Ultra', 1, '159.50', 'img/razer_pro_type_ultra.jpg');

ALTER TABLE `order_item`
  ADD CONSTRAINT `FK_order_id` FOREIGN KEY (`order_id`) REFERENCES `order` (`order_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;