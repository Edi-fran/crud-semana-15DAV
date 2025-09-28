-- Script para crear base de datos y tabla principal
CREATE DATABASE IF NOT EXISTS desarrollo_web CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE desarrollo_web;

CREATE TABLE IF NOT EXISTS productos (
  id_producto INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(120) NOT NULL,
  precio DECIMAL(10,2) NOT NULL CHECK (precio >= 0),
  stock INT NOT NULL CHECK (stock >= 0),
  creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Datos de ejemplo
INSERT INTO productos (nombre, precio, stock) VALUES
('Teclado mecánico', 59.90, 10),
('Mouse inalámbrico', 24.50, 35),
('Monitor 24 pulgadas', 179.00, 7);