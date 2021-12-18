-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 18, 2021 at 12:30 PM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 8.0.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hackathon`
--

-- --------------------------------------------------------

--
-- Table structure for table `useralerts`
--

CREATE TABLE `useralerts` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `email` varchar(50) NOT NULL,
  `url` varchar(120) NOT NULL,
  `time` datetime NOT NULL DEFAULT current_timestamp(),
  `price` int(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `useralerts`
--

INSERT INTO `useralerts` (`id`, `name`, `email`, `url`, `time`, `price`) VALUES
(5, 'Ganesh', 'Ganeshprasathagp@gmail.com', 'https://www.amazon.com/SanDisk-Cruzer-Ultra-Flash-SDCZ48-016G-U46/dp/B00NIEIRVY/ref=sr_1_10?crid=1CAP6BWZ3J8ZR&keywords=', '2021-12-18 11:39:42', 2500);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `useralerts`
--
ALTER TABLE `useralerts`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `useralerts`
--
ALTER TABLE `useralerts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
