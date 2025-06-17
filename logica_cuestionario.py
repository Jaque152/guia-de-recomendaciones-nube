# logica_cuestionario.py

import json
import os
from reglas_combinacionales import reglas_combinacionales, cumple_condicion_struct

# --- Constantes y carga de datos ---
PROVEEDORES = ["AWS", "GCP", "Azure"]
AREAS = ["mv", "contenedores", "almacenamiento", "bd", "ia", "scraping"]
FACTOR_PESO_FUNCIONAL = 1

# Máximo nivel (0–5) que cada proveedor ofrece por criterio de adecuación
NIVELES_MAXIMOS = {
    "confidencialidad": {"AWS": 5, "GCP": 5, "Azure": 5},
    "costos":           {"AWS": 3, "GCP": 5, "Azure": 3},
    "disponibilidad":   {"AWS": 5, "GCP": 3, "Azure": 3},
    "integridad":       {"AWS": 5, "GCP": 3, "Azure": 5},
}

# Cargar matriz de confidencialidad
with open(os.path.join(os.path.dirname(__file__), "confidencialidad_niveles.json"), encoding="utf-8") as f:
    MATRIZ_CONF = json.load(f)

# Cargar catálogo de servicios
with open(os.path.join(os.path.dirname(__file__), "servicios.json"), encoding="utf-8") as f:
    SERVICIOS = json.load(f)


def obtener_nivel_confidencialidad(servicio_nombre, proveedor, nivel_deseado):
    """
    Devuelve listado de dicts con los detalles de cumplimiento de niveles de confidencialidad
    hasta el nivel_deseado (o todos si nivel_deseado es muy alto),
    y el máximo nivel encontrado para ese servicio y proveedor.
    """
    niveles_cumplidos = []
    max_nivel_encontrado = 0

    for entry in MATRIZ_CONF.get(proveedor, []):
        # Asegurarse de que 'Servicio' es una lista para una verificación consistente
        servicios_en_entrada = [entry["Servicio"]] if isinstance(entry["Servicio"], str) else entry["Servicio"]
        
        # Normalizar el nombre del servicio para la comparación
        nombre_servicio_lower = servicio_nombre.lower()

        # Si el servicio_nombre es un alias que debe mapearse a un servicio real
        # Este es un punto crucial para las VMs
        if nombre_servicio_lower == "maquinas virtuales":
            # Si el servicio es "maquinas virtuales", buscamos los servicios específicos de VM
            # en la matriz de confidencialidad (ej: "Amazon EC2", "Compute Engine", "Azure Virtual Machines")
            # Este mapeo es un ejemplo, se debería basar en cómo están nombrados en confidencialidad_niveles.json
            if proveedor == "AWS":
                servicios_en_entrada = ["Amazon EC2"]
            elif proveedor == "GCP":
                servicios_en_entrada = ["Compute Engine"]
            elif proveedor == "Azure":
                servicios_en_entrada = ["Azure Virtual Machines"]
            else:
                servicios_en_entrada = [] # No hay mapeo específico, no se encontrarán niveles
        elif nombre_servicio_lower == "almacenamiento de objetos":
            if proveedor == "AWS":
                servicios_en_entrada = ["Amazon S3"]
            elif proveedor == "GCP":
                servicios_en_entrada = ["Cloud Storage"]
            elif proveedor == "Azure":
                servicios_en_entrada = ["Azure Blob Storage"]
        elif nombre_servicio_lower == "almacenamiento de bloques":
            if proveedor == "AWS":
                servicios_en_entrada = ["Amazon EBS"]
            elif proveedor == "GCP":
                servicios_en_entrada = ["Persistent Disk"]
            elif proveedor == "Azure":
                servicios_en_entrada = ["Azure Disk Storage"]
        elif nombre_servicio_lower == "almacenamiento de archivos":
            if proveedor == "AWS":
                servicios_en_entrada = ["Amazon EFS"]
            elif proveedor == "GCP":
                servicios_en_entrada = ["Filestore"]
            elif proveedor == "Azure":
                servicios_en_entrada = ["Azure Files"]

        # Verificar si el servicio solicitado está en la lista de servicios de la entrada de la matriz
        if any(svc_in_entry.lower() == nombre_servicio_lower for svc_in_entry in servicios_en_entrada):
            nivel_actual = entry["Nivel de confidencialidad"]
            if nivel_actual <= nivel_deseado:
                niveles_cumplidos.append({
                    "Nivel de confidencialidad": nivel_actual,
                    "Como se cumple para datos en reposo": entry.get("Como se cumple para datos en reposo", "No especificado"),
                    "Como se cumple para datos en transito": entry.get("Como se cumple para datos en transito", "No especificado")
                })
            # Siempre actualizar el nivel máximo encontrado, independientemente del nivel deseado
            if nivel_actual > max_nivel_encontrado:
                max_nivel_encontrado = nivel_actual

    # Ordenar los niveles cumplidos por "Nivel de confidencialidad"
    niveles_cumplidos.sort(key=lambda x: x["Nivel de confidencialidad"])
    return niveles_cumplidos, max_nivel_encontrado


