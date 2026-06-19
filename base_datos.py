import sqlite3
import re
import bcrypt

DB_NAME = "veronica_avanzado.db"

def inicializar_db():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS materias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS preguntas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            materia_id INTEGER,
            enunciado TEXT NOT NULL,
            opcion_a TEXT NOT NULL,
            opcion_b TEXT NOT NULL,
            opcion_c TEXT NOT NULL,
            opcion_d TEXT NOT NULL,
            correcta INTEGER NOT NULL,
            mejora TEXT NOT NULL,
            FOREIGN KEY (materia_id) REFERENCES materias(id)
        )
    """)
    
    conexion.commit()
    conexion.close()
    _insertar_datos_iniciales()

def validar_politica_contrasena(contrasena):
    if len(contrasena) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres."
    if not re.search(r"[A-Z]", contrasena):
        return False, "La contraseña debe incluir al menos una letra mayúscula."
    if not re.search(r"[0-9]", contrasena):
        return False, "La contraseña debe incluir al menos un número."
    return True, "Contraseña segura."

def registrar_usuario(usuario, contrasena):
    cumple_politica, _ = validar_politica_contrasena(contrasena)
    if not cumple_politica:
        return False
        
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        
        # Aumentamos el factor de trabajo a 12 (estándar seguro en la industria)
        sal = bcrypt.gensalt(rounds=12)
        contra_encriptada = bcrypt.hashpw(contrasena.encode('utf-8'), sal)
        
        # Consulta completamente parametrizada (Evita Inyección SQL)
        cursor.execute("INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)", (usuario, contra_encriptada))
        conexion.commit()
        conexion.close()
        return True
    except sqlite3.IntegrityError:
        return False

def validar_credenciales(usuario, contrasena):
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    # Consulta parametrizada segura
    cursor.execute("SELECT contrasena FROM usuarios WHERE usuario = ?", (usuario,))
    resultado = cursor.fetchone()
    conexion.close()
    
    if resultado:
        contra_guardada = resultado[0]
        return bcrypt.checkpw(contrasena.encode('utf-8'), contra_guardada)
    return False

def obtener_materias():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre FROM materias")
    materias = [fila[0] for fila in cursor.fetchall()]
    conexion.close()
    return materias

def obtener_preguntas_materia(nombre_materia):
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT p.id, p.enunciado, p.opcion_a, p.opcion_b, p.opcion_c, p.opcion_d, p.correcta, p.mejora
        FROM preguntas p
        JOIN materias m ON p.materia_id = m.id
        WHERE m.nombre = ?
    """, (nombre_materia,))
    
    filas = cursor.fetchall()
    conexion.close()
    
    preguntas = []
    for fila in filas:
        preguntas.append({
            "id": fila[0],
            "pregunta": fila[1],
            "opciones": [fila[2], fila[3], fila[4], fila[5]],
            "correcta": fila[6],
            "mejora": fila[7]
        })
    return preguntas

def _insertar_datos_iniciales():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM materias")
    if cursor.fetchone()[0] == 0:
        materias = ["Lengua Española", "Matemática", "Álgebra", "Cálculo Diferencial", "Dibujo Técnico"]
        for m in materias:
            cursor.execute("INSERT INTO materias (nombre) VALUES (?)", (m,))
            
        cursor.execute("SELECT id FROM materias WHERE nombre = 'Lengua Española'")
        le_id = cursor.fetchone()[0]
        cursor.execute("""
            INSERT INTO preguntas (materia_id, enunciado, opcion_a, opcion_b, opcion_c, opcion_d, correcta, mejora)
            VALUES (?, '1. ¿Cuál de las siguientes palabras es esdrújula?', 'Sábado', 'Cantar', 'Árbol', 'Café', 0, 'Las esdrújulas se acentúan siempre en la antepenúltima sílaba.')
        """, (le_id,))
        cursor.execute("""
            INSERT INTO preguntas (materia_id, enunciado, opcion_a, opcion_b, opcion_c, opcion_d, correcta, mejora)
            VALUES (?, '2. ¿Qué tipo de palabra es correr?', 'Sustantivo', 'Verbo', 'Adjetivo', 'Adverbio', 1, 'Los verbos denotan acciones o estados.')
        """, (le_id,))

        cursor.execute("SELECT id FROM materias WHERE nombre = 'Matemática'")
        mat_id = cursor.fetchone()[0]
        cursor.execute("""
            INSERT INTO preguntas (materia_id, enunciado, opcion_a, opcion_b, opcion_c, opcion_d, correcta, mejora)
            VALUES (?, '1. ¿Cuál es el resultado de 7 + 5 * 2?', '24', '17', '14', '19', 1, 'Por jerarquía primero multiplicas 5*2 y luego sumas 7.')
        """, (mat_id,))
        cursor.execute("""
            INSERT INTO preguntas (materia_id, enunciado, opcion_a, opcion_b, opcion_c, opcion_d, correcta, mejora)
            VALUES (?, '2. ¿A cuánto equivale pi redondeado a dos decimales?', '3.12', '3.16', '3.14', '3.18', 2, 'El valor estándar es 3.14.')
        """, (mat_id,))

    conexion.commit()
    conexion.close()