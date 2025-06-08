    #    ##---FRONT-Streamlit---##
import streamlit as st
from logica_cuestionario import evaluar_respuestas
from logica_cuestionario import obtener_servicios_relevantes
from fpdf import FPDF
import base64

st.set_page_config(page_title="Cuestionario Proveedores de Nube", layout="centered")
#---------- PANTALLA DE INICIO -----------##
if "cuestionario_iniciado" not in st.session_state:
    st.session_state["cuestionario_iniciado"] = False

if not st.session_state["cuestionario_iniciado"]:
    st.title("Guía de Selección de Proveedor de Nube")
    st.markdown("""
    Esta herramienta sirve como guía para elegir el proveedor que mejor se adapte a las necesidades del proyecto.
    Se considerarán aspectos como:
    - Almacenamiento
    - Bases de datos
    - Inteligencia Artificial
    - Scrapping 
    ---
    Elija un enfoque de seguridad
    """)

    if st.button("Enfoque confidencialidad "):
        st.session_state["cuestionario_iniciado"] = True
    else:
        st.markdown(
            '<a href="https://www.ejemplo.com/integridad" target="_blank">'
            '<button style="background-color:#f44336;color:white;border:none;padding:8px 16px;border-radius:4px;">Enfoque integridad</button>'
            '</a>',
            unsafe_allow_html=True
        )
    st.stop()


def generar_descripcion_servicio(servicio):
    texto = f"{servicio['nombre']}\n"
    if "caracteristicas_confidencialidad" in servicio:
        texto += "Confidencialidad:\n"
        for c in servicio["caracteristicas_confidencialidad"]:
            texto += f"  - {c}\n"
    if "regiones_disponibles" in servicio:
        texto += "Regiones:\n"
        for r in servicio["regiones_disponibles"]:
            texto += f"  - {r}\n"
    if "costo_aproximado" in servicio:
        texto += f"Costo aproximado: {servicio['costo_aproximado']}\n"
    return texto
####--------PÁGINA CUESTIONARIO -------------###
st.title("Cuestionario para Selección de Proveedor de Nube")
st.markdown("Enfoque en confidencialidad.")

res = {}

# Sección: Máquinas Virtuales
with st.expander("Máquinas Virtuales"):
    res["mv_requiere"] = st.radio("¿Requiere el uso de Máquinas Virtuales (MV)?", ["Seleccionar...", "Sí", "No"])
    
    if res["mv_requiere"] == "Sí":
        res["mv_tipo"] = st.selectbox("¿Qué tipo de MV necesita?", [
            "Seleccionar...", "Propósito general", "Optimización de memoria", "Optimización de CPU",
            "Aceleradas por GPU", "Optimización de almacenamiento"])

        res["mv_so_multiple"] = st.radio("¿Requiere soporte para múltiples Sistemas Operativos?", ["Seleccionar...", "Sí", "No"])

        if res["mv_so_multiple"] == "Sí":
            res["mv_sistemas"] = st.multiselect("Elegir Sistema Operativo", ["Linux", "Windows", "MacOs"])
        elif res["mv_so_multiple"] == "No":
            so_unico = st.selectbox("Elegir Sistema Operativo", ["Seleccionar...", "Linux", "Windows", "MacOs"])
            res["mv_sistemas"] = [so_unico] if so_unico != "Seleccionar..." else []

        if res.get("mv_sistemas"):
            res["mv_escalamiento_predictivo"] = st.radio("¿Requiere escalamiento predictivo?", ["Seleccionar...", "Sí", "No"])
            res["mv_autoescalamiento"] = st.radio("¿Requiere auto-escalamiento?", ["Seleccionar...", "Sí", "No"])
            res["mv_hibernacion"] = st.radio("¿Requiere hibernación o suspensión de MV?", ["Seleccionar...", "Sí", "No"])

# Sección: Contenedores
with st.expander("Contenedores"):
    res["contenedores"] = st.radio("¿Su proyecto requiere el uso de Kubernetes o contenedores?", ["Seleccionar...","Sí", "No"])

# Sección: Almacenamiento
with st.expander("Almacenamiento"):
    res["almacenamiento"] = st.selectbox("¿Qué tipo de almacenamiento necesita?", [
           "Seleccionar...", "Objetos", "Bloques", "Archivos", "Ninguno"])
    

