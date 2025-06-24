# app.py
import streamlit as st
from logica_cuestionario import (
    evaluar_respuestas,
    evaluar_funcional,
    evaluar_adecuacion,
    obtener_servicios_relevantes,
    obtener_nivel_confidencialidad,
)
from fpdf import FPDF
import base64, json, os, traceback
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Guía de recomendaciones para la selección de proveedor de servicios en la nube",
    layout="centered"
)
PROVEEDORES = ["AWS", "GCP", "Azure"]

# --- Pantalla de inicio ---
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
    if col1.button("Confidencialidad"):
        st.session_state.cuestionario_iniciado = True
        st.session_state.enfoque_seguridad = "Confidencialidad"
    integridad_url = "[https://guia-cloud-herramienta.streamlit.app/](https://guia-cloud-herramienta.streamlit.app/)"
    col2.markdown(
        f'<a href="{integridad_url}" target="_blank" rel="noopener noreferrer"><button style="background-color:#f44336;color:white;padding:8px 16px;border:none;border-radius:4px;cursor:pointer;">Integridad</button></a>',
        unsafe_allow_html=True
    )
    st.stop()

# --- Carga de datos externos (para app.py) ---
_BASE = os.path.dirname(__file__)
try:
    with open(os.path.join(_BASE, "confidencialidad_niveles.json"), encoding="utf-8") as f:
        MATRIZ_CONF = json.load(f)
    with open(os.path.join(_BASE, "servicios.json"), encoding="utf-8") as f:
        SERVICIOS = json.load(f)
except FileNotFoundError:
    st.error("Error: Archivo de configuración no encontrado. Asegúrate de que 'confidencialidad_niveles.json' y 'servicios.json' estén en el mismo directorio.")
    st.stop()
except json.JSONDecodeError:
    st.error("Error: Archivo de configuración inválido. Asegúrate de que 'confidencialidad_niveles.json' y 'servicios.json' sean JSON válidos.")
    st.stop()

defs = {}
for prov in MATRIZ_CONF:
    for e in MATRIZ_CONF[prov]:
        lvl = e["Nivel de confidencialidad"]
        reposo = e.get("Como se cumple para datos en reposo", "")
        trans = e.get("Como se cumple para datos en transito", "")
        defs.setdefault(lvl, set()).update({f"Reposo: {reposo}", f"Tránsito: {trans}"})
defs = {lvl: list(desc) for lvl, desc in defs.items()}

# --- Inicializar respuestas ---
res = {
    "mv_requiere": "Seleccionar...", "mv_tipo": "Seleccionar...", "mv_so_multiple": "Seleccionar...", "mv_sistemas": [],
    "mv_escalamiento_predictivo": "Seleccionar...", "mv_autoescalamiento": "Seleccionar...", "mv_hibernacion": "Seleccionar...",
    "contenedores": "Seleccionar...",
    "almacenamiento": "Seleccionar...",
    "bd_requiere": "Seleccionar...", "bd_tipo": "Seleccionar...", "bd_motor": "Seleccionar...",
    "bd_escalabilidad_rel": "Seleccionar...", "bd_escalabilidad_no_rel": "Seleccionar...",
    "ia_requiere": "Seleccionar...", "ia_tipo": "Seleccionar...", "ia_servicios_especializados": [],
    "voz_idiomas": "Seleccionar...", "voz_clonacion": "Seleccionar...", "voz_naturalidad": "Seleccionar...",
    "vision_lugares": "Seleccionar...", "vision_celebridades": "Seleccionar...",
    "pln_analisis": "Seleccionar...", "traduccion_personalizada": "Seleccionar...",
    "scraping": "Seleccionar...",
    "enfoque_seguridad": "Seleccionar...", "confidencialidad": 3, "confidencialidad_texto": "Media",
    "integridad": 3, "integridad_texto": "Medio", "costo": 3, "costo_texto": "Medio", "disponibilidad": 3, "disponibilidad_texto": "Media"
}

st.title("Guía de recomendaciones para la selección de proveedor de servicios en la nube")
st.markdown("Por favor, complete el siguiente cuestionario para recibir una recomendación personalizada.")

