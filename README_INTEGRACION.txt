DENTYX — LANDING "ELIGE TU ROL" (PACIENTE / DENTISTA)
====================================================
Archivos incluidos y qué hace cada uno:

1) config/urls.py
   - Define la ruta raíz "" para mostrar la landing de elección de rol.
   - Incluye las rutas de los módulos de paciente y dentista.

2) apps/accounts/views.py
   - Vista ChooseRoleView (TemplateView) que renderiza templates/accounts/choose_role.html.
   - Propaga el parámetro ?next= si se llega desde un recurso protegido.

3) templates/accounts/choose_role.html
   - Página con diseño usando la paleta LUNA.
   - Botones para "Paciente" y "Dentista" con enlaces a login/registro de cada rol.

4) frontend_paciente/urls.py y frontend_paciente/views.py
   - Endpoints mínimos: /paciente/login/ y /paciente/registro/.
   - Vistas placeholder para que puedas conectar tu lógica real.

5) frontend_dentista/urls.py y frontend_dentista/views.py
   - Endpoints mínimos: /dentista/login/ y /dentista/registro/.
   - Vistas placeholder para que puedas conectar tu lógica real.

6) static/css/base.css (opcional)
   - Estilos base. Si ya cuentas con uno, puedes ignorar este archivo.

INTEGRACIÓN
-----------
- Copia el contenido en tu proyecto Django manteniendo la misma estructura de carpetas.
- Verifica en settings.py:
    INSTALLED_APPS incluye "apps.accounts", "frontend_paciente", "frontend_dentista".
    TEMPLATES['DIRS'] incluye la carpeta 'templates' del proyecto.
    STATICFILES_DIRS incluye la carpeta 'static' si es un proyecto multipaquete.

- Reinicia el servidor: python manage.py runserver 8001 --settings=config.settings.dev
- Visita: http://127.0.0.1:8001/ para ver la landing.