# Sección: Bases de Datos
with st.expander("Bases de Datos"):
    res["bd_requiere"] = st.radio("¿Requiere Bases de Datos (BD)?", ["Seleccionar...","Sí", "No"])
    if res["bd_requiere"] == "Sí":
        res["bd_tipo"] = st.radio("¿Qué tipo de BD necesita?", ["Seleccionar...","Relacional", "No relacional"])
        if res["bd_tipo"] == "Relacional":
            res["bd_motor"] = st.selectbox("¿Qué motor de BD relacional prefiere?", ["Seleccionar...","MySQL", "PostgreSQL", "MariaDB", "SQL Server", "Oracle"])
            res["bd_escalabilidad_rel"] = st.radio("¿Qué tipo de escalabilidad prefiere?", ["Seleccionar...","Vertical", "Horizontal", "Ninguna"])
        else:
            res["bd_escalabilidad_no_rel"] = st.radio("¿Qué tipo de escalabilidad necesita?", [
                "Seleccionar...","Escalabilidad automática con ajuste de capacidad",
                "Escalabilidad automática con réplicas de lectura",
                "Escalabilidad horizontal con fragmentación automática",
                "Ninguna"])

# Sección: IA 
with st.expander("Inteligencia Artificial"):
    res["ia_requiere"] = st.radio("¿Requiere servicios de Inteligencia Artificial ?", ["Seleccionar...","Sí", "No"])
    if res["ia_requiere"] == "Sí":
        res["ia_tipo"] = st.radio("¿Qué tipo de servicio IA necesita?", ["Seleccionar...","Uso general", "Especializado"])
        if res["ia_tipo"] == "Especializado":
            res["ia_servicios_especializados"] = st.selectbox("Seleccione los servicios especializados", [
                "Seleccionar...","Reconocimiento de voz", "Convertir Texto a Voz", "Visión",
                "Procesamiento de lenguaje natural", "Traducción"])
            if "Reconocimiento de voz" in res["ia_servicios_especializados"]:
                res["voz_idiomas"] = st.radio("¿Requiere soporte para más idiomas además del inglés?", ["Seleccionar...","Sí", "No"])
            if "Convertir Texto a Voz" in res["ia_servicios_especializados"]:
                res["voz_clonacion"] = st.radio("¿Requiere clonación de voz?", ["Seleccionar...","Sí", "No"])
                if res["voz_clonacion"] == "Sí":
                    res["voz_naturalidad"] = st.radio("¿Qué tipo de voz prefiere?", ["Seleccionar...","Muy natural", "Medianamente natural", "Poco natural"])
            if "Visión" in res["ia_servicios_especializados"]:
                res["vision_lugares"] = st.radio("¿Requiere reconocimiento de lugares emblemáticos?", ["Seleccionar...","Sí", "No"])
                res["vision_celebridades"] = st.radio("¿Requiere reconocimiento de celebridades?", ["Seleccionar...","Sí", "No"])
            if "Procesamiento de lenguaje natural" in res["ia_servicios_especializados"]:
                res["pln_analisis"] = st.radio("¿Requiere análisis avanzado de texto?", ["Seleccionar...","Sí", "No"])
            if "Traducción" in res["ia_servicios_especializados"]:
                res["traduccion_personalizada"] = st.radio("¿Requiere modelos personalizados?", ["Seleccionar...","Sí", "No"])
        
# Sección: Web Scraping
with st.expander("Web Scraping"):
    res["scraping"] = st.radio("¿Requiere scraping web?", ["Seleccionar...","Sí", "No"])
    
# Sección: Prioridades del proyecto
with st.expander(" Prioridades del Proyecto"):
    st.text("Considera 1= Bajo y 5 = Alto")
    res["presupuesto"] = st.slider("¿Cuál es el presupuesto del proyecto?", 1, 5, 3)
    res["disponibilidad"] = st.slider("Nivel de disponibilidad deseado", 1, 5, 3)
    res["confidencialidad"] = st.slider("Nivel de confidencialidad deseado", 1, 5, 3)