# --- Sección de preguntas ---
with st.expander("Máquinas Virtuales"):
    res["mv_requiere"] = st.radio(
        "¿Requiere el uso de Máquinas Virtuales?", ["Seleccionar...","Sí","No"], key="mv_req"
    )
    if res["mv_requiere"] == "Sí":
        res["mv_tipo"] = st.selectbox(
            "Tipo de MV",
            ["Seleccionar...","Propósito general","Optimización de memoria",
              "Optimización de CPU","Aceleradas por GPU","Optimización de almacenamiento"],
            key="mv_tipo"
        )
        # MODIFICACIÓN: Eliminada la pregunta de SO múltiple, ahora solo multiselect
        res["mv_sistemas"] = st.multiselect(
            "Seleccione los sistemas operativos", 
            ["Linux","Windows","MacOs"], 
            key="mv_sistemas", placeholder="Seleccione una o más opciones"
        )
        # Las siguientes preguntas dependen solo de que se hayan seleccionado SOs, no del tipo de selección
        if res["mv_sistemas"]: # Si se ha seleccionado al menos un SO
            res["mv_escalamiento_predictivo"] = st.radio(
                "¿Escalamiento predictivo?", ["Sí","No"], key="mv_escalamiento_predictivo", 
                help= "El sistema anticipa patrones de uso mediante aprendizaje automático o análisis histórico y ajusta los recursos antes de que se necesiten, evitando latencia o caídas por picos de carga"
            )
            res["mv_autoescalamiento"] = st.radio(
                "¿Requiere auto-escalamiento?", ["Sí","No"], key="mv_autoescalamiento",
                help="Permite que el sistema agregue o elimine recursos automáticamente según la carga real."
            )
            res["mv_hibernacion"] = st.radio(
                "¿Requiere hibernación o suspensión de MV?", ["Sí","No"], key="mv_hibernacion",
                help="Permite pausar temporalmente una máquina virtual (MV) conservando su estado en disco (RAM, procesos), para poder reanudarla más tarde exactamente donde se detuvo."
            )

with st.expander("Contenedores"):
    res["contenedores"] = st.radio(
        "¿Requiere contenedores?", ["Seleccionar...","Sí","No"], key="contenedores"
    )

with st.expander("Almacenamiento"):
    res["almacenamiento"] = st.selectbox(
        "Tipo de almacenamiento", ["Seleccionar...","Objetos","Bloques","Archivos","Ninguno"], key="almacenamiento"
    )

with st.expander("Bases de Datos"):
    res["bd_requiere"] = st.radio(
        "¿Requiere BD?", ["Seleccionar...","Sí","No"], key="bd_requiere"
    )
    if res["bd_requiere"] == "Sí":
        res["bd_tipo"] = st.radio(
            "Tipo de BD", ["Relacional","No relacional"], key="bd_tipo"
        )
        if res["bd_tipo"] == "Relacional":
            res["bd_motor"] = st.selectbox(
                "Motor BD",
                ["MySQL","PostgreSQL","MariaDB","SQL Server","Oracle"], key="bd_motor"
            )
            res["bd_escalabilidad_rel"] = st.radio(
                "Escalabilidad relacional", ["Vertical","Horizontal","Ninguna"], key="bd_escalabilidad_rel"
            )
        else:
            res["bd_escalabilidad_no_rel"] = st.radio(
                "Escalabilidad NoSQL", ["Seleccionar...","Escalabilidad automática con ajuste de capacidad",
                "Escalabilidad automática con réplicas de lectura",
                "Escalabilidad horizontal con fragmentación automática",
                "Ninguna"], key="bd_escalabilidad_no_rel",
                help="#Escalabilidad automática con ajuste de capacidad:El sistema ajusta dinámicamente la capacidad según la carga, sin necesidad de reinicio.#Escalabilidad automática con réplicas de lectura:Se crean réplicas distribuidas que solo procesan lecturas, para mejorar el rendimiento en escenarios con muchas consultas.
                    #Escalabilidad horizontal con fragmentación automática:El sistema divide los datos en fragmentos y los distribuye entre múltiples nodos.Esto permite escalar horizontalmente sin intervención."
            )

