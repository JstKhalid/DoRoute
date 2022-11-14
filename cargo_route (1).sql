-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 14, 2022 at 06:57 AM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cargo_route`
--

-- --------------------------------------------------------

--
-- Table structure for table `city`
--

CREATE TABLE `city` (
  `city_id` int(11) NOT NULL,
  `city_name` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `city`
--

INSERT INTO `city` (`city_id`, `city_name`) VALUES
(1, 'Jakarta'),
(2, 'Bandung'),
(3, 'Yogyakarta'),
(4, 'Semarang'),
(5, 'Solo'),
(6, 'Surabaya'),
(7, 'Malang'),
(8, 'Denpasar'),
(9, 'Banjarmasin'),
(10, 'Palangkaraya'),
(11, 'Balikpapan'),
(12, 'Tarakan'),
(13, 'Palu'),
(14, 'Makassar'),
(15, 'Kendari'),
(16, 'Gorontalo'),
(17, 'Manado'),
(18, 'Ambon'),
(19, 'Ternate'),
(20, 'Pontianak');

-- --------------------------------------------------------

--
-- Table structure for table `sample`
--

CREATE TABLE `sample` (
  `sample_id` int(11) NOT NULL,
  `origin` int(11) NOT NULL,
  `destination` int(11) NOT NULL,
  `distance` int(25) NOT NULL,
  `price` int(11) NOT NULL,
  `rate` float NOT NULL,
  `duration` int(11) NOT NULL,
  `airline` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `sample`
--

INSERT INTO `sample` (`sample_id`, `origin`, `destination`, `distance`, `price`, `rate`, `duration`, `airline`) VALUES
(1, 1, 3, 430, 13000, 3.5, 2, ''),
(2, 1, 5, 537, 15500, 4, 3, ''),
(3, 1, 4, 407, 12500, 4, 2, ''),
(4, 1, 10, 909, 19000, 4, 7, ''),
(5, 1, 11, 1259, 20250, 4, 10, ''),
(6, 1, 9, 917, 19250, 4.5, 7, ''),
(7, 1, 14, 1397, 21000, 4.5, 11, ''),
(8, 1, 7, 671, 16500, 4, 4, ''),
(9, 1, 6, 808, 18250, 4.5, 6, ''),
(10, 3, 11, 1025, 19750, 4.5, 8, ''),
(11, 4, 6, 257, 10000, 3.5, 1, ''),
(12, 6, 2, 776, 18000, 4.5, 5, ''),
(13, 6, 8, 303, 11500, 3, 1, ''),
(14, 6, 14, 791, 18000, 4, 5, ''),
(15, 6, 17, 1674, 22000, 5, 12, ''),
(16, 6, 9, 484, 14000, 3.5, 2, ''),
(17, 9, 11, 339, 12000, 3, 1, ''),
(18, 11, 12, 517, 15000, 3.5, 3, ''),
(19, 11, 13, 463, 13500, 4, 2, ''),
(20, 11, 14, 515, 15000, 4, 3, ''),
(21, 13, 14, 463, 13500, 3, 2, ''),
(22, 14, 18, 959, 19500, 4, 7, ''),
(23, 14, 15, 439, 13250, 3.5, 2, ''),
(24, 14, 16, 735, 17250, 4.5, 5, ''),
(25, 14, 17, 1233, 20000, 5, 9, '');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `city`
--
ALTER TABLE `city`
  ADD PRIMARY KEY (`city_id`);

--
-- Indexes for table `sample`
--
ALTER TABLE `sample`
  ADD PRIMARY KEY (`sample_id`),
  ADD KEY `city origin` (`origin`),
  ADD KEY `city destination` (`destination`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `city`
--
ALTER TABLE `city`
  MODIFY `city_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `sample`
--
ALTER TABLE `sample`
  MODIFY `sample_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `sample`
--
ALTER TABLE `sample`
  ADD CONSTRAINT `sample_ibfk_1` FOREIGN KEY (`origin`) REFERENCES `city` (`city_id`),
  ADD CONSTRAINT `sample_ibfk_2` FOREIGN KEY (`destination`) REFERENCES `city` (`city_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