def obtener_servicios_relevantes(respuestas, proveedor):
    """
    Retorna una lista de servicios del JSON que coinciden con las respuestas del usuario.
    Normaliza las claves de entrada de 'respuestas' para que coincidan con la nueva estructura
    esperada por esta función.
    """
    rel = []

    # Mapeo de las claves del cuestionario a las claves internas de logica_cuestionario.py
    # y los servicios.json si es necesario.
    # Estas claves ahora vienen de tu app.py actualizada.
    mv_requiere = respuestas.get("mv_requiere")
    mv_tipo = respuestas.get("mv_tipo")
    mv_sistemas = respuestas.get("mv_sistemas", [])
    mv_escalabilidad_automatica = respuestas.get("mv_escalabilidad_automatica")
    mv_hibernacion = respuestas.get("mv_hibernacion")

    contenedores_requiere = respuestas.get("contenedores_requiere")
    contenedores_orquestador = respuestas.get("contenedores_orquestador")
    contenedores_servless = respuestas.get("contenedores_servless")

    almacenamiento_requiere = respuestas.get("almacenamiento_requiere")
    almacenamiento_tipo = respuestas.get("almacenamiento_tipo")
    almacenamiento_acceso_frecuente = respuestas.get("almacenamiento_acceso_frecuente")
    almacenamiento_resiliencia = respuestas.get("almacenamiento_resiliencia")

    bd_requiere = respuestas.get("bd_requiere")
    bd_tipo = respuestas.get("bd_tipo")
    bd_escalabilidad_lectura = respuestas.get("bd_escalabilidad_lectura")
    bd_analitica = respuestas.get("bd_analitica")

    ia_requiere = respuestas.get("ia_requiere")
    ia_tipo = respuestas.get("ia_tipo", []) # Ahora es una lista desde el multiselect
    ia_modelos_preentrenados = respuestas.get("ia_modelos_preentrenados")

    scraping_requiere = respuestas.get("scraping_requiere")
    scraping_volumen = respuestas.get("scraping_volumen")
    scraping_anti_bloqueo = respuestas.get("scraping_anti_bloqueo")
    scraping_headless = respuestas.get("scraping_headless")

    # Máquinas virtuales
    if mv_requiere == "Sí":
        # Para MV, podemos agregar un servicio genérico "Maquinas Virtuales"
        # y la lógica de confidencialidad en obtener_nivel_confidencialidad se encargará del mapeo interno
        # a servicios específicos de cada proveedor (EC2, Compute Engine, Azure VM).
        # Esto es para que haya un 'servicio' que pueda ser buscado en confidencialidad_niveles.json
        rel.append({"nombre": "Maquinas Virtuales", "tipo": mv_tipo})

    # Contenedores
    if contenedores_requiere == "Sí":
        cont = SERVICIOS[proveedor].get("contenedores")
        if cont: # Si es un diccionario (servicio único) o una lista de servicios
            if isinstance(cont, dict):
                rel.append(cont)
            elif isinstance(cont, list):
                rel.extend(cont)

    # Almacenamiento
    if almacenamiento_requiere == "Sí" and almacenamiento_tipo:
        # Mapear el tipo de almacenamiento a las claves en servicios.json
        # y para confidencialidad_niveles.json
        if almacenamiento_tipo == "Objetos":
            serv_data = SERVICIOS[proveedor].get("almacenamiento", {}).get("objetos")
            if serv_data:
                rel.extend(serv_data)
        elif almacenamiento_tipo == "Bloques":
            serv_data = SERVICIOS[proveedor].get("almacenamiento", {}).get("bloques")
            if serv_data:
                rel.extend(serv_data)
        elif almacenamiento_tipo == "Archivos":
            serv_data = SERVICIOS[proveedor].get("almacenamiento", {}).get("archivos")
            if serv_data:
                rel.extend(serv_data)
        # Si es "Mixto", quizás añadir todos los tipos de almacenamiento si existen
        elif almacenamiento_tipo == "Mixto":
             for tipo_key in ["objetos", "bloques", "archivos"]:
                serv_data = SERVICIOS[proveedor].get("almacenamiento", {}).get(tipo_key)
                if serv_data:
                    rel.extend(serv_data)

    # Bases de datos
    if bd_requiere == "Sí":
        bd_seccion = SERVICIOS[proveedor].get("bd", {})
        if bd_tipo == "Relacional":
            rel.extend(bd_seccion.get("relacional", []))
        elif bd_tipo.startswith("NoSQL"): # Cubre todos los tipos NoSQL
            rel.extend(bd_seccion.get("no_relacional", [])) # Asumiendo un único array para NoSQL

    # IA
    if ia_requiere == "Sí":
        ia_sec = SERVICIOS[proveedor].get("ia", {})
        # Si ia_tipo es una lista (multiselect en app.py)
        if "Procesamiento de Lenguaje Natural (PLN)" in ia_tipo:
            rel.extend(ia_sec.get("pln", []))
        if "Visión por Computadora" in ia_tipo:
            rel.extend(ia_sec.get("vision", []))
        if "Voz (Síntesis/Reconocimiento)" in ia_tipo:
            # Aquí podrías decidir si añadir "voz" o "texto_a_voz" o ambos
            rel.extend(ia_sec.get("voz", []))
            rel.extend(ia_sec.get("texto_a_voz", []))
        if "Recomendación/Personalización" in ia_tipo:
            rel.extend(ia_sec.get("recomendacion", []))
        if "Análisis predictivo" in ia_tipo:
            rel.extend(ia_sec.get("analisis_predictivo", []))
        
        # Si la respuesta es "Uso general" (que ahora es una opción del multiselect 'ia_tipo')
        if "Uso general" in ia_tipo:
            rel.extend(ia_sec.get("general", [])) # Asegúrate que existe una sección 'general' en servicios.json para IA

    # Web scraping
    if scraping_requiere == "Sí":
        rel.extend(SERVICIOS[proveedor].get("scraping", []))

    # Asegurarse de que los servicios devueltos son únicos
    unique_services = {}
    for service in rel:
        name = service.get("nombre")
        if name and name not in unique_services:
            unique_services[name] = service
    
    return list(unique_services.values())

