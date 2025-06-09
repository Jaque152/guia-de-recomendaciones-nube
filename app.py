    #    ##---FRONT-Streamlit---##
import streamlit as st
from logica_cuestionario import evaluar_respuestas
from logica_cuestionario import obtener_servicios_relevantes
from fpdf import FPDF
import base64
from fpdf import FPDF
from datetime import datetime

st.set_page_config(page_title="Guía de recomendaciones para la selección de proveedor de servicios en la nube”", layout="centered")
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
    youtube_url = "https://www.youtube.com/watch?v=TU_VIDEO_ID"
    col2.markdown(
        f'''
        <a href="{youtube_url}" target="_blank">
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


#st.write(f"Ha elegido **{st.session_state.enfoque_seguridad}** como enfoque de seguridad.")
##----------------------------------------##

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
st.title("Guía de recomendaciones para la selección de proveedor de servicios en la nube")
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
            res["mv_escalamiento_predictivo"] = st.radio(
                "¿Requiere escalamiento predictivo?", 
                ["Seleccionar...", "Sí", "No"],
                help="El sistema anticipa patrones de uso mediante aprendizaje automático o análisis histórico y ajusta los recursos antes de que se necesiten, evitando latencia o caídas por picos de carga"
            )
            res["mv_autoescalamiento"] = st.radio(
                "¿Requiere auto-escalamiento?", 
                ["Seleccionar...", "Sí", "No"],
                help="Permite que el sistema agregue o elimine recursos automáticamente según la carga real."
            )
            res["mv_hibernacion"] = st.radio(
                "¿Requiere hibernación o suspensión de MV?", 
                ["Seleccionar...", "Sí", "No"],
                help="Permite pausar temporalmente una máquina virtual (MV) conservando su estado en disco (RAM, procesos), para poder reanudarla más tarde exactamente donde se detuvo."
            )

# Sección: Contenedores
with st.expander("Contenedores"):
    res["contenedores"] = st.radio("¿Su proyecto requiere el uso de Kubernetes o contenedores?", ["Seleccionar...","Sí", "No"])

# Sección: Almacenamiento
with st.expander("Almacenamiento"):
    res["almacenamiento"] = st.selectbox("¿Qué tipo de almacenamiento necesita?", [
           "Seleccionar...", "Objetos", "Bloques", "Archivos", "Ninguno"])
    

# Sección: Bases de Datos
# Sección: Bases de Datos
with st.expander("Bases de Datos"):
    res["bd_requiere"] = st.radio("¿Requiere Bases de Datos (BD)?", ["Seleccionar...", "Sí", "No"])
    if res["bd_requiere"] == "Sí":
        res["bd_tipo"] = st.radio("¿Qué tipo de BD necesita?", ["Seleccionar...", "Relacional", "No relacional"])
        
        if res["bd_tipo"] == "Relacional":
            res["bd_motor"] = st.selectbox(
                "¿Qué motor de BD relacional prefiere?",
                ["Seleccionar...", "MySQL", "PostgreSQL", "MariaDB", "SQL Server", "Oracle"]
            )
            res["bd_escalabilidad_rel"] = st.radio(
                "¿Qué tipo de escalabilidad prefiere?",
                ["Seleccionar...", "Vertical", "Horizontal", "Ninguna"],
                help="#Escalabilidad Vertical:capacidad de aumentar la potencia de un único servidor o nodo, añadiendo recursos como CPU, memoria RAM o almacenamiento para que esa misma máquina procese una carga mayor. #Escalabilidad Horizontal: consiste en añadir más servidores o instancias idénticas para repartir la carga de trabajo entre múltiples nodos"
            )

        elif res["bd_tipo"] == "No relacional":
            res["bd_escalabilidad_no_rel"] = st.radio(
                "¿Qué tipo de escalabilidad necesita?",
                [
                    "Seleccionar...",
                    "Escalabilidad automática con ajuste de capacidad",
                    "Escalabilidad automática con réplicas de lectura",
                    "Escalabilidad horizontal con fragmentación automática",
                    "Ninguna"
                ],
                help=(
                    "#Escalabilidad automática con ajuste de capacidad: "
                    "El sistema ajusta dinámicamente la capacidad según la carga, sin necesidad de reinicio.\n"
                    "#Escalabilidad automática con réplicas de lectura: "
                    "Se crean réplicas distribuidas que solo procesan lecturas, para mejorar el rendimiento en escenarios con muchas consultas.\n"
                    "#Escalabilidad horizontal con fragmentación automática: "
                    "El sistema divide los datos en fragmentos y los distribuye entre múltiples nodos. "
                    "Esto permite escalar horizontalmente sin intervención."
                )
            )


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

# Sección: Enfoque de Seguridad
with st.expander("Seguridad"):
    st.text("Considera 1= Bajo y 5 = Alto")
    res["enfoque_seguridad"] = st.selectbox("¿Qué enfoque de seguridad prefiere?", ["Seleccionar...", "Confidencialidad", "Integridad", "Ambos"])
    if res["enfoque_seguridad"] in ["Confidencialidad", "Ambos"]:
        res["confidencialidad"] = st.slider("Nivel de confidencialidad deseado", 1, 5, 3, key="confidencialidad_slider")
    if res["enfoque_seguridad"] in ["Integridad", "Ambos"]:
        res["integridad"] = st.slider("Nivel de integridad deseado", 1, 5, 3,key="integridad_slider" )
# Sección: Prioridades del proyecto
with st.expander(" Prioridades del Proyecto"):
    st.text("Considera 1= Bajo y 5 = Alto")
    res["costo"] = st.slider("¿Cuál es el nivel de costo del proyecto?", 1, 5, 3)
    res["disponibilidad"] = st.slider("Nivel de disponibilidad deseado", 1, 5, 3)

# Evaluación
st.markdown("---")
st.subheader("Resultado del Cuestionario")
if st.button("Ver recomendaciones"):
    campos_incompletos = any(v in ["Seleccionar...", "", None, []] for v in res.values())
    if campos_incompletos:
        st.error("Debe responder todas las preguntas antes de continuar.")
        st.stop()
    scores, razones, res_modificado = evaluar_respuestas(res)
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
    # PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Guía de recomendaciones para la selección de proveedor en la nube", ln=True)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Resumen de elecciones del usuario", ln=True)
    pdf.set_font("Arial", "", 10)
    
    pdf.multi_cell(0, 6, f"- Enfoque de seguridad: {res_modificado.get('enfoque_seguridad', 'No especificado')}")
    pdf.multi_cell(0, 6, f"- Nivel de Confidencialidad: {res_modificado.get('confidencialidad_texto', 'No especificado')}")
    pdf.multi_cell(0, 6, f"- Nivel de Integridad: {res_modificado.get('integridad_texto', 'No especificado')}")
    pdf.multi_cell(0, 6, f"- Máquinas Virtuales: {res_modificado.get('mv_requiere', 'No especificado')}")
    if res_modificado.get("mv_requiere") == "Sí":
        pdf.multi_cell(0, 6, f"    - Tipo: {res_modificado.get('mv_tipo', '-')}")
        pdf.multi_cell(0, 6, f"    - SO: {', '.join(res_modificado.get('mv_sistemas', []))}")
    pdf.multi_cell(0, 6, f"- Contenedores: {res_modificado.get('contenedores', 'No especificado')}")
    pdf.multi_cell(0, 6, f"- Almacenamiento: {res_modificado.get('almacenamiento', 'No especificado')}")
    pdf.multi_cell(0, 6, f"- Bases de Datos: {res_modificado.get('bd_requiere', 'No especificado')}")
    if res_modificado.get("bd_requiere") == "Sí":
        pdf.multi_cell(0, 6, f"    - Tipo: {res_modificado.get('bd_tipo', '-')}")
        if res_modificado.get("bd_tipo") == "Relacional":
            pdf.multi_cell(0, 6, f"    - Motor: {res_modificado.get('bd_motor', '-')}")
    pdf.multi_cell(0, 6, f"- Servicios de IA requeridos: {res_modificado.get('ia_tipo', 'No especificado')}")
    pdf.multi_cell(0, 6, f"- Web Scraping: {res_modificado.get('scraping', 'No especificado')}")
    pdf.multi_cell(0, 6, f"- Presupuesto (Costo): {res_modificado.get('costo_texto', 'No especificado')}")
    pdf.multi_cell(0, 6, f"- Nivel de disponibilidad deseado: {res_modificado.get('disponibilidad_texto', 'No especificado')}")
    pdf.ln(5)

    ordenados = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    max_puntaje = ordenados[0][1]
    ganadores = [p for p, v in scores.items() if v == max_puntaje]

    for proveedor, puntaje in ordenados:
        pdf.set_font("Arial", "B", 12)
        if proveedor in ganadores and len(ganadores) == 1:
            pdf.set_text_color(0, 102, 0)  # Verde para el único ganador
            pdf.cell(0, 10, f"Proveedor recomendado: {proveedor} ({puntaje} puntos)", ln=True)
        elif proveedor in ganadores:
            pdf.set_text_color(0, 102, 102)  # Color distinto para empate
            pdf.cell(0, 10, f"Empate - Opción válida: {proveedor} ({puntaje} puntos)", ln=True)
        else:
            pdf.set_text_color(0, 0, 128)
            pdf.cell(0, 10, f"Alternativa: {proveedor} ({puntaje} puntos)", ln=True)
        
        # Restablece el color y la fuente para las razones
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", "", 10)
        
        for r in razones[proveedor]:
            pdf.multi_cell(0, 6, f"- {r}")

        
        servicios_obtenidos = obtener_servicios_relevantes(res_modificado, proveedor)
        
        if servicios_obtenidos:
            pdf.set_font("Arial", "B", 11)
            pdf.cell(0, 8, "Servicios sugeridos:", ln=True)
            pdf.set_font("Arial", "", 9)
            nombres_vistos = set()
            
            # El bucle ahora usa la lista completa 'servicios_obtenidos'.
            for s in servicios_obtenidos:
                if s['nombre'] in nombres_vistos:
                    continue
                # Usa res_modificado para las comprobaciones
                if "mac" in s.get("nombre", "").lower() and "MacOs" not in res_modificado.get("mv_sistemas", []):
                    continue
                nombres_vistos.add(s['nombre'])
                pdf.set_font("Arial", "B", 9)
                pdf.multi_cell(0, 6, f"Servicio: {s['nombre']}")
                
                # Restablece la fuente para los detalles
                pdf.set_font("Arial", "", 9)

                if "funcionalidades" in s:
                    pdf.multi_cell(0, 6, f"Funcionalidades cubiertas: {s['funcionalidades']}")
                if "regiones_disponibles" in s:
                    regiones = ', '.join(s['regiones_disponibles'])
                    pdf.multi_cell(0, 6, f"Región sugerida: {regiones}")
                if "configuraciones" in s:
                    pdf.multi_cell(0, 6, f"Configuraciones: {s['configuraciones']}")
                
                # Lógica correcta para mostrar características de seguridad
                # Se comprueba para CADA servicio si debe mostrar la sección
                if res_modificado.get("enfoque_seguridad") in ["Confidencialidad", "Ambos"]:
                    if "caracteristicas_confidencialidad" in s:
                        pdf.set_font("Arial", "B", 9)
                        pdf.multi_cell(0, 6, "Características de Confidencialidad:")
                        pdf.set_font("Arial", "", 9)
                        for c in s["caracteristicas_confidencialidad"]:
                            pdf.multi_cell(0, 6, f"  - {c}")

                if res_modificado.get("enfoque_seguridad") in ["Integridad", "Ambos"]:
                    if "caracteristicas_integridad" in s:
                        pdf.set_font("Arial", "B", 9)
                        pdf.multi_cell(0, 6, "Características de Integridad:")
                        pdf.set_font("Arial", "", 9)
                        for c in s["caracteristicas_integridad"]:
                            pdf.multi_cell(0, 6, f"  - {c}")
                
                if "costo_aproximado" in s:
                    pdf.set_font("Arial", "B", 9)
                    pdf.multi_cell(0, 6, "Costo mínimo estimado:")
                    pdf.set_font("Arial", "", 9)
                    costo = s["costo_aproximado"]
                    if isinstance(costo, list):
                        for c in costo:
                            pdf.multi_cell(0, 6, f"  - {c}")
                    else:
                        pdf.multi_cell(0, 6, f"  {costo}")
        pdf.ln(5)

    from datetime import datetime
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    pdf_output = f"Reporte_de_recomendaciones_{fecha_actual}.pdf"
    #pdf_output = "reporte_final_recomendacion.pdf"
    pdf.output(pdf_output)
    with open(pdf_output, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{pdf_output}">📄 Descargar PDF con recomendaciones</a>'
        st.markdown(href, unsafe_allow_html=True)
    