with st.expander("Inteligencia Artificial"):
    res["ia_requiere"] = st.radio(
        "¿Requiere IA?", ["Seleccionar...","Sí","No"], key="ia_requiere"
    )
    if res["ia_requiere"] == "Sí":
        res["ia_tipo"] = st.radio(
            "Tipo de servicio IA", ["Uso general","Especializado"], key="ia_tipo"
        )
        if res["ia_tipo"] == "Especializado":
            servicios_ia = st.multiselect(
                "Seleccionar servicios especializados",
                ["Reconocimiento de voz","Convertir Texto a Voz","Visión",
                  "Procesamiento de lenguaje natural","Traducción"], 
                key="ia_servicios_especializados",
                placeholder="Seleccione una o más opciones"
            )
            res["ia_servicios_especializados"] = servicios_ia
            if "Reconocimiento de voz" in servicios_ia:
                res["voz_idiomas"] = st.radio("¿Soporte idiomas adicionales?", ["Sí","No"], key="voz_idiomas")
            if "Convertir Texto a Voz" in servicios_ia:
                res["voz_clonacion"] = st.radio("¿Clonación de voz?", ["Sí","No"], key="voz_clonacion")
                if res["voz_clonacion"] == "Sí":
                    res["voz_naturalidad"] = st.radio("Nivel de naturalidad de voz", ["Muy natural","Mediana","Poca"], key="voz_naturalidad")
            if "Visión" in servicios_ia:
                res["vision_lugares"] = st.radio("¿Reconocimiento de lugares?", ["Sí","No"], key="vision_lugares")
            if "Visión" in servicios_ia: # Mantener esta para la pregunta
                res["vision_celebridades"] = st.radio("¿Reconocimiento de celebridades?", ["Sí","No"], key="vision_celebridades")
            if "Procesamiento de lenguaje natural" in servicios_ia:
                res["pln_analisis"] = st.radio("¿Análisis de texto?", ["Sí","No"], key="pln_analisis")
            if "Traducción" in servicios_ia:
                res["traduccion_personalizada"] = st.radio("¿Modelos personalizados?", ["Sí","No"], key="traduccion_personalizada")

with st.expander("Web Scraping"):
    res["scraping"] = st.radio("¿Requiere scraping web?", ["Seleccionar...","Sí","No"], key="scraping")

# --- Dictionaries for descriptions from tables ---
conf_descriptions = {
    1: "Protección mínima proporcionada por el proveedor. Cifrado del lado del servidor sin cargos adicionales.",
    2: "El usuario gestiona aspectos de seguridad mediante claves, aunque el cifrado lo realiza el proveedor.",
    3: "El usuario proporciona sus propias claves de cifrado (BYOK) y gestiona el control de acceso en una red privada.",
    4: "Cifrado con Módulos de Seguridad de Hardware (HSM) para cumplir regulaciones de alto nivel como FIPS.",
    5: "Los datos se cifran con tecnologías avanzadas (ej. cómputo confidencial) y se incluye cifrado en tránsito."
}

int_descriptions = {
    1: "Uso de Checksums y replicación automática de datos para recuperarse de fallos de hardware.",
    2: "Uso de Checksums y replicación automática de datos para recuperarse de fallos de hardware.",
    3: "Control de versiones y control de accesos para definir quién tiene permiso para editar los datos.",
    4: "Almacenamiento WORM (Write-Once, Read-Many) y ledgers verificables con encadenamiento criptográfico.",
    5: "Almacenamiento WORM (Write-Once, Read-Many) y ledgers verificables con encadenamiento criptográfico."
}

cost_descriptions = {
    1: "Descuentos automáticos y pruebas gratis; para presupuestos ajustados.",
    2: "Descuentos automáticos y pruebas gratis; para presupuestos ajustados.",
    3: "Planes de ahorro, instancias reservadas.",
    4: "Flexibilidad y optimización a escala masiva (el costo no es la principal preocupación).",
    5: "Flexibilidad y optimización a escala masiva (el costo no es la principal preocupación)."
}

disp_descriptions = {
    1: "Alta disponibilidad básica garantizada.",
    2: "Alta disponibilidad básica garantizada.",
    3: "Mayor flexibilidad para arquitecturas de alta disponibilidad.",
    4: "Flexibilidad y optimización a escala masiva para servicios críticos.",
    5: "Flexibilidad y optimización a escala masiva para servicios críticos."
}