def aplicar_reglas_combinacionales(respuestas, scores, razones):
    """
    Añade puntos extra según reglas_combinacionales.py.
    Asegura que las razones son únicas usando un set temporal.
    """
    for regla in reglas_combinacionales:
        if cumple_condicion_struct(respuestas, regla["condiciones"]):
            proveedores = regla["proveedor"]
            if isinstance(proveedores, str):
                proveedores = [proveedores]
            for p in proveedores:
                if p in scores:
                    scores[p] += regla["puntos"]
                    # Añadir a un set para asegurar unicidad antes de añadir a la lista final
                    if regla["descripcion"] not in razones[p]: # Solo añadir si no existe ya
                        razones[p].add(regla["descripcion"]) # Usar .add para sets


def evaluar_funcional(res):
    """
    Calcula la puntuación funcional: 1 punto por cada área satisfecha,
    luego multiplica cada punto por FACTOR_PESO_FUNCIONAL.
    Las razones se almacenan en un set para evitar duplicados.
    """
    cont = {p: {a: 0 for a in AREAS} for p in PROVEEDORES} # Corregido typo
    razones = {p: set() for p in PROVEEDORES} # Usar set para razones

    # MV
    if res.get("mv_requiere") == "Sí":
        area = "mv"
        tipo = res.get("mv_tipo")
        so = res.get("mv_sistemas", [])
        
        # Mapeo de tipos de MV a proveedores y razones
        if tipo == "Optimización de CPU":
            cont["Azure"][area] += 1
            razones["Azure"].add("CPU-Optimized en Azure (+1).")
        if tipo in ["Optimización de memoria", "Aceleradores de hardware (GPU/FPGA)"]:
            for p in ("AWS", "Azure", "GCP"): # Añadimos GCP también si soporta estas cargas
                cont[p][area] += 1
                razones[p].add(f"Carga especializada ({tipo}) en {p} (+1).")
        if tipo == "Cómputo de alto rendimiento": # Nuevo tipo de MV en tu app.py
            for p in PROVEEDORES:
                cont[p][area] += 1
                razones[p].add(f"Cómputo de alto rendimiento en {p} (+1).")

        if "MacOs" in so: # Revisa si el SO es macOS
            cont["AWS"][area] += 1
            razones["AWS"].add("Soporte macOS nativo en AWS (+1).")
        elif "Linux" in so or "Windows" in so or "Ambos" in so: # Si se selecciona Linux/Windows/Ambos
             for p in PROVEEDORES:
                cont[p][area] += 1
                razones[p].add(f"Soporte para {', '.join(so)} en {p} (+1).")

        if res.get("mv_escalabilidad_automatica") == "Sí": # Renombrado
            for p in ("AWS","GCP","Azure"): # Los tres ofrecen autoescalamiento
                cont[p][area] += 1
                razones[p].add(f"Escalabilidad automática para MV en {p} (+1).")
        if res.get("mv_hibernacion") == "Sí":
            for p in ("AWS","GCP"): # Azure también tiene opciones similares ahora
                cont[p][area] += 1
                razones[p].add(f"Hibernación de MV en {p} (+1).")


    # Contenedores
    if res.get("contenedores_requiere") == "Sí":
        if res.get("contenedores_orquestador") == "Kubernetes":
            for p in PROVEEDORES: # Los tres tienen Kubernetes
                cont[p]["contenedores"] += 1
                razones[p].add(f"Orquestación de contenedores con Kubernetes en {p} (+1).")
        if res.get("contenedores_servless") == "Sí":
            cont["AWS"]["contenedores"] += 1 # Ej: AWS Fargate
            cont["GCP"]["contenedores"] += 1 # Ej: Cloud Run
            cont["Azure"]["contenedores"] += 1 # Ej: Azure Container Instances / Azure Container Apps
            razones["AWS"].add("Enfoque serverless para contenedores en AWS (+1).")
            razones["GCP"].add("Enfoque serverless para contenedores en GCP (+1).")
            razones["Azure"].add("Enfoque serverless para contenedores en Azure (+1).")

    # Almacenamiento
    if res.get("almacenamiento_requiere") == "Sí":
        tipo_alm = res.get("almacenamiento_tipo")
        if tipo_alm == "Objetos":
            for p in PROVEEDORES:
                cont[p]["almacenamiento"] += 1
                razones[p].add(f"Almacenamiento de objetos en {p} (+1).")
        elif tipo_alm == "Bloques":
            for p in PROVEEDORES:
                cont[p]["almacenamiento"] += 1
                razones[p].add(f"Almacenamiento de bloques en {p} (+1).")
        elif tipo_alm == "Archivos":
            for p in PROVEEDORES:
                cont[p]["almacenamiento"] += 1
                razones[p].add(f"Almacenamiento de archivos en {p} (+1).")
        elif tipo_alm == "Mixto": # Si el usuario eligió mixto, se valoran todos
            for p in PROVEEDORES:
                cont[p]["almacenamiento"] += 1
                razones[p].add(f"Almacenamiento de objetos, bloques y archivos en {p} (+1).")
        
        if res.get("almacenamiento_acceso_frecuente") == "Sí":
            for p in PROVEEDORES:
                cont[p]["almacenamiento"] += 1
                razones[p].add(f"Acceso frecuente a datos en {p} (+1).")
        if res.get("almacenamiento_resiliencia") == "Sí":
            for p in PROVEEDORES:
                cont[p]["almacenamiento"] += 1
                razones[p].add(f"Alta resiliencia y durabilidad de datos en {p} (+1).")

    # Bases de datos
    if res.get("bd_requiere") == "Sí":
        tipo_bd = res.get("bd_tipo")
        if tipo_bd == "Relacional":
            for p in PROVEEDORES:
                cont[p]["bd"] += 1
                razones[p].add(f"Bases de datos relacionales en {p} (+1).")
        elif tipo_bd.startswith("NoSQL"): # Cubre todos los tipos NoSQL
            for p in PROVEEDORES:
                cont[p]["bd"] += 1
                razones[p].add(f"Bases de datos NoSQL ({tipo_bd.split('(')[1].replace(')', '')}) en {p} (+1).")
        
        if res.get("bd_escalabilidad_lectura") == "Sí":
            for p in PROVEEDORES:
                cont[p]["bd"] += 1
                razones[p].add(f"Alta escalabilidad para lecturas de BD en {p} (+1).")
        if res.get("bd_analitica") == "Sí":
            for p in PROVEEDORES:
                cont[p]["bd"] += 1
                razones[p].add(f"Capacidades de analítica/BI en BD en {p} (+1).")

    # IA / ML
    if res.get("ia_requiere") == "Sí":
        ia_tipos_seleccionados = res.get("ia_tipo", [])
        
        if "Procesamiento de Lenguaje Natural (PLN)" in ia_tipos_seleccionados:
            for p in PROVEEDORES:
                cont[p]["ia"] += 1
                razones[p].add(f"Servicios de PLN en {p} (+1).")
        if "Visión por Computadora" in ia_tipos_seleccionados:
            for p in PROVEEDORES:
                cont[p]["ia"] += 1
                razones[p].add(f"Servicios de Visión por Computadora en {p} (+1).")
        if "Voz (Síntesis/Reconocimiento)" in ia_tipos_seleccionados:
            for p in PROVEEDORES:
                cont[p]["ia"] += 1
                razones[p].add(f"Servicios de Voz (TTS/STT) en {p} (+1).")
        if "Recomendación/Personalización" in ia_tipos_seleccionados:
            for p in PROVEEDORES:
                cont[p]["ia"] += 1
                razones[p].add(f"Servicios de Recomendación/Personalización en {p} (+1).")
        if "Análisis predictivo" in ia_tipos_seleccionados:
            for p in PROVEEDORES:
                cont[p]["ia"] += 1
                razones[p].add(f"Servicios de Análisis predictivo en {p} (+1).")
        
        if res.get("ia_modelos_preentrenados") in ["Pre-entrenados", "Ambos"]:
            for p in PROVEEDORES:
                cont[p]["ia"] += 1
                razones[p].add(f"Soporte para modelos IA pre-entrenados en {p} (+1).")
        if res.get("ia_modelos_preentrenados") in ["Construir propios", "Ambos"]:
            for p in PROVEEDORES:
                cont[p]["ia"] += 1
                razones[p].add(f"Flexibilidad para construir modelos IA propios en {p} (+1).")


    # Scraping
    if res.get("scraping_requiere") == "Sí":
        for p in PROVEEDORES:
            cont[p]["scraping"] += 1
            razones[p].add(f"Soporte para Web Scraping en {p} (+1).")
        
        if res.get("scraping_anti_bloqueo") == "Sí":
            for p in PROVEEDORES:
                cont[p]["scraping"] += 1
                razones[p].add(f"Mecanismos anti-bloqueo para scraping en {p} (+1).")
        if res.get("scraping_headless") == "Sí":
            for p in PROVEEDORES:
                cont[p]["scraping"] += 1
                razones[p].add(f"Soporte para navegadores headless en {p} (+1).")

    # Multiplicar por factor
    scores = {p: sum(cont[p].values()) * FACTOR_PESO_FUNCIONAL for p in PROVEEDORES}
    
    # Convertir los sets de razones a listas para el retorno
    # final_razones = {p: list(r) for p, r in razones.items()}
    final_razones = razones
    return scores, final_razones


