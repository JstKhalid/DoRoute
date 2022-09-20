-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 20, 2022 at 04:43 AM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 7.4.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bobt`
--

-- --------------------------------------------------------

--
-- Table structure for table `hitung_bobot`
--

CREATE TABLE `hitung_bobot` (
  `id_rute` int(11) NOT NULL,
  `asal` varchar(200) NOT NULL,
  `tujuan` varchar(200) NOT NULL,
  `harga` int(11) NOT NULL,
  `jarak` int(11) NOT NULL,
  `rating` int(11) NOT NULL,
  `durasi` int(11) NOT NULL,
  `agensi` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `hitung_bobot`
--

INSERT INTO `hitung_bobot` (`id_rute`, `asal`, `tujuan`, `harga`, `jarak`, `rating`, `durasi`, `agensi`) VALUES
(1, 'jakarta', 'pontianak', 18982, 800, 4, 12, 'Citilink'),
(3, 'jakarta', 'yogya', 11485, 570, 4, 12, 'Citilink'),
(4, 'jakarta', 'surabaya', 12862, 813, 5, 12, 'Citilink'),
(5, 'surabaya', 'jakarta', 25724, 813, 4, 12, 'Citilink'),
(6, 'pontianak', 'padang', 10500, 2075, 4, 16, 'Citilink'),
(9, 'yogya', 'padang', 9500, 1829, 4, 12, 'Citilink'),
(12, 'surabaya', 'manado', 9500, 1829, 4, 12, 'Citilink');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `hitung_bobot`
--
ALTER TABLE `hitung_bobot`
  ADD PRIMARY KEY (`id_rute`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `hitung_bobot`
--
ALTER TABLE `hitung_bobot`
  MODIFY `id_rute` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
