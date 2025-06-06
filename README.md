# 🌳 Proyecto1ParcialWeb - Sistema de Registro Forestal

## 📋 Estructura del Proyecto

- **📝 `indicaciones.md`**: Requerimientos del profesor
- **📊 `planning.md`**: Flujo del sistema (**NO TOCAR**)
- **✅ `TASKS.md`**: Tareas puntuales que se deben realizar (**NO TOCAR**)
- **🔧 `DeveloperTasks`**: Nuestras tareas (Si se puede modificar)

Este README sirve como repositorio de códigos, explicaciones, links, scripts, SQLs, tareas a realizar, etc. que se están o se van a usar en el Proyecto.

## 🗄️ Base de Datos

### 📄 Script SQL Completo

```sql
CREATE DATABASE IF NOT EXISTS sistemaforestalfinal;
USE sistemaforestalfinal;

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

-- Tabla: conservation_activities
CREATE TABLE `conservation_activities` (
  `id` int(11) NOT NULL,
  `nombre_actividad` varchar(150) NOT NULL,
  `fecha_actividad` date NOT NULL,
  `responsable` varchar(100) DEFAULT NULL,
  `tipo_actividad_id` int(11) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `zona_id` int(11) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  `creado_en` timestamp NOT NULL DEFAULT current_timestamp(),
  `actualizado_en` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: estado_conservacion
CREATE TABLE `estado_conservacion` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  `creado_en` timestamp NOT NULL DEFAULT current_timestamp(),
  `actualizado_en` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Datos iniciales: estado_conservacion
INSERT INTO `estado_conservacion` (`id`, `nombre`, `descripcion`, `activo`, `creado_en`, `actualizado_en`) VALUES
(1, 'Extinto', 'La especie ya no existe', 1, '2025-05-24 01:37:44', '2025-05-24 01:37:44'),
(2, 'En Peligro Crítico', 'Muy alta probabilidad de extinción', 1, '2025-05-24 01:37:44', '2025-05-24 01:37:44'),
(3, 'En Peligro', 'Alto riesgo de extinción', 1, '2025-05-24 01:37:44', '2025-05-24 01:37:44'),
(4, 'Vulnerable', 'Riesgo significativo', 1, '2025-05-24 01:37:44', '2025-05-24 01:37:44'),
(5, 'Preocupación Menor', 'Bajo riesgo', 1, '2025-05-24 01:37:44', '2025-05-24 01:37:44'),
(6, 'No Evaluado', 'No ha sido evaluada', 1, '2025-05-24 01:37:44', '2025-05-24 01:37:44');

-- Tabla: tipo_actividad
CREATE TABLE `tipo_actividad` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  `creado_en` timestamp NOT NULL DEFAULT current_timestamp(),
  `actualizado_en` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Datos iniciales: tipo_actividad
INSERT INTO `tipo_actividad` (`id`, `nombre`, `descripcion`, `activo`, `creado_en`, `actualizado_en`) VALUES
(1, 'Reforestación', 'Plantación de árboles', 1, '2025-05-24 01:37:44', '2025-05-24 01:37:44'),
(2, 'Monitoreo', 'Supervisión y control', 1, '2025-05-24 01:37:44', '2025-05-24 01:37:44'),
(3, 'Educación', 'Actividades educativas', 1, '2025-05-24 01:37:44', '2025-05-24 01:37:44'),
(4, 'Limpieza', 'Mantenimiento y limpieza de la zona', 1, '2025-05-24 01:37:44', '2025-05-24 01:37:44');

-- Tabla: tree_species
CREATE TABLE `tree_species` (
  `id` int(11) NOT NULL,
  `nombre_comun` varchar(100) NOT NULL,
  `nombre_cientifico` varchar(150) DEFAULT NULL,
  `estado_conservacion_id` int(11) DEFAULT NULL,
  `zona_id` int(11) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  `creado_en` timestamp NOT NULL DEFAULT current_timestamp(),
  `actualizado_en` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: usuarios
CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `nombre_completo` varchar(100) NOT NULL,
  `rol` enum('admin','usuario','invitado') DEFAULT 'usuario',
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  `creado_en` timestamp NOT NULL DEFAULT current_timestamp(),
  `actualizado_en` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Datos iniciales: usuarios
INSERT INTO `usuarios` (`id`, `username`, `password`, `email`, `nombre_completo`, `rol`, `activo`, `creado_en`, `actualizado_en`) VALUES
(1, 'admin01', 'e4abae53cc1cebe5fe89ea93882c699a5e71ab0bbf42a83b7d833975b61c4a41', 'admin01@sistemaforestal.org', 'Administrador Principal', 'admin', 1, '2025-05-24 02:03:50', '2025-05-24 02:03:50'),
(2, 'usuario01', '0b60014e9138da6ffaeb93f3260537f8fa7e6e970c2bc9302f7da288d3dddc06', 'usuario01@sistemaforestal.org', 'Carlos López', 'usuario', 1, '2025-05-24 02:03:50', '2025-05-24 02:03:50'),
(3, 'usuario02', '199780e38e1000f34581b6c352f6f15c579a09e2d6cc4914800b0378d244d391', 'usuario02@sistemaforestal.org', 'María González', 'usuario', 1, '2025-05-24 02:03:50', '2025-05-24 02:03:50'),
(4, 'invitado01', '4134ad2e373d48695884803fa4de88ce81799c72ce62ef418639f986434c3228', 'invitado01@sistemaforestal.org', 'Invitado Pérez', 'invitado', 1, '2025-05-24 02:03:50', '2025-05-24 02:03:50');

-- Tabla: zones
CREATE TABLE `zones` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `tipo_bosque` varchar(100) DEFAULT NULL,
  `area_ha` decimal(10,2) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  `creado_en` timestamp NOT NULL DEFAULT current_timestamp(),
  `actualizado_en` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Configuración de claves primarias e índices
ALTER TABLE `conservation_activities`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_tipo_actividad_id` (`tipo_actividad_id`),
  ADD KEY `idx_zona_id_actividad` (`zona_id`);