# --- Sección de Seguridad ---
with st.expander("Seguridad"):
    res["enfoque_seguridad"] = st.radio(
        "Enfoque de seguridad",
        ["Seleccionar...","Confidencialidad","Integridad","Ambos"], key="enfoque_seguridad"
    )
    if res["enfoque_seguridad"] in ["Confidencialidad","Ambos"]:
        nivel = st.slider("Nivel de confidencialidad (1-5)", 1, 5, 3, key="slider_conf")
        res["confidencialidad"] = nivel
        res["confidencialidad_texto"] = {1:"Muy baja",2:"Baja",3:"Media",4:"Alta",5:"Muy alta"}[nivel]
        
        selected_conf_desc = conf_descriptions.get(nivel, "Descripción no disponible para este nivel.")
        st.info(f"**Nivel {nivel} de Confidencialidad:** {selected_conf_desc}")
        
    else:
        res["confidencialidad"], res["confidencialidad_texto"] = 0, "No aplica"

    if res["enfoque_seguridad"] in ["Integridad","Ambos"]:
        nivel_i = st.slider("Nivel de integridad (1-5)", 1, 5, 3, key="slider_int")
        res["integridad"] = nivel_i
        selected_int_desc = int_descriptions.get(nivel_i, "Descripción no disponible para este nivel.")
        st.warning(f"**Nivel {nivel_i} de Integridad:** {selected_int_desc}")
    else:
        res["integridad"], res["integridad_texto"] = 0, "No aplica"

# --- Sección de Prioridades del Proyecto ---
with st.expander("Prioridades del Proyecto"):
    nivel_c = st.slider("Nivel de costo (1-5)", 1, 5, 3, key="slider_cost")
    res["costo"] = nivel_c
    res["costo_texto"] = "Bajo" if nivel_c<3 else ("Medio" if nivel_c==3 else "Alto")
    selected_cost_desc = cost_descriptions.get(nivel_c, "Descripción no disponible para este nivel.")
    st.info(f"**Nivel {nivel_c} de Costo:** {selected_cost_desc}")

    nivel_d = st.slider("Nivel de disponibilidad (1-5)", 1, 5, 3, key="slider_disp")
    res["disponibilidad"] = nivel_d
    res["disponibilidad_texto"] = "Baja" if nivel_d<3 else ("Medio" if nivel_d==3 else "Alta")
    selected_disp_desc = disp_descriptions.get(nivel_d, "Descripción no disponible para este nivel.")
    st.info(f"**Nivel {nivel_d} de Disponibilidad:** {selected_disp_desc}")


