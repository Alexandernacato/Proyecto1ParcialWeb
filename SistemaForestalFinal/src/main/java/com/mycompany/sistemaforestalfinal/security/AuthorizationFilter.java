        package com.mycompany.sistemaforestalfinal.security;

        import com.mycompany.sistemaforestalfinal.model.Usuario;
        import jakarta.servlet.*;
        import jakarta.servlet.annotation.WebFilter;
        import jakarta.servlet.http.*;

        import java.io.IOException;

        @WebFilter("/*") // Aplica a todas las rutas
        public class AuthorizationFilter implements Filter {

            @Override
            public void init(FilterConfig filterConfig) throws ServletException {
                // Inicialización opcional
            }

            @Override
            public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
                    throws IOException, ServletException {

                HttpServletRequest req = (HttpServletRequest) request;
                HttpServletResponse resp = (HttpServletResponse) response;
                String uri = req.getRequestURI();

                HttpSession session = req.getSession(false);
                Usuario usuario = (session != null) ? (Usuario) session.getAttribute("usuario") : null;

                // Permitir acceso a recursos públicos (login, css, js, imágenes, etc)
                if (uri.endsWith("login") || uri.endsWith("login.jsp") || uri.endsWith("logout")
                        || uri.contains("/css/") || uri.contains("/js/") || uri.contains("/images/")) {
                    chain.doFilter(request, response);
                    return;
                }

                // Si no hay usuario logueado, redirigir al login
                if (usuario == null) {
                    resp.sendRedirect("login.jsp");
                    return;
                }
                   String rol = usuario.getRol();

            // Protegemos URLs sensibles
            // Solo admins pueden crear, editar y eliminar especies
            if (uri.contains("/treespecies")) {
                String option = req.getParameter("option");
                if (option != null && (option.equals("new") || option.equals("update") || option.equals("delete"))) {
                    if (!"admin".equals(rol)) {
                        resp.sendError(HttpServletResponse.SC_FORBIDDEN, "Acceso denegado.");
                        return;
                    }
                }
            }

                // Controlar acceso según rol a las páginas específicas

                // Página admin solo para rol admin
                if (uri.endsWith("indexadmin.jsp") && !"admin".equals(usuario.getRol())) {
                    resp.sendError(HttpServletResponse.SC_FORBIDDEN, "Acceso denegado.");
                    return;
                }

                // Página usuario para rol usuario o admin
                if (uri.endsWith("index.jsp") && !"usuario".equals(usuario.getRol()) && !"admin".equals(usuario.getRol())) {
                    resp.sendError(HttpServletResponse.SC_FORBIDDEN, "Acceso denegado.");
                    return;
                }

                // Si se quiere proteger otras rutas, añadir reglas similares aquí

                // Permitir continuar la petición
                chain.doFilter(request, response);
            }

            @Override
            public void destroy() {
                // Limpieza si es necesario
            }
        }
