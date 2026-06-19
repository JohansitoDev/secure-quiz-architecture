import time
import streamlit as st
import base_datos

def inicializar_sesion():
    if 'examen_iniciado' not in st.session_state:
        st.session_state.examen_iniciado = False
    if 'materia_seleccionada' not in st.session_state:
        st.session_state.materia_seleccionada = ""
    if 'respuestas' not in st.session_state:
        st.session_state.respuestas = {}
    if 'tiempo_limite' not in st.session_state:
        st.session_state.tiempo_limite = None
    if 'forzar_final' not in st.session_state:
        st.session_state.forzar_final = False

def iniciar_examen(materia):
    st.session_state.examen_iniciado = True
    st.session_state.materia_seleccionada = materia
    st.session_state.forzar_final = False
    preguntas = base_datos.obtainer_preguntas_materia(materia)
    st.session_state.respuestas = {i: None for i in range(len(preguntas))}
    st.session_state.tiempo_limite = time.time() + 180

def reiniciar_examen():
    iniciar_examen(st.session_state.materia_seleccionada)
    st.rerun()

def cambiar_materia():
    st.session_state.examen_iniciado = False
    st.rerun()