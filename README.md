# Examen DUOC - Proyecto Full Stack

Este es un proyecto de examen del DUOC, construido utilizando Nuxt 3 para el frontend y Django Rest Framework para el backend.

## Descripción

El objetivo de este proyecto es desarrollar una aplicación web full stack que demuestre el conocimiento en tecnologías modernas de desarrollo web. La aplicación está compuesta por un backend desarrollado en Django Rest Framework y un frontend desarrollado en Nuxt 3.

## Tecnologías Utilizadas

- **Backend**: Django Rest Framework
- **Frontend**: Nuxt 3

## Requisitos

- **Python** (3.x recomendado)
- **Node.js** (14.x o superior)
- **pip** (para la instalación de paquetes de Python)
- **npm** (para la instalación de paquetes de Node.js)

## Configuración del Proyecto

### Backend (Django Rest Framework)

1. Clona el repositorio:

    ```bash
    git clone <https://github.com/Niko2Tech/django-nuxt-3>
    cd <backend>
    ```

2. Crea y activa un entorno virtual:

    ```bash
    python -m venv env
    source env/bin/activate  # En Windows usa `env\Scripts\activate`
    ```

3. Instala las dependencias de Python:

    ```bash
    pip install -r requirements.txt
    ```

4. Realiza las migraciones y ejecuta el servidor de desarrollo:

    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

5. Accede a `http://127.0.0.1:8000` para verificar que el backend está funcionando.

### Frontend (Nuxt 3)

1. Navega al directorio `frontend`:

    ```bash
    cd frontend
    ```

2. Instala las dependencias de Node.js:

    ```bash
    npm install
    ```

3. Ejecuta el servidor de desarrollo:

    ```bash
    npm run dev
    ```

4. Accede a `http://localhost:3000` para verificar que el frontend está funcionando.

