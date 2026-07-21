<div align="center">

# 🌊 WaraWave

### Información ciudadana para playas más seguras

Aplicación web para reportar incidentes en playas, consultar condiciones marítimas y apoyar la moderación mediante información de la comunidad.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.38%2B-FF4B4B?logo=streamlit&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-Auth%20%7C%20Database%20%7C%20Storage-3ECF8E?logo=supabase&logoColor=white)
![Open-Meteo](https://img.shields.io/badge/Open--Meteo-Marine%20API-1485CC)

</div>

---

## 📌 Descripción

**WaraWave** es una aplicación web desarrollada con **Python y Streamlit** para informar sobre el estado de las playas de Arica.

La plataforma permite que los ciudadanos registren reportes con evidencia y ubicación geográfica, revisen publicaciones de la comunidad y consulten condiciones marítimas estimadas.

También incluye herramientas especiales para administradores y autoridades, facilitando la moderación de contenido y el análisis de reportes por playa, categoría y fecha.

El proyecto fue desarrollado en la **Universidad de Tarapacá, Arica**, durante el primer semestre de 2026 para la asignatura **Taller de Técnicas de Programación**.

---

## ✨ Funcionalidades

### 👤 Ciudadanos

- Registro e inicio de sesión mediante **Supabase Auth**.
- Creación de reportes seleccionando una playa.
- Clasificación mediante categorías.
- Creación de categorías personalizadas con la opción `Otro`.
- Registro automático de ubicación geográfica.
- Visualización de la ubicación mediante un mapa.
- Adjuntar imágenes o videos como evidencia.
- Tablón comunitario ordenado cronológicamente.
- Filtros por playa y categoría.
- Confirmación única de reportes de otros usuarios.
- Opción **Tengo dudas** para alertar sobre información posiblemente incorrecta.
- Selección del motivo asociado a una duda.
- Historial personal de reportes.
- Visualización de reportes activos y retirados por moderación.

### 🌊 Condiciones del mar

La aplicación consulta información marítima mediante **Open-Meteo Marine API**.

Se muestran las siguientes variables:

- Altura de las olas.
- Período de las olas.
- Dirección de las olas.
- Temperatura superficial del mar.
- Nivel del mar.
- Velocidad de la corriente.
- Dirección de la corriente.

La información puede consultarse para:

- Playa Laucho.
- Playa Lisera.
- Playa Chinchorro.
- Playa Las Machas.

El nivel de riesgo se representa mediante colores e íconos:

| Nivel | Representación |
|---|---|
| Tranquilo | 🟢 |
| Moderado | 🟡 |
| Fuerte | 🟠 |
| Peligroso | 🔴 |

Los datos se almacenan temporalmente y se actualizan automáticamente cada hora.

> Los valores marítimos son estimaciones por sector. No reemplazan los avisos oficiales de la Armada, autoridades o salvavidas.

### 🛡️ Administradores

- Revisar reportes publicados.
- Retirar reportes del tablón.
- Restaurar reportes retirados.
- Mantener los reportes dentro del historial de su autor.
- Consultar la cantidad de confirmaciones.
- Consultar la cantidad de marcas de duda.
- Revisar los motivos asociados a las dudas.
- Filtrar reportes con o sin dudas.
- Ordenar reportes por cantidad de dudas.
- Activar o desactivar usuarios.
- Cambiar el rol de los usuarios.

### 📊 Autoridades

- Acceder al panel de auditoría.
- Filtrar reportes por playa.
- Filtrar por categoría.
- Filtrar por estado.
- Filtrar por rango de fechas.
- Consultar resúmenes por zona.
- Identificar reportes prioritarios.
- Revisar confirmaciones.
- Consultar coordenadas para apoyar inspecciones.

---

## 👥 Roles

| Rol | Acceso |
|---|---|
| `ciudadano` | Tablón, historial, oleaje y creación de reportes |
| `administrador` | Funciones ciudadanas, moderación y gestión de usuarios |
| `autoridad` | Funciones ciudadanas y panel de auditoría |

Todas las cuentas nuevas se registran inicialmente con el rol:

```text
ciudadano
```

Los roles especiales deben ser asignados posteriormente por un administrador o directamente desde Supabase.

---

## 🧰 Tecnologías utilizadas

- **Python**
- **Streamlit**
- **Supabase Auth**
- **Supabase PostgreSQL**
- **Supabase Storage**
- **Row Level Security — RLS**
- **Open-Meteo Marine API**
- **streamlit-geolocation**
- **Requests**
- **Git y GitHub**
- **TOML**

---

## 📁 Estructura del proyecto

```text
WaraWave/
├── app.py
├── configuracion.py
├── estilos.py
├── navegacion.py
├── oleaje.py
├── utilidades.py
├── requirements.txt
├── database_actualizacion_CORREGIDO.sql
├── README.md
│
├── .streamlit/
│   └── secrets.toml
│
└── vistas/
    ├── __init__.py
    ├── administracion.py
    ├── autenticacion.py
    ├── bienvenida.py
    ├── componentes_reportes.py
    ├── crear_reporte.py
    ├── historial.py
    ├── oleaje.py
    └── tablon.py
```

El archivo `.streamlit/secrets.toml` contiene credenciales privadas y **no debe subirse a GitHub**.

---

## ⚙️ Requisitos

Antes de ejecutar la aplicación necesitas:

- Python 3.10 o superior.
- Git.
- Una cuenta de Supabase.
- Un proyecto activo en Supabase.
- Conexión a Internet.
- Un navegador con permisos de geolocalización.

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/joaquinquezadaflores-cell/WaraWave.git
```

Entrar a la carpeta:

```bash
cd WaraWave
```

Para trabajar con la rama de Ayleen:

```bash
git switch ayleen
```

### 2. Crear un entorno virtual

En Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\activate
```

En Linux o macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

---

## 🔐 Configuración de Supabase

### Base de datos

En Supabase, entra a:

```text
SQL Editor → New query
```

Ejecuta el archivo:

```text
database_actualizacion_CORREGIDO.sql
```

Este archivo configura, entre otras cosas:

- Vinculación con Supabase Auth.
- Roles de usuarios.
- Estado activo o desactivado.
- Ubicación geográfica de reportes.
- Moderación sin eliminación física.
- Confirmaciones únicas.
- Políticas de seguridad RLS.
- Almacenamiento de evidencias.

La aplicación también utiliza la tabla:

```text
dudas_reportes
```

Esta tabla registra los reportes marcados como dudosos y sus respectivos motivos.

### Credenciales locales

Crea la carpeta:

```text
.streamlit
```

Dentro crea:

```text
secrets.toml
```

Agrega lo siguiente:

```toml
[connections.supabase]
url = "TU_PROJECT_URL"
key = "TU_PUBLISHABLE_KEY"
```

Utiliza una clave pública:

```text
sb_publishable_...
```

También puede utilizarse la clave antigua:

```text
anon public
```

Nunca publiques claves como:

```text
service_role
sb_secret_
```

---

## ▶️ Ejecutar la aplicación

Con el entorno virtual activado:

```bash
python -m streamlit run app.py
```

La aplicación estará disponible normalmente en:

```text
http://localhost:8501
```

Para utilizar otro puerto:

```bash
python -m streamlit run app.py --server.port 8502
```

---

## 👑 Crear una cuenta administradora

Primero registra la cuenta normalmente desde WaraWave.

Después ejecuta en Supabase:

```sql
update public.usuarios
set rol = 'administrador',
    activo = true
where lower(correo) = lower('correo-admin@gmail.com');
```

Cierra la sesión y vuelve a ingresar para actualizar los permisos.

---

## 🏛️ Crear una cuenta de autoridad

Primero registra la cuenta normalmente desde WaraWave.

Después ejecuta:

```sql
update public.usuarios
set rol = 'autoridad',
    activo = true
where lower(correo) = lower('correo-autoridad@gmail.com');
```

---

## 🗃️ Evidencias permitidas

| Tipo | Formatos | Tamaño máximo |
|---|---|---:|
| Imagen | PNG, JPG, JPEG y GIF | 8 MB |
| Video | MP4, WebM y MOV | 20 MB |

Los archivos se almacenan en el bucket:

```text
reportes-imagenes
```

---

## 🔒 Seguridad

WaraWave incorpora:

- Autenticación mediante Supabase Auth.
- Contraseñas administradas por Supabase.
- Validación de correos.
- Validación de contraseñas seguras.
- Políticas de seguridad a nivel de fila.
- Separación de permisos mediante roles.
- Bloqueo de confirmaciones repetidas.
- Restricción de valoraciones sobre reportes propios.
- Protección del contenido ingresado por usuarios.
- Credenciales separadas del código fuente.
- Moderación sin pérdida del historial personal.

---

## 🧪 Flujo de prueba

Para comprobar las funciones principales:

1. Registrar una cuenta ciudadana.
2. Iniciar sesión.
3. Crear un reporte.
4. Registrar la ubicación geográfica.
5. Adjuntar una imagen o video.
6. Ingresar con una segunda cuenta.
7. Confirmar el reporte o marcarlo como dudoso.
8. Revisar el historial del autor.
9. Ingresar como administrador para moderar.
10. Ingresar como autoridad para revisar la auditoría.
11. Consultar las condiciones marítimas.

---

## 👨‍💻 Equipo

- **Ayleen Humire**
- **Joaquín Quezada**
- **Catalina Ramírez**
- **Benjamín Aguilera**

---

## 🎓 Contexto académico

- **Universidad:** Universidad de Tarapacá
- **Sede:** Arica, Chile
- **Asignatura:** Taller de Técnicas de Programación
- **Periodo:** Primer semestre de 2026

---

<div align="center">

## 🌊 WaraWave

**Información ciudadana para playas más seguras**

</div>