#    ##---FRONT-Streamlit---##
import streamlit as st
from logica_cuestionario import evaluar_respuestas
from logica_cuestionario import obtener_servicios_relevantes, obtener_nivel_confidencialidad
from fpdf import FPDF
import base64
from datetime import datetime
import traceback

st.set_page_config(page_title="Guía de recomendaciones para la selección de proveedor de servicios en la nube", layout="centered")

# Lista de proveedores 
PROVEEDORES = ["AWS", "GCP", "Azure"]

#---------- PANTALLA DE INICIO -----------##
if "cuestionario_iniciado" not in st.session_state:
    st.session_state.cuestionario_iniciado = False
    st.session_state.enfoque_seguridad = None


if not st.session_state.cuestionario_iniciado:
    st.title("Guía de recomendaciones para la selección de proveedor de servicios en la nube")
    st.markdown("""
    Esta herramienta sirve como guía para elegir el proveedor que mejor se adapte a las necesidades del proyecto.
    - Almacenamiento
    - Bases de datos
    - Inteligencia Artificial
    - Scraping
    
    ### Elija un enfoque de seguridad:
    """)

    col1, col2 = st.columns(2)
    # Botón para Confidencialidad -> inicia cuestionario
    if col1.button("Confidencialidad"):
        st.session_state.enfoque_seguridad = "Confidencialidad"
        st.session_state.cuestionario_iniciado = True

    # Enlace HTML para Integridad -> abre nueva pestaña
    integridad_url = "https://guia-cloud-herramienta.streamlit.app/"
    col2.markdown(
        f'''
        <a href="{integridad_url}">
            <button style="
                background-color: #f44336;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                cursor: pointer;
            ">
                Integridad
            </button>
        </a>
        ''',
        unsafe_allow_html=True
    )
    st.stop()

##----------------------------------------##

####--------PÁGINA CUESTIONARIO -------------###
st.title("Guía de recomendaciones para la selección de proveedor de servicios en la nube")
st.markdown("Por favor, complete el siguiente cuestionario para recibir una recomendación personalizada.")

# Diccionario para almacenar las respuestas del usuario
res = {
    "mv_requiere": "Seleccionar...", "mv_tipo": "Seleccionar...", "mv_so_multiple": "Seleccionar...", "mv_sistemas": [], 
    "mv_escalamiento_predictivo": "Seleccionar...", "mv_autoescalamiento": "Seleccionar...", "mv_hibernacion": "Seleccionar...",
    "contenedores": "Seleccionar...", "almacenamiento": "Seleccionar...", "bd_requiere": "Seleccionar...",
    "bd_tipo": "Seleccionar...", "bd_motor": "Seleccionar...", "bd_escalabilidad_rel": "Seleccionar...",
    "bd_escalabilidad_no_rel": "Seleccionar...", "ia_requiere": "Seleccionar...", "ia_tipo": "Seleccionar...",
    "ia_servicios_especializados": [], "voz_idiomas": "Seleccionar...", "voz_clonacion": "Seleccionar...",
    "voz_naturalidad": "Seleccionar...", "vision_lugares": "Seleccionar...", "vision_celebridades": "Seleccionar...",
    "pln_analisis": "Seleccionar...", "traduccion_personalizada": "Seleccionar...", "scraping": "Seleccionar...",
    "enfoque_seguridad": "Seleccionar...", 
    "confidencialidad": 3, "confidencialidad_texto": "Media", "integridad": 3, "integridad_texto": "Medio",
    "costo": 3, "costo_texto": "Medio", "disponibilidad": 3, "disponibilidad_texto": "Media"
}