# Evaluación
st.markdown("---")
st.subheader("Resultado del Cuestionario")
if st.button("Ver recomendaciones"):
    campos_incompletos = any(v in ["Seleccionar...", "", None, []] for v in res.values())
    if campos_incompletos:
        st.error("Debe responder todas las preguntas antes de continuar.")
        st.stop()
    scores, razones = evaluar_respuestas(res)
    max_puntaje = max(scores.values())
    ganadores = [p for p, pts in scores.items() if pts == max_puntaje]

    if len(ganadores) == 1:
        st.success(f"✅ El proveedor más recomendado es: **{ganadores[0]}** con {max_puntaje} puntos.")
    else:
        st.warning("🤝 Empate entre los siguientes proveedores:")
        for g in ganadores:
            st.markdown(f"- **{g}** ({max_puntaje} puntos)")

    st.write("### Puntos por proveedor")
    for p in scores:
        st.markdown(f"- **{p}**: {scores[p]} puntos")

    st.write("### Justificación de los puntajes")
    cols = st.columns(3)
    for i, p in enumerate(PROVEEDORES := ["AWS", "GCP", "Azure"]):
        with cols[i]:
            st.markdown(f"#### {p}")
            for r in razones[p]:
                st.markdown(f"- {r}")

    
    # PDF
    # PDF Mejorado
    from fpdf import FPDF
    from datetime import datetime
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Guía de recomendaciones para la selección de proveedor en la nube", ln=True)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Resumen de elecciones del usuario", ln=True)
    pdf.set_font("Arial", "", 10)
    for k, v in res.items():
        if isinstance(v, list):
            v = ', '.join(v)
        elif v is None:
            v = "No especificado"
        pdf.multi_cell(0, 6, f"- {k.replace('_', ' ').capitalize()}: {v}")
    pdf.ln(5)

    ordenados = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    ganador = ordenados[0][0]

    for proveedor, puntaje in ordenados:
        if proveedor == ganador:
            pdf.set_font("Arial", "B", 12)
            pdf.set_text_color(0, 102, 0)  # Verde para el ganador
            pdf.cell(0, 10, f"Proveedor recomendado: {proveedor} ({puntaje} puntos)", ln=True)
        else:
            pdf.set_font("Arial", "B", 12)
            pdf.set_text_color(0, 0, 128)  # Azul para alternativos
            pdf.cell(0, 10, f"Alternativa: {proveedor} ({puntaje} puntos)", ln=True)

        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", "", 10)
        for r in razones[proveedor]:
            pdf.multi_cell(0, 6, f"- {r}")

        servicios_obtenidos = obtener_servicios_relevantes(res, proveedor)
        if proveedor == "AWS" and "MacOs" in res.get("mv_sistemas", []):
            servicios_filtrados = [
                s for s in servicios_obtenidos
                if s.get("tipo") != "Propósito general" or "mac" in s.get("nombre", "").lower()
            ]
        else:
            servicios_filtrados = servicios_obtenidos

        if servicios_filtrados:
            pdf.set_font("Arial", "B", 11)
            pdf.cell(0, 8, "Servicios sugeridos:", ln=True)
            pdf.set_font("Arial", "", 9)
            nombres_vistos = set()
            for s in servicios_filtrados:
                if s['nombre'] in nombres_vistos:
                    continue
                nombres_vistos.add(s['nombre'])
                pdf.multi_cell(0, 6, f"Servicio: {s['nombre']}")
                if "funcionalidades" in s:
                    pdf.multi_cell(0, 6, f"Funcionalidades cubiertas: {s['funcionalidades']}")
                if "regiones_disponibles" in s:
                    regiones = ', '.join(s['regiones_disponibles'])
                    pdf.multi_cell(0, 6, f"Región sugerida: {regiones}")
                if "configuraciones" in s:
                    pdf.multi_cell(0, 6, f"Configuraciones: {s['configuraciones']}")
                if "confidencialidad" in s:
                    pdf.multi_cell(0, 6, f"Cumple Confidencialidad/Integridad: {s['confidencialidad']}")
                if "costo_aproximado" in s:
                    pdf.multi_cell(0, 6, f"Costo mínimo estimado: {s['costo_aproximado']}")
                pdf.ln(1)
        pdf.ln(5)

    from datetime import datetime
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    pdf_output = f"Reporte_de_recomendaciones_{fecha_actual}.pdf"
    #pdf_output = "reporte_final_recomendacion.pdf"
    pdf.output(pdf_output)
    with open(pdf_output, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{pdf_output}">📄 Descargar PDF Final</a>'
        st.markdown(href, unsafe_allow_html=True)
    

