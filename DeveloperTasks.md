# 🔧 Developer Tasks

## 👨‍💻 ALEXANDER
- [ ] Tarea pendiente 1
- [ ] Tarea pendiente 2
- [ ] Tarea pendiente 3

---

## 👨‍💻 ANTONIO
- [ ] Tarea pendiente 1
- [ ] Tarea pendiente 2
- [ ] Tarea pendiente 3

---

## 👨‍💻 GABRIEL

### 🌐 Servicios SOAP Implementados

```php
<?php
ini_set("soap.wsdl_cache_enabled", "0");

function connectDB() {
    $host = "localhost";
    $db = "sistemaforestalfinal";
    $user = "root";
    $pass = "";
    try {
        return new PDO("mysql:host=$host;dbname=$db;charset=utf8mb4", $user, $pass, [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION
        ]);
    } catch (PDOException $e) {
        die("Error conexión DB: " . $e->getMessage());
    }
}

// Servicio 1: Zonas con sus especies
function getZonesWithSpecies() {
    $db = connectDB();
    $stmt = $db->query("
        SELECT z.nombre AS zona, ts.nombre_comun, ts.nombre_cientifico
        FROM zones z
        LEFT JOIN tree_species ts ON ts.zona_id = z.id
        ORDER BY z.nombre, ts.nombre_comun
    ");
    $result = [];
    while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
        $zona = $row['zona'];
        if (!isset($result[$zona])) {
            $result[$zona] = [];
        }
        if ($row['nombre_comun']) {
            $result[$zona][] = [
                'nombre_comun' => $row['nombre_comun'],
                'nombre_cientifico' => $row['nombre_cientifico']
            ];
        }
    }
    return $result;
}

// Servicio 2: Registrar usuario
function registerUser($data) {
    $db = connectDB();

    // Validar duplicados
    $stmt = $db->prepare("SELECT COUNT(*) FROM usuarios WHERE username = ? OR email = ?");
    $stmt->execute([$data['username'], $data['email']]);
    if ($stmt->fetchColumn() > 0) {
        return "Error: El usuario o email ya existe.";
    }

    $password_hash = hash('sha256', $data['password']);
    $insert = $db->prepare("INSERT INTO usuarios (username, password, email, nombre_completo, rol) VALUES (?, ?, ?, ?, ?)");
    $insert->execute([
        $data['username'],
        $password_hash,
        $data['email'],
        $data['nombre_completo'],
        $data['rol'] ?? 'usuario'
    ]);

    return "Usuario registrado exitosamente.";
}
?>
```
---

## 👨‍💻 PABLO
- [ ] Tarea pendiente 1
- [ ] Tarea pendiente 2
- [ ] Tarea pendiente 3


