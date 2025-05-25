<%@ include file="menu.jsp" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Conservación Forestal</title>
    <link rel="stylesheet" href="css/index.css">
    <script src="https://kit.fontawesome.com/a076d05399.js" crossorigin="anonymous"></script>
</head>
<body>

<section class="hero-section">
    <h1>Conservación Forestal: Protegiendo el Futuro</h1>
    <p>Nuestro compromiso es preservar y restaurar los ecosistemas forestales para las generaciones futuras.</p>
</section>

<main class="container">
    <section id="importancia">
        <h2>¿Por qué son importantes los bosques?</h2>
        <div class="beneficios">
            <div class="beneficio">
                <div class="icon-placeholder">
                    <i class="fas fa-wind"></i>
                </div>
                <h3>Producción de Oxígeno</h3>
                <p>Los bosques son los pulmones del planeta, generando oxígeno vital para todos los seres vivos en la Tierra.</p>
            </div>
            <div class="beneficio">
                <div class="icon-placeholder">
                    <i class="fas fa-leaf"></i>
                </div>
                <h3>Biodiversidad</h3>
                <p>Hogar de millones de especies de plantas y animales, preservando el delicado equilibrio de nuestros ecosistemas.</p>
            </div>
            <div class="beneficio">
                <div class="icon-placeholder">
                    <i class="fas fa-cloud-rain"></i>
                </div>
                <h3>Regulación Climática</h3>
                <p>Ayudan a mitigar el cambio climático capturando carbono y regulando los ciclos hídricos globales.</p>
            </div>
        </div>
    </section>

    <section id="proyectos">
        <h2>Nuestros Proyectos de Conservación</h2>
        <div class="proyectos-grid">
            <div class="proyecto">
                <div class="image-placeholder"></div>
                <div class="proyecto-contenido">
                    <h3>Reforestación Comunitaria</h3>
                    <p>Trabajamos con comunidades locales para plantar y cuidar nuevos bosques, restaurando áreas degradadas y promoviendo la sostenibilidad.</p>
                </div>
            </div>
            <div class="proyecto">
                <div class="image-placeholder"></div>
                <div class="proyecto-contenido">
                    <h3>Protección de Especies</h3>
                    <p>Programas para proteger especies en peligro de extinción y conservar la rica biodiversidad de los ecosistemas forestales del Ecuador.</p>
                </div>
            </div>
        </div>
    </section>

    <section id="educacion">
        <h2>Educación Ambiental</h2>
        <p>Ofrecemos talleres, charlas y programas para concientizar sobre la importancia de los bosques y promover prácticas sostenibles en comunidades y escuelas.</p>
        <button class="cta-button">Únete a Nuestros Talleres</button>
    </section>

    <section id="contacto">
        <h2>Contáctanos</h2>
        <form>
            <input type="text" placeholder="Nombre" required>
            <input type="email" placeholder="Correo Electrónico" required>
            <textarea placeholder="Tu Mensaje" required></textarea>
            <button type="submit" class="submit-button">Enviar Mensaje</button>
        </form>
    </section>
</main>

<footer>
    <p>&copy; 2025 Conservación Forestal. Todos los derechos reservados.</p>
    <div class="redes-sociales">
        <a href="#" class="social-icon"><i class="fab fa-facebook-f"></i></a>
        <a href="#" class="social-icon"><i class="fab fa-twitter"></i></a>
        <a href="#" class="social-icon"><i class="fab fa-instagram"></i></a>
    </div>
</footer>

</body>
</html>
