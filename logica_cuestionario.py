# logica_cuestionario.py
import json
import os
from reglas_combinacionales import reglas_combinacionales, cumple_condicion_struct

# Constantes
PROVEEDORES = ["AWS", "GCP", "Azure"]
AREAS = ["mv", "contenedores", "almacenamiento", "bd", "ia", "scraping"]
FACTOR_PESO_FUNCIONAL = 1

# Niveles máximos para adecuación (offered levels)
NIVELES_MAXIMOS = {
    "confidencialidad": {"AWS":5, "GCP":5, "Azure":5},
    "costos":           {"AWS":3, "GCP":5, "Azure":3},
    "disponibilidad":   {"AWS":5, "GCP":3, "Azure":3},
    "integridad":       {"AWS":5, "GCP":3, "Azure":5},
}

# Carga de datos externos
_BASE = os.path.dirname(__file__)
with open(os.path.join(_BASE, "confidencialidad_niveles.json"), encoding="utf-8") as f:
    MATRIZ_CONF = json.load(f)
with open(os.path.join(_BASE, "servicios.json"), encoding="utf-8") as f:
    SERVICIOS = json.load(f)


def obtener_nivel_confidencialidad(servicio, proveedor, nivel_req):
    cumplidos, max_n = [], 0
    for e in MATRIZ_CONF.get(proveedor, []):
        servicios_en_matriz = e["Servicio"] if isinstance(e["Servicio"], list) else [e["Servicio"]]
        # Comparamos el servicio de entrada (ej. "Amazon EC2") con los servicios en la matriz de confidencialidad
        if servicio.lower() in [s.lower() for s in servicios_en_matriz]:
            nivel = e["Nivel de confidencialidad"]
            if nivel <= nivel_req:
                cumplidos.append({
                    "Nivel de confidencialidad": nivel,
                    "Como se cumple para datos en reposo": e.get("Como se cumple para datos en reposo"),
                    "Como se cumple para datos en transito": e.get("Como se cumple para datos en transito")
                })
            max_n = max(max_n, nivel)
    cumplidos.sort(key=lambda x: x["Nivel de confidencialidad"])
    return cumplidos, max_n


def obtener_servicios_relevantes(res, proveedor):
    rel = []
    # Máquinas virtuales - Lógica mejorada para seleccionar la VM correcta por tipo
    if res.get("mv_requiere") == "Sí":
        mv_services = SERVICIOS[proveedor].get("mv")
        if mv_services:
            # Asegurarse de que mv_services es siempre una lista para iterar consistentemente
            if not isinstance(mv_services, list):
                mv_services = [mv_services]
            
            found_mv = None
            selected_mv_type = res.get("mv_tipo") # e.g., "Propósito general"
            
            # Buscar una VM que coincida exactamente con el tipo seleccionado por el usuario
            if selected_mv_type and selected_mv_type != "Seleccionar...":
                for mv_svc in mv_services:
                    if mv_svc.get("tipo") == selected_mv_type: # Checks if 'tipo' in JSON matches selected_mv_type
                        found_mv = mv_svc
                        break
            
            # Si no se encontró una VM por tipo específico, o si el tipo era "Propósito general"
            # intentar encontrar una de "Propósito general" o simplemente la primera disponible
            if not found_mv and mv_services:
                # Priorizar "Propósito general" si existe y no se encontró otra coincidencia
                for mv_svc in mv_services:
                    if mv_svc.get("tipo") == "Propósito general":
                        found_mv = mv_svc
                        break
                if not found_mv: # Si aún no se encontró, tomar la primera de la lista
                    found_mv = mv_services[0]

            if found_mv:
                rel.append(found_mv)

    # Contenedores
    if res.get("contenedores") == "Sí":
        cont = SERVICIOS[proveedor].get("contenedores")
        if cont:
            if isinstance(cont, dict): rel.append(cont)
            else: rel.extend(cont)
    # Almacenamiento
    tipo = res.get("almacenamiento")
    if tipo in ["Objetos","Bloques","Archivos"]:
        sec = SERVICIOS[proveedor]["almacenamiento"].get(tipo.lower())
        if sec:
            if isinstance(sec, dict): rel.append(sec)
            else: rel.extend(sec)
    # Bases de datos
    if res.get("bd_requiere") == "Sí":
        bd = SERVICIOS[proveedor].get("bd", {})
        if res.get("bd_tipo") == "Relacional": rel.extend(bd.get("relacional", []))
        else: rel.extend(bd.get("no_relacional", []))
    # Inteligencia Artificial (todos subs)
    if res.get("ia_requiere") == "Sí":
        ia = SERVICIOS[proveedor].get("ia", {})
        for serv in res.get("ia_servicios_especializados", []):
            if serv == "Reconocimiento de voz": sec = ia.get("voz", [])
            elif serv == "Convertir Texto a Voz": sec = ia.get("texto_a_voz", [])
            elif serv == "Visión": sec = ia.get("vision", [])
            elif serv == "Procesamiento de lenguaje natural": sec = ia.get("pln", [])
            elif serv == "Traducción": sec = ia.get("traduccion", [])
            else: sec = []
            if isinstance(sec, dict): rel.append(sec)
            else: rel.extend(sec)
    # Scraping
    if res.get("scraping") == "Sí": 
        scrap = SERVICIOS[proveedor].get("scraping")
        if scrap:
            if isinstance(scrap, dict): rel.append(scrap)
            else: rel.extend(scrap)
    
    # Normalizar y deduplicar
    unique = {}
    for s in rel:
        name = None
        if isinstance(s, dict):
            name_raw = s.get("nombre")
            # Asegurarse de que 'name' sea siempre una cadena de texto
            if isinstance(name_raw, list):
                name = ", ".join(map(str, name_raw)) # Unir elementos de la lista en una cadena
            elif name_raw is not None:
                name = str(name_raw)
        else:
            # Esto maneja casos donde 's' no es un diccionario (estructura inesperada)
            # Convierte 's' a una cadena para usarla como nombre.
            name = str(s)
            s = {"nombre": name, "_original_data": s} # Se puede añadir para depuración

        if name: # Solo añadir si se obtuvo un nombre válido
            if name not in unique:
                unique[name] = s
    return list(unique.values())


