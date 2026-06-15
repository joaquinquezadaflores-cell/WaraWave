# WaraWave

## Descripción del proyecto
WaraWave es una aplicación web interactiva desarrollada en **Python** y potenciada por el entorno de desarrollo **Streamlit**. El sistema está diseñado para conectarse de forma segura y directa a una base de datos relacional en la nube provista por **Supabase** y consumir datos oceanográficos en tiempo real.

Este proyecto corresponde a un desarrollo enfocado en la gestión de usuarios, el control de alertas y el monitoreo de variables marítimas, implementado bajo estándares modernos de protección de datos, configuración limpia y consumo de APIs externas.

El proyecto está siendo desarrollado en la *Universidad de Tarapacá (Arica)* durante el *primer semestre de 2026*, en el ramo *Taller de Técnicas de Programación*.

## Autores
- Ayleen Humire
- Joaquin Quezada
- Catalina Ramirez
- Benjamin Aguilera

## Características
- **Conexión en la Nube:** Integración nativa con bases de datos en la nube mediante Supabase.
- **Seguridad Avanzada:** Almacenamiento de credenciales críticas aislado del código mediante el sistema centralizado de secretos de Streamlit.
- **Gestión de Usuarios:** Interfaz intuitiva para el registro e inserción automática de cuentas en la base de datos en tiempo real.
- **Creación de Reportes:** Apartado donde los usuarios desarrollan reportes en base a lo que observan.
- **Módulo Administrativo:** Panel exclusivo para administradores con privilegios elevados para auditar, gestionar y eliminar reportes del sistema de forma segura.
- **Monitoreo Marítimo en Tiempo Real:** Integración con la API global **Open-Meteo** para visualizar datos en vivo sobre el oleaje (altura, período y dirección de las olas) y condiciones del mar.
- **Control de Acceso Riguroso:** Implementación y auditoría de políticas de seguridad a nivel de fila (RLS) en la base de datos.

## Tecnologías utilizadas
- Python 3.14.6
- Streamlit (Interfaz gráfica web)
- Supabase-py (Cliente oficial de Supabase)
- Open-Meteo API (Datos meteorológicos y de oleaje marinos)
- Git / GitHub
- TOML (Para la gestión de variables de entorno locales)

## Requisitos
- Python 3.10 o superior instalado.
- Cuenta de Supabase con un proyecto activo.
- Terminal compatible (PowerShell, Bash o similar).
- Conexión estable a Internet.

## Instalación

1. **Clonar el repositorio:**
   Abre tu terminal en la carpeta donde deseas guardar el proyecto y clona el código ejecutable desde GitHub:
   ```bash
   git clone https://github.com
   ```

2. **Acceder a la ruta de instalación:**
   Ingresa a la carpeta principal del proyecto:
   ```bash
   cd WaraWave
   ```

3. **Configurar el entorno virtual e instalar dependencias:**
   Crea y activa tu entorno virtual, y luego instala las librerías necesarias especificadas en el archivo de requerimientos:
   ```bash
   python -m venv venv
   # En Windows para activar:
   .\venv\Scripts\activate
   # Instalar requerimientos:
   pip install -r requirements.txt
   ```

4. **Configuración secreta de credenciales locales:**
   Para que la aplicación funcione en tu entorno local sin exponer tus claves en GitHub, crea una carpeta llamada `.streamlit` en la raíz del proyecto y dentro añade el archivo `secrets.toml`:
   ```toml
   [connections.supabase]
   url = "https://supabase.co"
   key = "tu_llave_anon_legacy_public_key_aqui"
   ```
   *(Tip: Asegúrate de que el archivo `.gitignore` contenga la línea `.streamlit/secrets.toml` antes de realizar cualquier commit).*

## Uso básico

1. Asegúrate de tener activo tu entorno virtual (`venv`).
2. Ejecuta el servidor local de la interfaz interactiva escribiendo en la terminal:
   ```bash
   streamlit run app.py
   ```
3. La aplicación se abrirá automáticamente en tu navegador web predeterminado (por defecto en la ruta `http://localhost:8501`).
4. Interactúa con el formulario de creación de cuentas, visualiza el oleaje en tiempo real en los paneles informativos o accede al módulo administrador si cuentas con las credenciales requeridas.