# --- Cuestionario ---
with st.expander("Máquinas Virtuales"):
    res["mv_requiere"] = st.radio("¿Requiere el uso de Máquinas Virtuales (MV)?", ["Seleccionar...", "Sí", "No"], key="mv_req")
    if res["mv_requiere"] == "Sí":
        res["mv_tipo"] = st.selectbox("¿Qué tipo de MV necesita?", ["Seleccionar...", "Propósito general", "Optimización de memoria", "Optimización de CPU", "Aceleradas por GPU", "Optimización de almacenamiento"], key="mv_tipo")
        res["mv_so_multiple"] = st.radio("¿Requiere soporte para múltiples Sistemas Operativos?", ["Seleccionar...", "Sí", "No"], key="mv_so_multiple")
        if res["mv_so_multiple"] == "Sí":
            res["mv_sistemas"] = st.multiselect("Elegir Sistema Operativo", ["Linux", "Windows", "MacOs"], key="mv_sistemas_multi")
        elif res["mv_so_multiple"] == "No":
            so_unico = st.selectbox("Elegir Sistema Operativo", ["Seleccionar...", "Linux", "Windows", "MacOs"], key="mv_sistemas_single")
            res["mv_sistemas"] = [so_unico] if so_unico != "Seleccionar..." else []
        if res["mv_sistemas"]:
            res["mv_escalamiento_predictivo"] = st.radio("¿Requiere escalamiento predictivo?", ["Seleccionar...", "Sí", "No"], key="mv_escalamiento_predictivo")
            res["mv_autoescalamiento"] = st.radio("¿Requiere auto-escalamiento?", ["Seleccionar...", "Sí", "No"], key="mv_autoescalamiento")
            res["mv_hibernacion"] = st.radio("¿Requiere hibernación o suspensión de MV?", ["Seleccionar...", "Sí", "No"], key="mv_hibernacion")

with st.expander("Contenedores"):
    res["contenedores"] = st.radio("¿Su proyecto requiere el uso de Kubernetes o contenedores?", ["Seleccionar...","Sí", "No"], key="contenedores")

with st.expander("Almacenamiento"):
    res["almacenamiento"] = st.selectbox("¿Qué tipo de almacenamiento necesita?", ["Seleccionar...", "Objetos", "Bloques", "Archivos", "Ninguno"], key="almacenamiento")
    
with st.expander("Bases de Datos"):
    res["bd_requiere"] = st.radio("¿Requiere Bases de Datos (BD)?", ["Seleccionar...", "Sí", "No"], key="bd_requiere")
    if res["bd_requiere"] == "Sí":
        res["bd_tipo"] = st.radio("¿Qué tipo de BD necesita?", ["Seleccionar...", "Relacional", "No relacional"], key="bd_tipo")
        if res["bd_tipo"] == "Relacional":
            res["bd_motor"] = st.selectbox("¿Qué motor de BD relacional prefiere?", ["Seleccionar...", "MySQL", "PostgreSQL", "MariaDB", "SQL Server", "Oracle"], key="bd_motor")
            res["bd_escalabilidad_rel"] = st.radio("¿Qué tipo de escalabilidad prefiere?", ["Seleccionar...", "Vertical", "Horizontal", "Ninguna"], key="bd_escalabilidad_rel")
        elif res["bd_tipo"] == "No relacional":
            res["bd_escalabilidad_no_rel"] = st.radio("¿Qué tipo de escalabilidad necesita?", ["Seleccionar...", "Escalabilidad automática con ajuste de capacidad", "Escalabilidad automática con réplicas de lectura", "Escalabilidad horizontal con fragmentación automática", "Ninguna"], key="bd_escalabilidad_no_rel")