def aplicar_reglas_combinacionales(res, scores, razones):
    for regla in reglas_combinacionales:
        if cumple_condicion_struct(res, regla.get("condiciones", {})):
            provs = regla.get("proveedor")
            provs = [provs] if isinstance(provs, str) else provs
            for p in provs:
                if p in scores:
                    scores[p] += regla.get("puntos", 0)
                    razones[p].add(regla.get("descripcion", ""))


def evaluar_funcional(res):
    """
    Aplica únicamente las reglas especificadas para puntaje funcional.
    """
    scores = {p: 0 for p in PROVEEDORES}
    razones = {p: set() for p in PROVEEDORES} # Inicializar razones aquí también

    # 1. MV Optimización de CPU
    if res.get("mv_requiere") == "Sí" and res.get("mv_tipo") == "Optimización de CPU":
        scores["Azure"] += 1
        razones["Azure"].add("Funcional MV: Optimización de CPU (+1)")

    # 2. MV optimización memoria o GPU
    if res.get("mv_requiere") == "Sí" and res.get("mv_tipo") in ["Optimización de memoria", "Aceleradas por GPU"]:
        scores["AWS"] += 1
        scores["Azure"] += 1
        razones["AWS"].add("Funcional MV: Optimización de memoria/GPU (+1)")
        razones["Azure"].add("Funcional MV: Optimización de memoria/GPU (+1)")

    # 3. MV optimizadas para almacenamiento
    if res.get("mv_requiere") == "Sí" and res.get("mv_tipo") == "Optimización de almacenamiento":
        scores["AWS"] += 1
        scores["Azure"] += 1
        razones["AWS"].add("Funcional MV: Optimización de almacenamiento (+1)")
        razones["Azure"].add("Funcional MV: Optimización de almacenamiento (+1)")

    # 4. MacOs
    if "MacOs" in res.get("mv_sistemas", []):
        scores["AWS"] += 1
        razones["AWS"].add("Funcional MV: Soporte MacOs (+1)")

    # 5. Escalamiento predictivo
    if res.get("mv_escalamiento_predictivo") == "Sí":
        scores["AWS"] += 1
        scores["GCP"] += 1
        razones["AWS"].add("Funcional MV: Escalamiento predictivo (+1)")
        razones["GCP"].add("Funcional MV: Escalamiento predictivo (+1)")

    # 6. Auto-escalamiento (nadie suma puntos)
    # no action

    # 7. Hibernación
    if res.get("mv_hibernacion") == "Sí":
        scores["AWS"] += 1
        scores["GCP"] += 1
        razones["AWS"].add("Funcional MV: Hibernación (+1)")
        razones["GCP"].add("Funcional MV: Hibernación (+1)")

    # 8. Contenedores (Kubernetes)
    if res.get("contenedores") == "Sí":
        scores["GCP"] += 1
        razones["GCP"].add("Funcional Contenedores: Kubernetes (+1)")

    # Almacenamiento: "Ninguno" no suma puntos

    # Bases de Datos
    if res.get("bd_requiere") == "Sí":
        # 1. Cualquier motor: AWS
        if res.get("bd_motor"):
            scores["AWS"] += 1
            razones["AWS"].add("Funcional BD: Soporte cualquier motor (+1)")
        # 2. GCP y Azure solo para SQL Server, MySQL, PostgreSQL
        if res.get("bd_motor") in ["SQL Server", "MySQL", "PostgreSQL"]:
            scores["GCP"] += 1
            scores["Azure"] += 1
            razones["GCP"].add("Funcional BD: Soporte SQL Server/MySQL/PostgreSQL (+1)")
            razones["Azure"].add("Funcional BD: Soporte SQL Server/MySQL/PostgreSQL (+1)")
        # 3. No relacional con réplicas de lectura
        if res.get("bd_tipo") == "No relacional" and res.get("bd_escalabilidad_no_rel") == "Automática réplicas":
            scores["AWS"] += 1
            razones["AWS"].add("Funcional BD: NoSQL con réplicas automáticas (+1)")
        # 4. No relacional con fragmentación automática
        if res.get("bd_tipo") == "No relacional" and res.get("bd_escalabilidad_no_rel") == "Horizontal automática":
            scores["AWS"] += 1
            scores["GCP"] += 1
            razones["AWS"].add("Funcional BD: NoSQL con fragmentación automática (+1)")
            razones["GCP"].add("Funcional BD: NoSQL con fragmentación automática (+1)")

    # IA / ML
    ia_servs = res.get("ia_servicios_especializados", [])
    # 1. Reconocimiento de voz + idiomas adicionales
    if "Reconocimiento de voz" in ia_servs and res.get("voz_idiomas") == "Sí":
        scores["Azure"] += 1
        scores["GCP"] += 1
        razones["Azure"].add("Funcional IA: Reconocimiento voz + idiomas (+1)")
        razones["GCP"].add("Funcional IA: Reconocimiento voz + idiomas (+1)")
    # 2. Texto a voz + clonación
    if "Convertir Texto a Voz" in ia_servs and res.get("voz_clonacion") == "Sí":
        scores["Azure"] += 1
        scores["GCP"] += 1
        razones["Azure"].add("Funcional IA: Texto a voz + clonación (+1)")
        razones["GCP"].add("Funcional IA: Texto a voz + clonación (+1)")
    # 4. Voz muy natural
    if "Convertir Texto a Voz" in ia_servs and res.get("voz_naturalidad") == "Muy natural":
        scores["Azure"] += 1
        razones["Azure"].add("Funcional IA: Voz muy natural (+1)")
    # 5. Voz medianamente natural
    if "Convertir Texto a Voz" in ia_servs and res.get("voz_naturalidad") == "Mediana":
        scores["GCP"] += 1
        razones["GCP"].add("Funcional IA: Voz medianamente natural (+1)")
    # 6. Voz poco natural
    if "Convertir Texto a Voz" in ia_servs and res.get("voz_naturalidad") == "Poca":
        scores["AWS"] += 1
        razones["AWS"].add("Funcional IA: Voz poco natural (+1)")
    # 7. Visión + reconocimiento de lugares
    if "Visión" in ia_servs and res.get("vision_lugares") == "Sí":
        scores["GCP"] += 1
        razones["GCP"].add("Funcional IA: Visión + reconocimiento lugares (+1)")
    # 8. Visión + reconocimiento de celebridades
    if "Visión" in ia_servs and res.get("vision_celebridades") == "Sí":
        scores["AWS"] += 1
        razones["AWS"].add("Funcional IA: Visión + reconocimiento celebridades (+1)")
    # 9. PLN + análisis avanzado
    if "Procesamiento de lenguaje natural" in ia_servs and res.get("pln_analisis") == "Sí":
        scores["GCP"] += 1
        razones["GCP"].add("Funcional IA: PLN + análisis avanzado (+1)")
    # 10. Traducción + modelos personalizados
    if "Traducción" in ia_servs and res.get("traduccion_personalizada") == "Sí":
        scores["Azure"] += 1
        scores["GCP"] += 1
        razones["Azure"].add("Funcional IA: Traducción + modelos personalizados (+1)")
        razones["GCP"].add("Funcional IA: Traducción + modelos personalizados (+1)")

    return scores, razones

