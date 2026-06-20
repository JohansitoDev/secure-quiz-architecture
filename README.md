# 🎓 Verónica - Mi Simulador Universitario Interactivo

¡Hola! Te presento a **Verónica**, un simulador interactivo y asistente de exámenes universitarios que desarrollé para ayudar a los estudiantes a practicar sus materias mediante una interfaz web estructurada, dinámica y con persistencia de datos.

Construí este proyecto utilizando **Python** junto con **Streamlit** para el frontend, y diseñé una arquitectura modular respaldada por **SQLite** y encriptación con **Bcrypt** para garantizar una gestión de usuarios completamente segura.

---

## ⚠️ Estado del Proyecto (En Desarrollo)

> **Nota importante:** Esta aplicación se encuentra actualmente en **fase activa de desarrollo**. Debido a que sigo mejorando la lógica del backend y optimizando los fragmentos de la interfaz, es muy probable que te encuentres con algunos errores temporales, bugs o conflictos de estado (*state issues*) al interactuar con ciertas funciones. ¡Agradezco enormemente la paciencia mientras sigo puliendo los detalles!

---

## 🛠️ Características Principales de Mi Aplicación

* 🔐 **Autenticación Segura:** Diseñé un sistema de registro e inicio de sesión que protege las credenciales de los usuarios encriptando las contraseñas con Bcrypt antes de guardarlas en la base de datos.
* ⏱️ **Temporizador Optimizado:** Implementé un control de tiempo dinámico por examen utilizando fragmentos de Streamlit (`@st.fragment`), lo que permite actualizar el reloj cada segundo de forma eficiente sin recargar toda la interfaz.
* 📊 **Evaluación e Inmediata Retroalimentación:** El sistema evalúa las respuestas al instante, muestra barras de progreso en el panel lateral y ofrece sugerencias personalizadas de mejora para las respuestas incorrectas.
* 🗄️ **Persistencia de Datos:** Estructuré el backend de forma desacoplada para manejar la lógica de las preguntas y los usuarios mediante una base de datos SQLite local (`veronica_avanzado.db`).

---

## 🚀 Cómo Ejecutar Mi Proyecto Localmente

1. **Clonar este repositorio:**
   ```bash
   git clone [https://github.com/JohansitoDev/secure-quiz-architecture.git](https://github.com/JohansitoDev/secure-quiz-architecture.git)
   cd secure-quiz-architecture