def evaluar_adecuacion(res):
    """
    Calcula la adecuación por criterio: peso_usuario × (nivel_ofrecido/5).
    Usa los sliders 'confidencialidad', 'costo', 'disponibilidad', 'integridad'.
    Las razones se almacenan en un set para evitar duplicados.
    """
    pesos = {
        "confidencialidad": res.get("confidencialidad", 3),
        "costos":           res.get("costo_texto", "Moderado"), # Ahora 'costo_texto'
        "disponibilidad":   res.get("disponibilidad", 3),
        "integridad":       res.get("integridad", 3)
    }
    scores = {p: 0.0 for p in PROVEEDORES}
    razones = {p: set() for p in PROVEEDORES} # Usar set para razones

    # Mapear costo_texto a un valor numérico para cálculo de adecuación
    costo_map_num = {"Bajo": 5, "Moderado": 3, "Alto": 1} # Inverso para que "Bajo" sea mayor puntuación
    
    for crit, tabla in NIVELES_MAXIMOS.items():
        for p in PROVEEDORES:
            nivel_ofrecido = tabla.get(p, 0)
            
            # Calcular contribución basándose en el tipo de criterio
            if crit == "costos":
                # La "puntuación" para costos es inversa: menor costo_texto (Bajo) -> mayor puntuación
                # Multiplicamos el nivel ofrecido por el mapeo numérico de la prioridad del usuario
                # NIVELES_MAXIMOS["costos"] ya representa qué tan "barato" es el proveedor (5=muy barato)
                # Si el usuario quiere costo "Bajo" (5 puntos), y el proveedor es "GCP" (5 puntos), 5*5 = 25
                # Si el usuario quiere costo "Bajo" (5 puntos), y el proveedor es "AWS" (3 puntos), 5*3 = 15
                # Dejamos la fórmula estándar para ser consistente. La "adecuación" para costos ya es el NIVELES_MAXIMOS.
                # Lo importante es que NIVELES_MAXIMOS[costos] ya indica "buenos costos" (más alto = mejor)
                # El peso del usuario debería enfatizar eso.
                # Para el costo, si el usuario quiere "Bajo" (peso 5), y el proveedor es bueno en costos (nivel 5), se multiplica.
                # Si el usuario quiere "Alto" (peso 1), y el proveedor es bueno en costos (nivel 5), se penaliza.
                # Revertir el peso del usuario para el costo_texto para que "Bajo" sea 5 y "Alto" sea 1.
                peso_costo_numerico = costo_map_num.get(pesos.get("costos"), 3)
                contrib = peso_costo_numerico * (nivel_ofrecido / 5) # Multiplicar por el nivel ofrecido normalizado
                
            else: # Para confidencialidad, disponibilidad, integridad
                # El peso del usuario es directo: 5 = muy importante
                peso_usuario = pesos.get(crit, 0)
                contrib = peso_usuario * (nivel_ofrecido / 5)

            scores[p] += contrib
            razones[p].add(
                f"Adecuación {crit}: {nivel_ofrecido}/5 × peso {pesos.get(crit, 'N/A')} = {contrib:.1f} pts."
            )

    return scores, razones


