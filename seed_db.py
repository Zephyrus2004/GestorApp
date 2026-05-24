import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile
from inventario.models import Categoria, Producto, Asignacion

def seed():
    print("Iniciando la siembra de la base de datos (IT Shop)...")

    # 1. Crear Superusuario y Usuarios de prueba
    users_data = [
        {'username': 'admin', 'email': 'admin@infotech.com', 'first_name': 'Cesar', 'last_name': 'Ceferino', 'rol': 'admin', 'is_superuser': True, 'is_staff': True},
        {'username': 'gestor', 'email': 'gestor@infotech.com', 'first_name': 'Ana', 'last_name': 'Gomez', 'rol': 'gestor', 'is_superuser': False, 'is_staff': True},
        {'username': 'usuario', 'email': 'usuario@infotech.com', 'first_name': 'Pedro', 'last_name': 'Perez', 'rol': 'usuario', 'is_superuser': False, 'is_staff': False},
    ]

    created_users = {}
    for data in users_data:
        # Si ya existe, lo actualizamos para cambiar el nombre/apellido y email
        user, created = User.objects.get_or_create(
            username=data['username'],
            defaults={
                'email': data['email'],
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'is_superuser': data['is_superuser'],
                'is_staff': data['is_staff'],
            }
        )
        if not created:
            user.email = data['email']
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.save()
            print(f"Usuario '{data['username']}' actualizado.")
        else:
            user.set_password('password123')
            user.save()
            print(f"Usuario '{data['username']}' creado con contraseña: password123")
            
        # Asegurar que el perfil tiene el rol correcto
        profile, p_created = UserProfile.objects.get_or_create(user=user)
        profile.rol = data['rol']
        profile.departamento = 'Gerencia y Control' if data['rol'] == 'admin' else ('Ventas e Inventario' if data['rol'] == 'gestor' else 'Cliente Preferencial')
        profile.telefono = '+58 412 5551234'
        profile.save()
        created_users[data['rol']] = user

    # 2. Crear Categorías
    categorias_data = [
        {'nombre': 'Laptops y Computadoras', 'descripcion': 'Equipos de computación portátiles y de escritorio de alta gama.', 'icono': 'bi-laptop'},
        {'nombre': 'Impresoras y Escáneres', 'descripcion': 'Equipos de impresión láser, multifuncionales y digitalización.', 'icono': 'bi-printer'},
        {'nombre': 'Servidores y Redes', 'descripcion': 'Equipos de comunicación, routers, switches, servidores y racks empresariales.', 'icono': 'bi-router'},
        {'nombre': 'Componentes y Accesorios', 'descripcion': 'Procesadores, tarjetas gráficas, memorias RAM, discos SSD y periféricos.', 'icono': 'bi-cpu'},
        {'nombre': 'Licencias de Software', 'descripcion': 'Sistemas operativos, antivirus, suites de oficina y software especializado.', 'icono': 'bi-file-earmark-code'},
    ]

    created_categories = {}
    for c_data in categorias_data:
        cat, created = Categoria.objects.get_or_create(
            nombre=c_data['nombre'],
            defaults={
                'descripcion': c_data['descripcion'],
                'icono': c_data['icono']
            }
        )
        if created:
            print(f"Categoría '{c_data['nombre']}' creada.")
        created_categories[c_data['nombre']] = cat

    # 3. Crear Productos
    productos_data = [
        # Laptops
        {
            'nombre': 'ThinkPad L14 Gen 4',
            'descripcion': 'Laptop corporativa para diseño y desarrollo de software comercial. Ryzen 5, 16GB RAM, 512GB SSD.',
            'categoria': created_categories['Laptops y Computadoras'],
            'marca': 'Lenovo',
            'modelo': 'L14 Gen 4',
            'numero_serie': 'LNV-SER-99218',
            'precio': 850.00,
            'stock': 12,
            'estado': Producto.Estado.NUEVO,
            'disponible': True,
            'ubicacion': 'Vitrina Principal (Pasillo A)'
        },
        {
            'nombre': 'MacBook Air M2',
            'descripcion': 'Equipo de diseño y desarrollo gráfico profesional. Chip M2, 8GB RAM, 256GB SSD.',
            'categoria': created_categories['Laptops y Computadoras'],
            'marca': 'Apple',
            'modelo': 'Air M2 2023',
            'numero_serie': 'APL-MAC-22831',
            'precio': 1100.00,
            'stock': 4,
            'estado': Producto.Estado.BUENO,
            'disponible': False,
            'ubicacion': 'Alquilado / Entregado a Cliente'
        },
        # Impresoras
        {
            'nombre': 'LaserJet Enterprise M507dn',
            'descripcion': 'Impresora láser de alto rendimiento y volumen para oficinas comerciales de alta demanda.',
            'categoria': created_categories['Impresoras y Escáneres'],
            'marca': 'HP',
            'modelo': 'M507dn',
            'numero_serie': 'HP-LAS-00918',
            'precio': 450.00,
            'stock': 3,
            'estado': Producto.Estado.REGULAR,
            'disponible': True,
            'ubicacion': 'Depósito Central'
        },
        # Servidores y Redes
        {
            'nombre': 'Switch Catalyst 2960-L',
            'descripcion': 'Switch gestionable de 24 puertos Gigabit Ethernet con enlaces ascendentes SFP de 1G.',
            'categoria': created_categories['Servidores y Redes'],
            'marca': 'Cisco',
            'modelo': 'WS-C2960L-24TS-LL',
            'numero_serie': 'CSC-SW-11827',
            'precio': 680.00,
            'stock': 2,
            'estado': Producto.Estado.BUENO,
            'disponible': True,
            'ubicacion': 'Estante de Redes'
        },
        {
            'nombre': 'Servidor PowerEdge R750',
            'descripcion': 'Servidor de rack de alto rendimiento Dell PowerEdge R750 para bases de datos corporativas y virtualización.',
            'categoria': created_categories['Servidores y Redes'],
            'marca': 'Dell',
            'modelo': 'PowerEdge R750',
            'numero_serie': 'DLL-SRV-88271',
            'precio': 4500.00,
            'stock': 1,
            'estado': Producto.Estado.NUEVO,
            'disponible': True,
            'ubicacion': 'Área de Servidores'
        },
        # Componentes
        {
            'nombre': 'Memoria RAM DDR4 16GB',
            'descripcion': 'Módulo de memoria Kingston Fury Beast 3200MHz de alta velocidad para computadoras gaming y estaciones de trabajo.',
            'categoria': created_categories['Componentes y Accesorios'],
            'marca': 'Kingston',
            'modelo': 'Fury Beast DDR4',
            'numero_serie': 'KNG-RAM-44781',
            'precio': 45.00,
            'stock': 25,
            'estado': Producto.Estado.NUEVO,
            'disponible': True,
            'ubicacion': 'Vitrina Accesorios'
        },
        # Software
        {
            'nombre': 'Windows 11 Home OEM',
            'descripcion': 'Paquete de licencias de sistema operativo Windows 11 Home OEM para computadoras nuevas.',
            'categoria': created_categories['Licencias de Software'],
            'marca': 'Microsoft',
            'modelo': '11 Home',
            'numero_serie': 'MSFT-WIN-HM-01',
            'precio': 99.00,
            'stock': 150,
            'estado': Producto.Estado.NUEVO,
            'disponible': True,
            'ubicacion': 'Depósito Digital (Licencias)'
        }
    ]

    for p_data in productos_data:
        # Actualizamos o creamos
        prod, created = Producto.objects.update_or_create(
            numero_serie=p_data['numero_serie'],
            defaults={
                'nombre': p_data['nombre'],
                'descripcion': p_data['descripcion'],
                'categoria': p_data['categoria'],
                'marca': p_data['marca'],
                'modelo': p_data['modelo'],
                'precio': p_data['precio'],
                'stock': p_data['stock'],
                'estado': p_data['estado'],
                'disponible': p_data['disponible'],
                'ubicacion': p_data['ubicacion'],
                'registrado_por': created_users['admin']
            }
        )
        if created:
            print(f"Producto '{p_data['nombre']}' creado.")
        else:
            print(f"Producto '{p_data['nombre']}' actualizado.")
        
        # 4. Crear Asignaciones de prueba para el equipo alquilado
        if not prod.disponible and prod.nombre == 'MacBook Air M2':
            Asignacion.objects.get_or_create(
                producto=prod,
                asignado_a=created_users['usuario'],
                defaults={
                    'departamento': 'Cliente Corporativo - Diseño',
                    'estado': Asignacion.EstadoAsignacion.ACTIVA,
                    'observaciones': 'Alquilado a cliente corporativo para producción mensual de campaña publicitaria.',
                    'asignado_por': created_users['gestor']
                }
            )
            print(f"Asignacion activa creada para '{prod.nombre}' -> '{created_users['usuario'].username}'")

    print("\nSiembra completada con exito! La tienda de informatica tiene sus productos, categorias y usuarios inicializados.")

if __name__ == '__main__':
    seed()