ALTER TABLE `estado_conservacion`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

ALTER TABLE `tipo_actividad`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

ALTER TABLE `tree_species`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_zona_id` (`zona_id`),
  ADD KEY `idx_estado_conservacion_id` (`estado_conservacion_id`);

ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

ALTER TABLE `zones`
  ADD PRIMARY KEY (`id`);

-- Auto-incremento
ALTER TABLE `conservation_activities` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `estado_conservacion` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
ALTER TABLE `tipo_actividad` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
ALTER TABLE `tree_species` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `usuarios` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
ALTER TABLE `zones` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

COMMIT;
```

## 🔐 Credenciales de Acceso

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| `admin01` | `adminpass123` | admin |
| `usuario01` | `userpass123` | usuario |
| `usuario02` | `userpass456` | usuario |
| `invitado01` | `guestpass789` | invitado |

## 📊 Estructura de Tablas

### 👥 Usuarios
- **Roles**: admin, usuario, invitado
- **Campos**: id, username, password (hash), email, nombre_completo, rol

### 🌲 Especies de Árboles (tree_species)
- **Campos**: id, nombre_comun, nombre_cientifico, estado_conservacion_id, zona_id

### 🛡️ Estado de Conservación
- **Estados**: Extinto, En Peligro Crítico, En Peligro, Vulnerable, Preocupación Menor, No Evaluado

### 🎯 Actividades de Conservación
- **Tipos**: Reforestación, Monitoreo, Educación, Limpieza
- **Campos**: nombre_actividad, fecha_actividad, responsable, tipo_actividad_id, zona_id

### 🗺️ Zonas
- **Campos**: id, nombre, tipo_bosque, area_ha