def evaluar_respuestas(res):
    """
    1) Funcional
    2) Adecuación
    3) Reglas combinacionales
    4) Penalización/Advertencia por no alcanzar nivel de confidencialidad
    Devuelve: final_scores, final_reasons
    """
    # 1) Funcional
    f_scores, f_reasons = evaluar_funcional(res)
    # 2) Adecuación
    a_scores, a_reasons = evaluar_adecuacion(res)
    
    # 3) Sumar scores y combinar razones (los sets se combinan con union |)
    final_scores = {p: f_scores.get(p, 0) + a_scores.get(p, 0) for p in PROVEEDORES}
    final_reasons = {p: f_reasons.get(p, []) + list(a_reasons.get(p, set())) for p in PROVEEDORES}
    # 4) Reglas combinacionales (modifica final_scores y final_reasons in-place)
    aplicar_reglas_combinacionales(res, final_scores, final_reasons)
    
    # 5) Advertencia: confidencialidad (LÓGICA CORREGIDA para solo mensaje)
    if res.get("enfoque_seguridad") in ["Confidencialidad", "Ambos"]:
        nivel_req = res.get("confidencialidad", 3)
        # peso_conf = res.get("confidencialidad", 3) # No se usa para penalización, solo para mensaje

        for p in PROVEEDORES:
            # Obtener los servicios relevantes para el proveedor y las respuestas del usuario
            servicios_relevantes_proveedor = obtener_servicios_relevantes(res, p)
            
            if not servicios_relevantes_proveedor:
                # Si no hay servicios relevantes, no hay nada que evaluar para confidencialidad
                continue

            for s in servicios_relevantes_proveedor:
                nombre_servicio = s.get("nombre", "")
                if not nombre_servicio:
                    continue
                
                # Obtener el máximo nivel de confidencialidad que el servicio ofrece
                _, max_nivel_ofrecido = obtener_nivel_confidencialidad(nombre_servicio, p, nivel_req)
                
                if max_nivel_ofrecido < nivel_req:
                    # No restar puntos, solo añadir una advertencia
                    final_reasons[p].add(
                        f"¡Advertencia! El servicio '{nombre_servicio}' de {p} no alcanza el nivel de confidencialidad requerido de {nivel_req} (máx: {max_nivel_ofrecido})."
                    )
    
    # Convertir los sets de razones a listas antes de devolver
    final_reasons_list = {p: list(r) for p, r in final_reasons.items()}

    return None, final_reasons_list, final_scores # Devuelve None para el primer valor no usado, y los otros dos