def evaluar_adecuacion(res):
    # Pesos directos
    peso_conf = res.get("confidencialidad", 0)
    peso_cost = res.get("costo", 0)
    peso_disp = res.get("disponibilidad", 0)
    peso_int = res.get("integridad", 0)
    scores = {p:0.0 for p in PROVEEDORES}
    razones = {p:set() for p in PROVEEDORES}
    # Adecuación base
    for crit, tabla in NIVELES_MAXIMOS.items():
        for p in PROVEEDORES:
            nivel = tabla.get(p, 0)
            if crit == "costos":
                # invertido: bajo->5, alto->1
                map_c = {1:5,2:5,3:3,4:1,5:1}
                peso = map_c.get(peso_cost, 3)
            else:
                peso = eval(f"peso_{crit[:4]}") if crit != "integridad" else peso_int
                # for confidencialidad use peso_conf, integridad peso_int, disponibilidad peso_disp
                if crit == "disponibilidad": peso = peso_disp
                elif crit == "confidencialidad": peso = peso_conf
            contrib = peso * (nivel/5)
            scores[p] += contrib
            razones[p].add(f"Adecuación {crit} = {contrib:.1f}")
            #razones[p].add(f"Adecuación {crit}: {nivel}/5 × peso {peso} = {contrib:.1f}")
    # Bonificaciones específicas
    # Integridad alta
    if peso_int >= 4:
        for prov in ["AWS","Azure"]:
            scores[prov] += 1
            razones[prov].add("Bonus integridad alta (+1)")
    # Costo bajo
    if peso_cost <= 2:
        scores["GCP"] += 1
        razones["GCP"].add("Bonus costo bajo (+1)")
    # Presupuesto alto
    if peso_cost >= 4:
        scores["AWS"] += 1
        razones["AWS"].add("Bonus presupuesto alto AWS (+1)")
    # Disponibilidad media
    if peso_disp == 3:
        scores["AWS"] += 1
        razones["AWS"].add("Bonus disponibilidad media AWS (+1)")
    # Disponibilidad alta
    if peso_disp >= 4:
        scores["AWS"] += 1
        razones["AWS"].add("Bonus alta disponibilidad AWS (+1)")
    return scores, razones


