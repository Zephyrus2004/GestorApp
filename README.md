# 🖥️ Portal Universitario — Sistema de Productos de Informática

Sistema web para la gestión de productos y equipos de informática en una universidad, construido con **Django 5.x** y **Bootstrap 5**.

## 🚀 Características

- 🔐 **Autenticación completa**: Registro, login, logout, cambio de contraseña
- 👥 **Roles de usuario**: Administrador, Gestor, Usuario, Visitante
- 📦 **Inventario de equipos**: CRUD completo de productos y categorías
- 📊 **Dashboards por rol**: Cada rol ve información relevante a sus permisos
- 🛡️ **Control de acceso**: Decoradores de autorización por rol
- ⚙️ **Django Admin**: Panel de administración configurado

## 🛠️ Tecnologías

| Herramienta | Versión |
|---|---|
| Python | 3.13+ |
| Django | 5.x |
| Base de datos | SQLite |
| Frontend | Bootstrap 5 |
| Formularios | django-crispy-forms |

## 📁 Estructura del Proyecto

```
portal_uni/
├── core/           ← Configuración central Django
├── accounts/       ← Autenticación y perfiles de usuario
├── dashboard/      ← Vistas y paneles por rol
├── inventario/     ← Gestión de productos y equipos
├── static/         ← Archivos estáticos (CSS, JS, imágenes)
├── media/          ← Archivos subidos por usuarios
├── templates/      ← Templates globales
├── manage.py
├── requirements.txt
└── .env
```

## ⚡ Instalación

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/portal_uni.git
cd portal_uni

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
copy .env.example .env  # y editar SECRET_KEY

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
```

## 👤 Roles del Sistema

| Rol | Permisos |
|---|---|
| **Administrador** | Acceso total: usuarios, inventario, reportes, configuración |
| **Gestor** | Gestión de inventario: crear, editar, asignar productos |
| **Usuario** | Consultar inventario y solicitar equipos |
| **Visitante** | Solo lectura del catálogo público |

## 📄 Licencia

Este proyecto es de uso educativo.
