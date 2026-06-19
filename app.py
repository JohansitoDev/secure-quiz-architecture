import streamlit as st
import time
import logica
import base_datos

st.set_page_config(
    page_title="Verónica - Simulador Universitario",
    page_icon="🎓",
    layout="centered"
)

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stRadio > label { font-size: 1.1rem; font-weight: 600; color: #1E3A8A; }
    .correct { color: #155724; background-color: #d4edda; padding: 12px; border-radius: 8px; margin-top: 5px; border-left: 5px solid #28a745; }
    .incorrect { color: #721c24; background-color: #f8d7da; padding: 12px; border-radius: 8px; margin-top: 5px; border-left: 5px solid #dc3545; }
    .feedback { font-style: italic; color: #495057; background-color: #e9ecef; padding: 10px; border-radius: 6px; margin-top: 5px; }
    .bot-header { background-color: #1E3A8A; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

base_datos.inicializar_db()
logica.inicializar_sesion()

if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False
if 'usuario_actual' not in st.session_state:
    st.session_state.usuario_actual = ""

if not st.session_state.autenticado:
    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>Acceso al Sistema</h2>", unsafe_allow_html=True)
    pestaña_login, pestaña_registro = st.tabs(["🔐 Iniciar Sesión", "📝 Registrarse"])
    
    with pestaña_login:
        with st.form("formulario_login"):
            usuario_log = st.text_input("Usuario:", key="log_user")
            pass_log = st.text_input("Contraseña:", type="password", key="log_pass")
            btn_login = st.form_submit_button("Ingresar", use_container_width=True)
            if btn_login:
                if base_datos.validar_credenciales(usuario_log, pass_log):
                    st.session_state.autenticado = True
                    st.session_state.usuario_actual = usuario_log
                    st.success("¡Acceso concedido!")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos.")
                    
with pestaña_registro:
        with st.form("formulario_registro"):
            usuario_reg = st.text_input("Elige un Nombre de Usuario:", key="reg_user")
            pass_reg = st.text_input("Elige una Contraseña:", type="password", key="reg_pass")
            btn_registro = st.form_submit_button("Crear Cuenta", use_container_width=True)
            if btn_registro:
                if usuario_reg.strip() == "" or pass_reg.strip() == "":
                    st.warning("Los campos no pueden estar vacíos.")
                else:
                  
                    valido, mensaje = base_datos.validar_politica_contrasena(pass_reg)
                    if not valido:
                        st.error(mensaje)
                    else:
                        if base_datos.registrar_usuario(usuario_reg, pass_reg):
                            st.success("¡Cuenta registrada con encriptación Bcrypt en SQLite!")
                        else:
                            st.error("El nombre de usuario ya existe.")


else:
    st.sidebar.markdown(f"👤 **Usuario:** {st.session_state.usuario_actual}")
    if st.sidebar.button("🚪 Cerrar Sesión", type="secondary", use_container_width=True):
        st.session_state.autenticado = False
        st.session_state.usuario_actual = ""
        st.session_state.examen_iniciado = False
        st.rerun()

    st.markdown(f"""
        <div class="bot-header">
            <h1>VERÓNICA</h1>
            <p style="font-size: 1.2rem; margin: 0;">"Hola {st.session_state.usuario_actual}, soy Verónica, tu modelo de simulación y asistente interactiva de exámenes."</p>
        </div>
    """, unsafe_allow_html=True)

    materias_disponibles = base_datos.obtener_materias()

    if not st.session_state.examen_iniciado:
        st.markdown("### 📋 ¿Qué soy y qué puedo hacer por ti?")
        st.write("Sistema estructurado profesional de evaluación universitaria con persistencia de datos.")
        st.write("---")
        st.markdown("### 🛠️ Elige tu examen")
        materia = st.selectbox("Selecciona la materia que deseas practicar hoy:", materias_disponibles)
        
        if st.button("🚀 Iniciar Examen con Verónica", type="primary", use_container_width=True):
            logica.iniciar_examen(materia)
            st.rerun()
    else:
        preguntas_actuales = base_datos.obtener_preguntas_materia(st.session_state.materia_seleccionada)
        
        respondidas = sum(1 for r in st.session_state.respuestas.values() if r is not None)
        todas_respondidas = (respondidas == len(preguntas_actuales))

        tiempo_actual = time.time()
        tiempo_restante_global = int(st.session_state.tiempo_limite - tiempo_actual)
        if tiempo_restante_global <= 0:
            tiempo_restante_global = 0


        @st.fragment(run_every=1.0)
        def mostrar_reloj():
            t_actual = time.time()
            t_restante = int(st.session_state.tiempo_limite - t_actual)
            if t_restante <= 0:
                t_restante = 0
            mins, secs = divmod(t_restante, 60)
            col_info, col_reloj = st.columns([3, 1])
            with col_info:
                st.markdown(f"🔹 **Examen Activo:** {st.session_state.materia_seleccionada}")
            with col_reloj:
                st.metric(label="⏱️ Tiempo Restante", value=f"{mins:02d}:{secs:02d}")
            
      
            if t_restante == 0 and not st.session_state.forzar_final:
                st.session_state.forzar_final = True
                st.rerun()

        mostrar_reloj()
        tiempo_agotado = (tiempo_restante_global <= 0)
        
        if todas_respondidas and not tiempo_agotado:
            st.success("🎉 ¡Prueba Finalizada! Has respondido todas las preguntas antes de tiempo.")
        elif tiempo_agotado or st.session_state.forzar_final:
            st.error("🚨 ¡El tiempo se ha agotado por completo! He cerrado el examen.")

        st.write("---")
        correctas_totales = 0
        
        for idx, item in enumerate(preguntas_actuales):
            st.markdown(f"### {item['pregunta']}")
            opcion_previa = st.session_state.respuestas.get(idx)
            index_previo = item["opciones"].index(opcion_previa) if opcion_previa in item["opciones"] else None
            ya_respondida = opcion_previa is not None
            bloquear = tiempo_agotado or st.session_state.forzar_final or ya_respondida
            
            opcion_seleccionada = st.radio(
                "Opciones:",
                item["opciones"],
                key=f"p_{idx}",
                index=index_previo,
                label_visibility="collapsed",
                disabled=bloquear
            )
            
            if opcion_seleccionada != opcion_previa and opcion_previa is None:
                st.session_state.respuestas[idx] = opcion_seleccionada
                st.rerun()

            if opcion_seleccionada is not None:
                idx_seleccionado = item["opciones"].index(opcion_seleccionada)
                if idx_seleccionado == item["correcta"]:
                    st.markdown('<div class="correct">✅ <b>Verónica dice:</b> ¡Correcto!</div>', unsafe_allow_html=True)
                    if opcion_seleccionada == opcion_previa:
                        correctas_totales += 1
                else:
                    st.markdown('<div class="incorrect">❌ <b>Verónica dice:</b> Incorrecto.</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="feedback">💡 <b>Mejora:</b> {item["mejora"]}</div>', unsafe_allow_html=True)
            st.write("---")

        st.sidebar.title("📊 Evaluación de Verónica")
        progreso = correctas_totales / len(preguntas_actuales) if len(preguntas_actuales) > 0 else 0
        st.sidebar.progress(progreso)
        st.sidebar.metric(label="Tus Aciertos", value=f"{correctas_totales} / {len(preguntas_actuales)}")
        
        if st.sidebar.button("🔄 Volver a intentar", type="secondary", use_container_width=True):
            logica.reiniciar_examen()
            st.rerun() 
        if st.sidebar.button("🚪 Cambiar de Materia", type="primary", use_container_width=True):
            logica.cambiar_materia()
            st.rerun()

