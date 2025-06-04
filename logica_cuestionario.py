##--- Lógica del cuestionario ---##

from reglas_combinacionales import reglas_combinacionales, cumple_condicion_struct
import json
import os

PROVEEDORES = ["AWS", "GCP", "Azure"]

def aplicar_reglas_combinacionales(res, scores, razones):
    for regla in reglas_combinacionales:
        if cumple_condicion_struct(res, regla["condiciones"]):
            proveedores = [regla["proveedor"]] if isinstance(regla["proveedor"], str) else regla["proveedor"]
            for prov in proveedores:
                scores[prov] += regla["puntos"]
                razones[prov].append(regla["descripcion"])

def evaluar_respuestas(res):
    scores = {p: 0 for p in PROVEEDORES}
    razones = {p: [] for p in PROVEEDORES}

    # --- Normalización previa para reglas combinacionales ---
   # Convertir sliders (1-5) a texto SOLO para reglas combinadas
    nivel_textual = lambda x: "Bajo" if x <= 2 else "Medio" if x == 3 else "Alta"
    res["costo_texto"] = nivel_textual(res.get("presupuesto", 3))
    res["disponibilidad_texto"] = nivel_textual(res.get("disponibilidad", 3))
    res["confidencialidad_texto"] = nivel_textual(res.get("confidencialidad", 3))

    if res.get("bd_tipo") == "Relacional":
        res["bd_motor_relacional"] = res.get("bd_motor")
    elif res.get("bd_tipo") == "No relacional":
        res["bd_motor_norelacional"] = res.get("bd_motor")

    # --- MÁQUINAS VIRTUALES ---
    if res.get("mv_requiere") == "Sí":
        tipo = res.get("mv_tipo")
        if tipo == "Propósito general":
            for p in PROVEEDORES:
                scores[p] += 1
                razones[p].append("MV de propósito general (+1)")
        if tipo == "Optimización de CPU":
            scores["Azure"] += 1
            razones["Azure"].append("MV optimizada en CPU (+1)")
        if tipo in ["Optimización de memoria", "Aceleradas por GPU"]:
            for p in ["AWS", "Azure"]:
                scores[p] += 1
                razones[p].append(f"MV {tipo.lower()} (+1)")
        if tipo == "Optimización de almacenamiento":
            for p in ["AWS", "Azure"]:
                scores[p] += 1
                razones[p].append("MV optimizada para almacenamiento (+1)")

        so = res.get("mv_sistemas") or []
        if "MacOs" in so:
            scores["AWS"] += 1
            razones["AWS"].append("Solo AWS ofrece soporte para MacOS (+1)")
        if any(s in so for s in ["Linux", "Windows"]):
            for p in PROVEEDORES:
                scores[p] += 1
                razones[p].append("Soporte para Linux o Windows (+1)")

        if res.get("mv_escalamiento_predictivo") == "Sí":
            for p in ["AWS", "GCP"]:
                scores[p] += 1
                razones[p].append("Escalamiento predictivo (+1)")

        if res.get("mv_autoescalamiento") == "Sí":
            for p in PROVEEDORES:
                scores[p] += 1
                razones[p].append("Autoescalamiento (+1)")

        if res.get("mv_hibernacion") == "Sí":
            for p in ["AWS", "GCP"]:
                scores[p] += 1
                razones[p].append("Hibernación o suspensión (+1)")

    # --- CONTENEDORES ---
    if res.get("contenedores") == "Sí":
        scores["GCP"] += 1
        razones["GCP"].append("Contenedores/Kubernetes (+1)")

    # --- ALMACENAMIENTO ---
    #razones[p].append(f"Almacenamiento de {tipo.lower()} (+1)")

    # --- BASES DE DATOS ---
    if res.get("bd_requiere") == "Sí":
        if res.get("bd_tipo") == "Relacional":
            motor = res.get("bd_motor")
            if motor == "MySQL":
                scores["AWS"] += 1
                scores["Azure"] += 1
                razones["AWS"].append("Motor MySQL (+1)")
                razones["Azure"].append("Motor MySQL (+1)")
            elif motor in ["SQL Server", "PostgreSQL"]:
                for p in ["AWS", "GCP", "Azure"]:
                    scores[p] += 1
                    razones[p].append(f"Motor {motor} (+1)")
            if res.get("bd_escalabilidad_rel") in ["Horizontal", "Vertical"]:
                for p in PROVEEDORES:
                    scores[p] += 1
                    razones[p].append("Escalabilidad BD relacional (+1)")

        elif res.get("bd_tipo") == "No relacional":
            tipo_esc = res.get("bd_escalabilidad_no_rel")
            if tipo_esc == "Escalabilidad automática con ajuste de capacidad":
                for p in PROVEEDORES:
                    scores[p] += 1
                    razones[p].append("Escalabilidad automática con ajuste de capacidad (+1)")
            elif tipo_esc == "Escalabilidad automática con réplicas de lectura":
                scores["AWS"] += 1
                razones["AWS"].append("Réplicas de lectura en BD no relacional (+1)")
            elif tipo_esc == "Escalabilidad horizontal con fragmentación automática":
                for p in ["AWS", "GCP"]:
                    scores[p] += 1
                    razones[p].append("Fragmentación automática BD no relacional (+1)")

    # --- IA / ML ---
    if res.get("ia_requiere") == "Sí":
        tipo = res.get("ia_tipo")
        if tipo == "Uso general":
            for p in PROVEEDORES:
                scores[p] += 1
                razones[p].append("IA/ML general (+1)")
            if res.get("presupuesto", 3) <= 2:
                scores["GCP"] += 1
                razones["GCP"].append("IA general + presupuesto bajo (+1)")
        elif tipo == "Especializado":
            esp = res.get("ia_servicios_especializados")
            if esp == "Reconocimiento de voz":
                if res.get("voz_idiomas") == "Sí":
                    for p in ["Azure", "GCP"]:
                        scores[p] += 1
                        razones[p].append("Reconocimiento de voz multilenguaje (+1)")
                else:
                    for p in PROVEEDORES:
                        scores[p] += 1
                        razones[p].append("Reconocimiento de voz inglés (+1)")
            elif esp == "Convertir Texto a Voz":
                if res.get("voz_clonacion") == "Sí":
                    for p in ["Azure", "GCP"]:
                        scores[p] += 1
                        razones[p].append("Clonación de voz (+1)")
                    if res.get("voz_naturalidad") == "Muy natural":
                        scores["Azure"] += 1
                        razones["Azure"].append("Voz muy natural (+1)")
                    elif res.get("voz_naturalidad") == "Medianamente natural":
                        scores["GCP"] += 1
                        razones["GCP"].append("Voz medianamente natural (+1)")
                    elif res.get("voz_naturalidad") == "Poco natural":
                        scores["AWS"] += 1
                        razones["AWS"].append("Voz poco natural (+1)")
            elif esp == "Visión":
                if res.get("vision_lugares") == "Sí":
                    scores["GCP"] += 1
                    razones["GCP"].append("Reconocimiento de lugares emblemáticos (+1)")
                if res.get("vision_celebridades") == "Sí":
                    scores["AWS"] += 1
                    razones["AWS"].append("Reconocimiento de celebridades (+1)")
            elif esp == "Procesamiento de lenguaje natural":
                if res.get("pln_analisis") == "Sí":
                    scores["GCP"] += 1
                    razones["GCP"].append("Análisis avanzado de texto (+1)")
            elif esp == "Traducción":
                if res.get("traduccion_personalizada") == "Sí":
                    for p in ["Azure", "GCP"]:
                        scores[p] += 1
                        razones[p].append("Modelos personalizados de traducción (+1)")

    # --- PRIORIDADES ---
    costo = res.get("presupuesto", 3)
    if costo <= 2:
        scores["GCP"] += 1
        razones["GCP"].append("Costo bajo: GCP destacado. Ofrece créditos gratuitos de $300 USD.(+1)")
    elif costo >= 4:
        scores["AWS"] += 1
        razones["AWS"].append("Costo alto: AWS (+1)")

    disponibilidad = res.get("disponibilidad", 3)
    if disponibilidad >= 3:
        scores["AWS"] += 1
        razones["AWS"].append("Alta disponibilidad: AWS (+1)")

    confidencialidad = res.get("confidencialidad", 3)
    if confidencialidad >= 4:
        scores["Azure"] += 1
        razones["Azure"].append("Alta confidencialidad: Azure (+1)")
        scores["GCP"] += 1
        razones["GCP"].append("Alta confidencialidad: GCP (+1)")

    # Aplicar reglas combinadas
    res_for_reglas = res.copy()
    res_for_reglas["costo"] = res.get("costo_texto")
    res_for_reglas["disponibilidad"] = res.get("disponibilidad_texto")
    res_for_reglas["confidencialidad"] = res.get("confidencialidad_texto")
    aplicar_reglas_combinacionales(res_for_reglas, scores, razones)

    return scores, razones