st.markdown("---")
st.subheader("Resultado del Cuestionario y PDF")
if st.button("Ver recomendaciones"):
    try:
        # 1) Validación de campos obligatorios
        campo_nombres = {
            "enfoque_seguridad": "Enfoque de seguridad",
            "mv_requiere": "Máquinas Virtuales",
            "contenedores": "Contenedores",
            "almacenamiento": "Almacenamiento",
            "bd_requiere": "Bases de Datos"
        }
        errores = [campo_nombres[c] for c in campo_nombres if res[c] == "Seleccionar..."]
        if errores:
            st.error(f"Debe completar: {', '.join(errores)}")
            st.stop()

        # 2) Cálculo de adecuación (solo back-end)
        f_scores, f_reasons = evaluar_funcional(res)
        a_scores, a_reasons = evaluar_adecuacion(res)

        # 3) Evaluación final y UI en columnas
        scores, razones = evaluar_respuestas(res)
        f_scores, _ = evaluar_funcional(res)
        orden = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        max_p = orden[0][1]
        ganadores = [p for p, pts in orden if pts == max_p]

        if len(ganadores) == 1:
            st.success(f"Proveedor recomendado: {ganadores[0]} ({max_p:.1f} pts)")
        else:
            st.warning(f"Empate detectado entre: {', '.join(ganadores)} ({max_p:.1f} pts)")
            st.info("💡 **Sugerencia:** Se recomienda reevaluar las prioridades en la sección 'Prioridades del Proyecto' o considerar otros factores cualitativos no medidos por la herramienta (como la experiencia previa del equipo o relaciones comerciales existentes) para tomar una decisión final.")

        cols = st.columns(3)
        for i, prov in enumerate(PROVEEDORES):
            with cols[i]:
                st.markdown(f"### {prov}")
                st.metric("Puntos totales", f"{scores[prov]:.1f}")
                st.metric("Puntos por funcionalidad", f"{f_scores[prov]}")
                st.markdown("**Razones:**")
                for r in razones[prov]:
                    if not r.startswith("¡Advertencia!"):
                        st.write(f"- {r}")
                warns = [w for w in razones[prov] if w.startswith("¡Advertencia!")]
                if warns:
                    st.markdown("**Advertencias:**")
                    for w in warns: st.error(w)
                
                if prov in ganadores:
                    st.markdown("#### Detalles de Servicios Clave:")
                    # MV mapping
                    if res["mv_requiere"] == "Sí":
                        vm_data_list = SERVICIOS[prov].get("mv", [])
                        if not isinstance(vm_data_list, list):
                            vm_data_list = [vm_data_list]
                        
                        selected_vm_name = None
                        selected_vm_family = None 
                        selected_mv_type = res.get("mv_tipo")

                        if selected_mv_type and selected_mv_type != "Seleccionar...":
                            for vm_item in vm_data_list:
                                if vm_item.get("tipo") == selected_mv_type:
                                    selected_vm_name = vm_item.get("nombre")
                                    selected_vm_family = vm_item.get("familia")
                                    break
                        
                        if not selected_vm_name and vm_data_list:
                            for vm_item in vm_data_list:
                                if vm_item.get("tipo") == "Propósito general":
                                    selected_vm_name = vm_item.get("nombre")
                                    selected_vm_family = vm_item.get("familia")
                                    break
                            if not selected_vm_name and vm_data_list:
                                selected_vm_name = vm_data_list[0].get("nombre")
                                selected_vm_family = vm_data_list[0].get("familia")


                        if selected_vm_name:
                            vm_display_text = f"- **{selected_vm_name}**"
                            if selected_vm_family:
                                vm_display_text += f" (Familia: {selected_vm_family})"
                            st.write(vm_display_text)

                            niveles_vm_cumplidos, max_n_vm_disponible = obtener_nivel_confidencialidad(selected_vm_name, prov, res["confidencialidad"] )
                            if niveles_vm_cumplidos:
                                for lvl in niveles_vm_cumplidos:
                                    if lvl['Nivel de confidencialidad'] == 5 and lvl.get('Como se cumple para datos en transito'):
                                        st.write(f"    Nivel {lvl['Nivel de confidencialidad']}: Reposo: {lvl['Como se cumple para datos en reposo']}; Tránsito: {lvl['Como se cumple para datos en transito']}")
                                    else:
                                        st.write(f"    Nivel {lvl['Nivel de confidencialidad']}: Reposo: {lvl['Como se cumple para datos en reposo']}")
                            else:
                                st.info(f"    No se encontraron niveles de confidencialidad para **{selected_vm_name}** que cumplan con el nivel {res['confidencialidad']} (Máx disponible: {max_n_vm_disponible}).")
                        else:
                            st.info(f"    No se pudo determinar el servicio de VM para {prov} basado en el tipo seleccionado.")
                    
                    # Almacenamiento mapping
                    tipo = res.get("almacenamiento")
                    mapping = {}
                    if tipo == "Objetos": mapping = {"AWS":"Amazon S3","GCP":"Cloud Storage","Azure":"Blob Storage"}
                    elif tipo == "Bloques": mapping = {"AWS":"Amazon EBS","GCP":"Persistent Disk","Azure":"Azure Managed Disks"}
                    elif tipo == "Archivos": mapping = {"AWS":"Amazon EFS","GCP":"Filestore","Azure":"Azure Files"}
                    if mapping:
                        svc_st_name = mapping[prov]
                        niveles_st_cumplidos, max_n_st_disponible = obtener_nivel_confidencialidad(svc_st_name, prov, res["confidencialidad"] )
                        if niveles_st_cumplidos:
                            for lvl in niveles_st_cumplidos:
                                if lvl['Nivel de confidencialidad'] == 5 and lvl.get('Como se cumple para datos en transito'):
                                    st.write(f"- **{svc_st_name}** Nivel {lvl['Nivel de confidencialidad']}: Reposo: {lvl['Como se cumple para datos en reposo']}; Tránsito: {lvl['Como se cumple para datos en transito']}")
                                else:
                                    st.write(f"- **{svc_st_name}** Nivel {lvl['Nivel de confidencialidad']}: Reposo: {lvl['Como se cumple para datos en reposo']}")
                        else:
                            st.info(f"    No se encontraron niveles de confidencialidad para **{svc_st_name}** que cumplan con el nivel {res['confidencialidad']} (Máx disponible: {max_n_st_disponible}).")
                

            # Generación de PDF (La lógica del PDF no ha cambiado drásticamente para las descripciones de nivel,
            # ya que solo afectan la UI interactiva)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Guía de recomendaciones para la selección de proveedor en la nube", ln=True)

        # Resumen de elecciones del usuario
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Resumen de elecciones del usuario", ln=True)
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(0, 6, f"- Enfoque de seguridad: {res.get('enfoque_seguridad','No especificado')}")
        pdf.multi_cell(0, 6, f"- Nivel de Confidencialidad: {res.get('confidencialidad_texto','No especificado')}")
        pdf.multi_cell(0, 6, f"- Nivel de Integridad: {res.get('integridad_texto','No especificado')}")
        pdf.multi_cell(0, 6, f"- Máquinas Virtuales: {res.get('mv_requiere','No especificado')}")
        if res.get('mv_requiere') == "Sí":
            pdf.multi_cell(0, 6, f"    - Tipo: {res.get('mv_tipo','-')}")
            pdf.multi_cell(0, 6, f"    - SO: {', '.join(res.get('mv_sistemas',[]))}")
            # Intenta obtener la familia de la VM para el PDF también
            for prov in ganadores: # Asumimos que los ganadores son los que se mostrarán en PDF
                vm_data_list_pdf = SERVICIOS[prov].get("mv", [])
                if not isinstance(vm_data_list_pdf, list):
                    vm_data_list_pdf = [vm_data_list_pdf]

                selected_vm_name_pdf = None
                selected_vm_family_pdf = None
                
                selected_mv_type_pdf = res.get("mv_tipo")
                if selected_mv_type_pdf and selected_mv_type_pdf != "Seleccionar...":
                    for vm_item_pdf in vm_data_list_pdf:
                        if vm_item_pdf.get("tipo") == selected_mv_type_pdf:
                            selected_vm_name_pdf = vm_item_pdf.get("nombre")
                            selected_vm_family_pdf = vm_item_pdf.get("familia")
                            break
                
                if not selected_vm_name_pdf and vm_data_list_pdf:
                    for vm_item_pdf in vm_data_list_pdf:
                        if vm_item_pdf.get("tipo") == "Propósito general":
                            selected_vm_name_pdf = vm_item_pdf.get("nombre")
                            selected_vm_family_pdf = vm_item_pdf.get("familia")
                            break
                    if not selected_vm_name_pdf and vm_data_list_pdf:
                        selected_vm_name_pdf = vm_data_list_pdf[0].get("nombre")
                        selected_vm_family_pdf = vm_data_list_pdf[0].get("familia")

                if selected_vm_name_pdf:
                    pdf.multi_cell(0, 6, f"    - VM seleccionada: {selected_vm_name_pdf}" + (f" (Familia: {selected_vm_family_pdf})" if selected_vm_family_pdf else ""))
                    break # Salir después de encontrar la VM del primer ganador
        
        pdf.multi_cell(0, 6, f"- Contenedores: {res.get('contenedores','No especificado')}")
        pdf.multi_cell(0, 6, f"- Almacenamiento: {res.get('almacenamiento','No especificado')}")
        pdf.multi_cell(0, 6, f"- Bases de Datos: {res.get('bd_requiere','No especificado')}")
        if res.get('bd_requiere') == 'Sí':
            pdf.multi_cell(0, 6, f"    - Tipo: {res.get('bd_tipo','-')}")
            if res.get('bd_tipo') == 'Relacional':
                pdf.multi_cell(0, 6, f"    - Motor: {res.get('bd_motor','-')}")
        pdf.multi_cell(0, 6, f"- Servicios de IA requeridos: {res.get('ia_tipo','No especificado')}")
        pdf.multi_cell(0, 6, f"- Web Scraping: {res.get('scraping','No especificado')}")
        pdf.multi_cell(0, 6, f"- Presupuesto (Costo): {res.get('costo_texto','No especificado')}")
        pdf.multi_cell(0, 6, f"- Nivel de disponibilidad deseado: {res.get('disponibilidad_texto','No especificado')}")
        pdf.ln(5)

        # Ranking y razones
        for proveedor, puntaje in orden:
            pdf.set_font("Arial", "B", 12)
            if proveedor in ganadores and len(ganadores) == 1:
                pdf.set_text_color(0, 102, 0)
                pdf.cell(0, 10, f"Proveedor recomendado: {proveedor} ({puntaje:.1f} puntos)", ln=True)
            elif proveedor in ganadores:
                pdf.set_text_color(0, 102, 102)
                pdf.cell(0, 10, f"Empate válido: {proveedor} ({puntaje:.1f} puntos)", ln=True)
            else:
                pdf.set_text_color(0, 0, 128)
                pdf.cell(0, 10, f"Alternativa: {proveedor} ({puntaje:.1f} puntos)", ln=True)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Arial", "", 10)
            for r in razones[proveedor]:
                pdf.multi_cell(0, 6, f"- {r}")
            pdf.ln(2)

            # Servicios sugeridos
            servicios = obtener_servicios_relevantes(res, proveedor)
            if servicios:
                pdf.set_font("Arial", "B", 11)
                pdf.cell(0, 8, "Servicios sugeridos:", ln=True)
                pdf.set_font("Arial", "", 9)
                vistos = set()
                for s in servicios:
                    nombre = s.get('nombre')
                    if nombre in vistos: continue
                    vistos.add(nombre)
                    
                    # Incluir la familia en el PDF para VMs
                    display_name_pdf = nombre
                    if nombre in ["Amazon EC2", "Compute Engine", "Azure VM"] and s.get("familia"):
                        display_name_pdf += f" (Familia: {s['familia']})"

                    pdf.multi_cell(0, 6, f"Servicio: {display_name_pdf}")
                    if res['enfoque_seguridad'] in ['Confidencialidad','Ambos']:
                        niveles, _ = obtener_nivel_confidencialidad(nombre, proveedor, res['confidencialidad'])
                        for lvl in niveles:
                            if res['confidencialidad'] == 5 and lvl.get('Como se cumple para datos en transito'):
                                pdf.multi_cell(0, 6, f"  Nivel {lvl['Nivel de confidencialidad']}: Reposo: {lvl['Como se cumple para datos en reposo']}; Tránsito: {lvl['Como se cumple para datos en transito']}")
                            else:
                                pdf.multi_cell(0, 6, f"  Nivel {lvl['Nivel de confidencialidad']}: Reposo: {lvl['Como se cumple para datos en reposo']}")
                    if res['enfoque_seguridad'] in ['Integridad','Ambos'] and s.get('caracteristicas_integridad'):
                        pdf.multi_cell(0, 6, "  Características de Integridad:")
                        for c in s['caracteristicas_integridad']:
                            pdf.multi_cell(0, 6, f"    - {c}")
                    if s.get('costo_aproximado'):
                        costo_str = s['costo_aproximado']
                        if isinstance(costo_str, list):
                            costo_str = ", ".join(costo_str)
                        pdf.multi_cell(0, 6, f"  Costo estimado: {costo_str}")
                    pdf.ln(1)
                pdf.ln(3)

        # Descargar PDF
        nombre_pdf = f"Reporte_de_recomendaciones_{datetime.now().strftime('%Y-%m-%d')}.pdf"
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        b64 = base64.b64encode(pdf_bytes).decode()
        st.markdown(
            f'<a href="data:application/octet-stream;base64,{b64}" download="{nombre_pdf}">📄 Descargar PDF con recomendaciones</a>',
            unsafe_allow_html=True
        )

    except Exception as e:
        st.error(f"Error inesperado: {e}")
        st.error(traceback.format_exc())

