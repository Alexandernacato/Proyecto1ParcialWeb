<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8" />
    <title>Login - Conservación Forestal</title>
 
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet"/>
   
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet" />
    
    <link rel="stylesheet" href="css/login.css" />
</head>
<body>
    <div class="background-overlay"></div>
    <div class="login-container">
        <h2>Iniciar Sesión</h2>
        <% 
            String error = request.getParameter("error");
            if (error != null) {
        %>
            <div class="error-msg">Usuario o contraseña incorrectos.</div>
        <% } %>

        <form action="login" method="post" autocomplete="off">
            <div class="mb-3">
                <label for="username" class="form-label">Usuario</label>
                <input type="text" id="username" name="username" class="form-control" required autofocus>
            </div>
            <div class="mb-4">
                <label for="password" class="form-label">Contraseña</label>
                <input type="password" id="password" name="password" class="form-control" required>
            </div>
            <button type="submit" class="btn-login">Entrar</button>
        </form>
    </div>
</body>
</html>