with st.expander("Inteligencia Artificial"):
    res["ia_requiere"] = st.radio("¿Requiere servicios de Inteligencia Artificial ?", ["Seleccionar...","Sí", "No"], key="ia_requiere")
    if res["ia_requiere"] == "Sí":
        res["ia_tipo"] = st.radio("¿Qué tipo de servicio IA necesita?", ["Seleccionar...","Uso general", "Especializado"], key="ia_tipo")
        if res["ia_tipo"] == "Especializado":
            res["ia_servicios_especializados"] = st.multiselect("Seleccione los servicios especializados", ["Reconocimiento de voz", "Convertir Texto a Voz", "Visión", "Procesamiento de lenguaje natural", "Traducción"], key="ia_servicios_especializados_sel")
            if "Reconocimiento de voz" in res["ia_servicios_especializados"]:
                res["voz_idiomas"] = st.radio("¿Requiere soporte para más idiomas además del inglés?", ["Seleccionar...","Sí", "No"], key="voz_idiomas")
            if "Convertir Texto a Voz" in res["ia_servicios_especializados"]:
                res["voz_clonacion"] = st.radio("¿Requiere clonación de voz?", ["Seleccionar...","Sí", "No"], key="voz_clonacion")
                if res["voz_clonacion"] == "Sí":
                    res["voz_naturalidad"] = st.radio("¿Qué tipo de voz prefiere?", ["Seleccionar...","Muy natural", "Medianamente natural", "Poco natural"], key="voz_naturalidad")
            if "Visión" in res["ia_servicios_especializados"]:
                res["vision_lugares"] = st.radio("¿Requiere reconocimiento de lugares emblemáticos?", ["Seleccionar...","Sí", "No"], key="vision_lugares")
                res["vision_celebridades"] = st.radio("¿Requiere reconocimiento de celebridades?", ["Seleccionar...","Sí", "No"], key="vision_celebridades")
            if "Procesamiento de lenguaje natural" in res["ia_servicios_especializados"]:
                res["pln_analisis"] = st.radio("¿Requiere análisis avanzado de texto?", ["Seleccionar...","Sí", "No"], key="pln_analisis")
            if "Traducción" in res["ia_servicios_especializados"]:
                res["traduccion_personalizada"] = st.radio("¿Requiere modelos personalizados?", ["Seleccionar...","Sí", "No"], key="traduccion_personalizada")

with st.expander("Web Scraping"):
    res["scraping"] = st.radio("¿Requiere scraping web?", ["Seleccionar...","Sí", "No"], key="scraping")

## FIX: La sección de seguridad ahora contiene la pregunta principal sobre el enfoque.
with st.expander("Seguridad"):
    res["enfoque_seguridad"] = st.radio(
        "¿Cuál es el enfoque principal de seguridad para su proyecto?",
        ["Seleccionar...", "Confidencialidad", "Integridad", "Ambos"],
        key="enfoque_seguridad_choice"
    )

    if res["enfoque_seguridad"] in ["Confidencialidad", "Ambos"]:
        res["confidencialidad"] = st.slider("Nivel de confidencialidad deseado (1=Muy bajo, 5=Muy alto):", 1, 5, 3, key="peso_confidencialidad_slider")
        res["confidencialidad_texto"] = {1: "Muy baja", 2: "Baja", 3: "Media", 4: "Alta", 5: "Muy alta"}.get(res["confidencialidad"])
    else:
        res["confidencialidad"] = 0 
        res["confidencialidad_texto"] = "No aplica"

    if res["enfoque_seguridad"] in ["Integridad", "Ambos"]:
        res["integridad"] = st.slider("Nivel de integridad deseado (1=Muy bajo, 5=Muy alto):", 1, 5, 3, key="peso_integridad_slider")
        res["integridad_texto"] = "Medio"
        if res["integridad"] in [1, 2]: res["integridad_texto"] = "Bajo"
        if res["integridad"] in [4, 5]: res["integridad_texto"] = "Alto"
    else:
        res["integridad"] = 0 
        res["integridad_texto"] = "No aplica"

with st.expander("Prioridades del Proyecto"):
    res["costo"] = st.slider("Nivel de costo deseado (1= Bajo, 5= Alto):", 1, 5, 3, key="peso_costo_slider")
    res["costo_texto"] = "Medio"
    if res["costo"] in [1, 2]: res["costo_texto"] = "Bajo"
    if res["costo"] in [4, 5]: res["costo_texto"] = "Alto"

    res["disponibilidad"] = st.slider("Nivel de disponibilidad deseado (1= Bajo, 5= Alto):", 1, 5, 3, key="peso_disponibilidad_slider")
    res["disponibilidad_texto"] = "Media"
    if res["disponibilidad"] in [1, 2]: res["disponibilidad_texto"] = "Baja"
    if res["disponibilidad"] in [4, 5]: res["disponibilidad_texto"] = "Alta"