def evaluar_respuestas(res):
    f_scores, f_reasons = evaluar_funcional(res)
    a_scores, a_reasons = evaluar_adecuacion(res)
    final_scores = {p: f_scores[p] + a_scores[p] for p in PROVEEDORES}
    final_reasons = {p: f_reasons[p] | a_reasons[p] for p in PROVEEDORES} # Correctly merge sets
    aplicar_reglas_combinacionales(res, final_scores, final_reasons)
    # Advertencias confidencialidad
    if res.get("enfoque_seguridad") in ["Confidencialidad","Ambos"]:
        nivel_req = res.get("confidencialidad", 0)
        for p in PROVEEDORES:
            # Obtener solo los servicios relevantes que realmente se van a usar, incluyendo las VMs
            relevant_services_for_provider = obtener_servicios_relevantes(res, p)
            for svc_data in relevant_services_for_provider:
                svc_name = svc_data.get("nombre", "")
                # Asegurar que svc_name sea una cadena antes de pasarla
                if isinstance(svc_name, list):
                    svc_name = ", ".join(map(str, svc_name))
                elif svc_name is None:
                    continue # O manejar este caso como un error
                    
                niveles, max_n = obtener_nivel_confidencialidad(svc_name, p, nivel_req)
                if max_n < nivel_req:
                    final_reasons[p].add(
                        f"¡Advertencia! '{svc_name}' no alcanza el nivel de confidencialidad {nivel_req} (máx {max_n})"
                    )
    return final_scores, {p: list(final_reasons[p]) for p in PROVEEDORES}

