-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 16, 2021 at 10:54 AM
-- Server version: 10.4.10-MariaDB
-- PHP Version: 7.3.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `vblogs`
--

-- --------------------------------------------------------

--
-- Table structure for table `vblog_post`
--

CREATE TABLE `vblog_post` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `body` longtext NOT NULL,
  `author_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vblog_post`
--

INSERT INTO `vblog_post` (`id`, `title`, `body`, `author_id`) VALUES
(1, 'Post One', 'This is my first blog edited', 1),
(2, 'second post', 'this is second post', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `vblog_post`
--
ALTER TABLE `vblog_post`
  ADD PRIMARY KEY (`id`),
  ADD KEY `VBlog_post_author_id_51b61dde_fk_auth_user_id` (`author_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `vblog_post`
--
ALTER TABLE `vblog_post`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `vblog_post`
--
ALTER TABLE `vblog_post`
  ADD CONSTRAINT `VBlog_post_author_id_51b61dde_fk_auth_user_id` FOREIGN KEY (`author_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