# Función para obtener servicios detallados
ruta_servicios = os.path.join(os.path.dirname(__file__), "servicios.json")
with open(ruta_servicios, "r", encoding="utf-8") as f:
    SERVICIOS = json.load(f)

def construir_servicio_detallado(nombre, proveedor):
    for categoria in SERVICIOS[proveedor]:
        subcat = SERVICIOS[proveedor][categoria]
        if isinstance(subcat, dict):
            for tipo in subcat:
                for s in subcat[tipo]:
                    if isinstance(s, dict) and s.get("nombre") == nombre:
                        return s
        elif isinstance(subcat, list):
            for s in subcat:
                if isinstance(s, dict) and s.get("nombre") == nombre:
                    return s
    return {"nombre": nombre}

def obtener_servicios_relevantes(respuestas, proveedor):
    relevantes = []
    if respuestas.get("mv_requiere") == "Sí":
        relevantes.extend(SERVICIOS[proveedor].get("mv", []))

    tipo_alm = respuestas.get("almacenamiento", "").lower()
    if tipo_alm in SERVICIOS[proveedor].get("almacenamiento", {}):
        relevantes.extend(SERVICIOS[proveedor]["almacenamiento"][tipo_alm])

    if respuestas.get("bd_requiere") == "Sí":
        tipo_bd = respuestas.get("bd_tipo")
        if tipo_bd == "Relacional":
            relevantes.extend(SERVICIOS[proveedor]["bd"].get("relacional", []))
        elif tipo_bd == "No relacional":
            relevantes.extend(SERVICIOS[proveedor]["bd"].get("no_relacional", []))

    if respuestas.get("ia_requiere") == "Sí":
        ia_data = SERVICIOS[proveedor].get("ia", {})
        if respuestas.get("ia_tipo") == "Uso general":
            relevantes.extend(ia_data.get("general", []))
        elif respuestas.get("ia_tipo") == "Especializado":
            mapa_claves = {
                "Reconocimiento de voz": "voz",
                "Convertir Texto a Voz": "texto_a_voz",
                "Visión": "vision",
                "Procesamiento de lenguaje natural": "pln",
                "Traducción": "traduccion"
            }
            seleccion = respuestas.get("ia_servicios_especializados", "")
            clave = mapa_claves.get(seleccion)
            if clave:
                lista = ia_data.get(clave)
                if isinstance(lista, list):
                    for nombre in lista:
                        relevantes.append(construir_servicio_detallado(nombre, proveedor))
    return relevantes
