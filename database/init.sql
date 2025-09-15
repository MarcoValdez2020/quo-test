-- Script de inicialización de PostgreSQL para la API de Quo Test

-- Habilitar la extensión para generar UUIDs
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Creación de la tabla users
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- ID único generado automáticamente
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    fecha_registro TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Creación de índices para optimizar consultas
-- Crear índice único en email para mejorar el rendimiento
CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Crear índice en fecha_registro para consultas por fecha
CREATE INDEX IF NOT EXISTS idx_users_fecha_registro ON users(fecha_registro);

-- Insertar datos fake para pruebas
INSERT INTO users (nombre, email, fecha_registro) VALUES
('Juan Pérez', 'juan.perez@gmail.com', CURRENT_TIMESTAMP - INTERVAL '1 day'),
('María García', 'maria.garcia@hotmail.com', CURRENT_TIMESTAMP - INTERVAL '2 days'),
('Carlos López', 'carlos.lopez@yahoo.com', CURRENT_TIMESTAMP - INTERVAL '3 days'),
('Ana Martínez', 'ana.martinez@gmail.com', CURRENT_TIMESTAMP - INTERVAL '4 days'),
('Pedro Rodríguez', 'pedro.rodriguez@outlook.com', CURRENT_TIMESTAMP - INTERVAL '5 days'),
('Laura Sánchez', 'laura.sanchez@gmail.com', CURRENT_TIMESTAMP - INTERVAL '6 days'),
('Miguel González', 'miguel.gonzalez@hotmail.com', CURRENT_TIMESTAMP - INTERVAL '7 days'),
('Sofía Hernández', 'sofia.hernandez@yahoo.com', CURRENT_TIMESTAMP - INTERVAL '8 days'),
('Jorge Díaz', 'jorge.diaz@gmail.com', CURRENT_TIMESTAMP - INTERVAL '9 days'),
('Elena Moreno', 'elena.moreno@outlook.com', CURRENT_TIMESTAMP - INTERVAL '10 days'),
('David Ruiz', 'david.ruiz@gmail.com', CURRENT_TIMESTAMP - INTERVAL '15 days'),
('Carmen Torres', 'carmen.torres@hotmail.com', CURRENT_TIMESTAMP - INTERVAL '20 days'),
('Francisco Navarro', 'francisco.navarro@yahoo.com', CURRENT_TIMESTAMP - INTERVAL '25 days'),
('Isabel Molina', 'isabel.molina@gmail.com', CURRENT_TIMESTAMP - INTERVAL '30 days'),
('Alejandro Romero', 'alejandro.romero@outlook.com', CURRENT_TIMESTAMP - INTERVAL '35 days');


-- Creación de vistas para consultas solicitadas:

-- 1. Vista para obtener todos los usuarios registrados en los últimos 7 días
CREATE OR REPLACE VIEW usuarios_ultimos_7_dias AS
SELECT * FROM users
WHERE fecha_registro >= CURRENT_TIMESTAMP - INTERVAL '7 days';

-- 2. Vista para obtener cuantos usuarios hay por dominio de email
CREATE OR REPLACE VIEW usuarios_por_dominio AS
SELECT 
    split_part(email, '@', 2) AS dominio,
    COUNT(*) AS total_usuarios
FROM usuarios
GROUP BY dominio
ORDER BY total_usuarios DESC;