# --- Botón de Evaluación ---
st.markdown("---")
st.subheader("Resultado del Cuestionario")
if st.button("Ver recomendaciones"):
    try:
        # 1) Validaciones de campos obligatorios
        errores = []
        if res.get("enfoque_seguridad") == "Seleccionar...": errores.append("Enfoque de seguridad")
        if res.get("mv_requiere") == "Seleccionar...": errores.append("Máquinas Virtuales")
        if res.get("contenedores") == "Seleccionar...": errores.append("Contenedores")
        if res.get("almacenamiento") == "Seleccionar...": errores.append("Almacenamiento")
        if res.get("bd_requiere") == "Seleccionar...": errores.append("Bases de Datos")
       
        if errores:
            st.error(f"Debe completar todas las preguntas. Por favor, revise: {', '.join(sorted(set(errores)))}.")
            st.stop()

        # 2) Evaluación de respuestas
        puntuaciones, razones = evaluar_respuestas(res)
        max_p = max(puntuaciones.values())
        ganadores = [p for p, pts in puntuaciones.items() if pts == max_p]

        # 3) Mostrar resultado en pantalla
        if len(ganadores) == 1:
            st.success(f"Proveedor recomendado: **{ganadores[0]}** ({max_p:.1f} pts)")
        else:
            st.warning(f"Empate entre proveedores: {', '.join(ganadores)} ({max_p:.1f} pts)")

        # 4) Justificaciones por proveedor
        cols = st.columns(len(PROVEEDORES))
        for i, p in enumerate(PROVEEDORES):
            with cols[i]:
                st.markdown(f"#### {p}")
                if razones.get(p):
                    for r in sorted(set(razones[p])):
                        st.markdown(f"- {r}")
                        # Ocultar todas las líneas de adecuación para no confundir al usuario
                        if "Adecuación" not in r.lower():
                            st.markdown(f"- {r}")
                else:
                    st.markdown("- Sin justificaciones específicas.")

        # 5) Generación de PDF
        orden = sorted(puntuaciones.items(), key=lambda x: x[1], reverse=True)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Guía de recomendaciones para la selección de proveedor en la nube", ln=True, align='C')
        pdf.ln(5)

        # 5.1 Resumen de elecciones del usuario (detallado)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, "Resumen de elecciones del usuario", ln=True)
        pdf.set_font("Arial", "", 10)

        # Seguridad y prioridades
        pdf.cell(0, 6, f"Enfoque de seguridad: {res.get('enfoque_seguridad')}", ln=True)
        pdf.cell(0, 6, f"Nivel de confidencialidad: {res.get('confidencialidad_texto')} ({res.get('confidencialidad')})", ln=True)
        if res.get("enfoque_seguridad") in ["Integridad", "Ambos"]:
            pdf.cell(0, 6, f"Nivel de integridad: {res.get('integridad_texto')} ({res.get('integridad')})", ln=True)
        pdf.cell(0, 6, f"Nivel de costo: {res.get('costo_texto')} ({res.get('costo')})", ln=True)
        pdf.cell(0, 6, f"Nivel de disponibilidad: {res.get('disponibilidad_texto')} ({res.get('disponibilidad')})", ln=True)
        pdf.ln(3)

        # Máquinas Virtuales
        pdf.cell(0, 6, f"Requiere MV: {res.get('mv_requiere')}", ln=True)
        if res.get("mv_requiere") == "Sí":
            pdf.cell(0, 6, f"  - Tipo: {res.get('mv_tipo')}", ln=True)
            sistemas = ", ".join(res.get("mv_sistemas", [])) or "—"
            pdf.cell(0, 6, f"  - S.O.: {sistemas}", ln=True)
            pdf.cell(0, 6, f"  - Escalamiento predictivo: {res.get('mv_escalamiento_predictivo')}", ln=True)
            pdf.cell(0, 6, f"  - Auto-escalamiento: {res.get('mv_autoescalamiento')}", ln=True)
            pdf.cell(0, 6, f"  - Hibernación: {res.get('mv_hibernacion')}", ln=True)
        pdf.ln(2)

        # Contenedores, Almacenamiento, BD, IA, Scraping
        pdf.cell(0, 6, f"Contenedores: {res.get('contenedores')}", ln=True)
        pdf.cell(0, 6, f"Almacenamiento: {res.get('almacenamiento')}", ln=True)

        pdf.cell(0, 6, f"Requiere BD: {res.get('bd_requiere')}", ln=True)
        if res.get("bd_requiere") == "Sí":
            pdf.cell(0, 6, f"  Tipo: {res.get('bd_tipo')}", ln=True)
            if res.get("bd_tipo") == "Relacional":
                pdf.cell(0, 6, f"  Motor: {res.get('bd_motor')}", ln=True)
                pdf.cell(0, 6, f"  Escalabilidad: {res.get('bd_escalabilidad_rel')}", ln=True)
            else:
                pdf.cell(0, 6, f"  Escalabilidad: {res.get('bd_escalabilidad_no_rel')}", ln=True)
        pdf.cell(0, 6, f"IA requerida: {res.get('ia_requiere')}", ln=True)
        if res.get("ia_requiere") == "Sí":
            pdf.cell(0, 6, f"  Tipo: {res.get('ia_tipo')}", ln=True)
            if res.get("ia_tipo") == "Especializado":
                esp = ", ".join(res.get("ia_servicios_especializados", [])) or "—"
                pdf.cell(0, 6, f"  Servicios: {esp}", ln=True)
        pdf.cell(0, 6, f"Web Scraping: {res.get('scraping')}", ln=True)
        pdf.ln(5)

        # 5.2 Proveedor recomendado y alternativas (top 3)
        orden = sorted(puntuaciones.items(), key=lambda x: x[1], reverse=True)

        # 1er lugar
        mejor, pts_mejor = orden[0]
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, f"1° Proveedor recomendado: {mejor} ({pts_mejor:.1f} pts)", ln=True)
        # pdf.set_text_color(0,102,0)
        pdf.set_font("Arial", "", 12)
        for razon in razones.get(mejor, []):
            # pdf.multi_cell(0, 6, f"- {razon}")
            pdf.ln(5)

        # 2° lugar
        if len(orden) > 1:
            alt, pts_alt = orden[1]
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, f"2° Alternativa: {alt} ({pts_alt:.1f} pts)", ln=True)
            pdf.set_font("Arial", "", 12)
            for razon in razones.get(alt, []):
                pdf.multi_cell(0, 6, f"- {razon}")
            pdf.ln(4)

        # 3° lugar
        if len(orden) > 2:
            tercero, pts_tercero = orden[2]
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, f"3° Opción adicional: {tercero} ({pts_tercero:.1f} pts)", ln=True)
            pdf.set_font("Arial", "", 12)
            for razon in razones.get(tercero, []):
                pdf.multi_cell(0, 6, f"- {razon}")
            pdf.ln(5)
        # 5.3 Detalle de servicios por proveedor
        for prov, _ in orden:
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, f"Detalle de {prov}", ln=True)
            pdf.set_font("Arial", "", 12)
            servicios = obtener_servicios_relevantes(res, prov)
            for s in servicios:
                nombre = s.get("nombre")
                pdf.cell(0, 6, f"Servicio: {nombre}", ln=True)
                niveles, _ = obtener_nivel_confidencialidad(nombre, prov, res.get("confidencialidad"))
                if niveles:
                    pdf.cell(0, 6, "Confidencialidad (reposo):", ln=True)
                    for lvl in niveles:
                        pdf.multi_cell(0, 6, f"  - {lvl['reposo']}")
                costo_approx = s.get("costo_aproximado")
                if costo_approx:
                    txt = "; ".join(costo_approx) if isinstance(costo_approx, list) else costo_approx
                    pdf.cell(0, 6, f"Costo estimado: {txt}", ln=True)
                pdf.ln(3)

        # 5.4 Salida del PDF
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        pdf_output_name = f"Reporte_de_recomendaciones_{fecha_actual}.pdf"
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        b64 = base64.b64encode(pdf_bytes).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{pdf_output_name}">📄 Descargar PDF con recomendaciones</a>'
        st.markdown(href, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Ocurrió un error inesperado al procesar las recomendaciones: {e}")
        st.error(traceback.format_exc())
