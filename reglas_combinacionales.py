# -*- coding: utf-8 -*-
"""
Reglas combinacionales estructuradas para proveedores Cloud.
Cada regla incluye condiciones explícitas que deben cumplirse en el cuestionario.
"""

reglas_combinacionales = [
    {
        "condiciones": {
            "costo": "Bajo",
            "mv_tipo": "Optimización de CPU"
        },
        "proveedor": "Azure",
        "descripcion": "Azure tiene mejores precios en MV CPU-Optimized con núcleos físicos",
        "puntos": 1
    },
    {
        "condiciones": {
            "disponibilidad":"Alta"
            "costo":"Alto"
        },
        "proveedor": "AWS",
        "descripcion": "AWS ofrece mayor disponibilidad al contar con más Zonas y Regiones",
        "puntos": 1
    },
    {
        "condiciones": {
            "costo": "Bajo"
            "mv_tipo":"Uso General"
        },
        "proveedor": "GCP",
        "descripcion": "GCP ofrece instancias preemtibles (Spot VMs) con precios bajos y créditos iniciales de $300 USD duarante 90días ",
        "puntos": 1
    },
    {
        "condiciones": {
            "confidencialidad":"Alta",
            "almacenamiento":"Objetos"
        },
        "proveedor": "AWS",
        "descripcion": "AWS permite doble capa de cifrado (DSSE-KMS) con claves personalizadas",
        "puntos": 1
    },
    {
        "condiciones": {
            "disponibilidad":"Alta",
            "almacenamiento":"Objetos"
        },
        "proveedor": "Azure",
        "descripcion": "Azure Blob Storage soporta replicación geográfica activa (RA-GRS) y rendimiento escalable",
        "puntos": 1
    },
    {
        "condiciones": {
            "bd_tipo": "Relacional",
            "bd_motor_relacional": "Oracle",
            "costo": "Medio"
        },
        "proveedor": "AWS",
        "descripcion": "AWS RDS soporta más motores incluyendo Oracle y Aurora compatibles",
        "puntos": 1
    },
    {
        "condiciones": {
            "confidencialidad": "Media",
            "disponibilidad":"Alta",
            "bd_tipo": "Relacional"
        },
        "proveedor": "Azure",
        "descripcion": "Azure SQL Database ofrece Always Encrypted y geo-replicación",
        "puntos": 1
    },
    {
        "condiciones": {
            "bd_tipo": "No relacional",
            "bd_motor_norelacional": "DynamoDB",
            "escalabilidad": "Horizontal",
            "confidencialidad":"Alta"
        },
        "proveedor": "AWS",
        "descripcion": "AWS Keyspaces y DynamoDB ofrecen cifrado, IAM y replicación global",
        "puntos": 1
    },
    {
        "condiciones": {
            "bd_tipo": "No relacional",
            "costo": "Bajo"
        },
        "proveedor": "GCP",
        "descripcion": "Firestore de GCP ofrece autoajuste, modelo serverless y facturación por uso",
        "puntos": 1
    },
    {
        "condiciones": {
            "confidencialidad": "Alta",
            "ia_tipo": "Uso general"
        },
        "proveedor": "GCP",
        "descripcion": "Vertex AI soporta CMEK para proteger datos y modelos ML",
        "puntos": 1
    },
    {
        "condiciones": {
            "costo": "Bajo",
            "vision_lugares": "Sí"
        },
        "proveedor": "GCP",
        "descripcion": "GCP ofrece OCR avanzado y 1000 imágenes gratis al mes",
        "puntos": 1
    },
    {
        "condiciones": {
            "disponibilidad":"Alta",
            "ia_tipo": "Uso general"
        },
        "proveedor": "Azure",
        "descripcion": "Azure Machine Learning incluye AutoML y modelos híbridos replicables",
        "puntos": 1
    },
    {
        "condiciones": {
            "costo": "Alto",
            "confidencialidad": "Alta",
            "disponibilidad": "Alta"
        },
        "proveedor": "GCP",
        "descripcion": "GCP combina Confidential VMs, escalado global y precios competitivos",
        "puntos": 1
    },
    {
        "condiciones": {
            "costo": "Medio",
            "confidencialidad": "Media",
            "disponibilidad": "Media"
        },
        "proveedor": "Azure",
        "descripcion": "Azure permite claves gestionadas por el cliente, geo-replicación y modelos de precios flexibles",
        "puntos": 1
    },
    {
        "condiciones": {
            "costo": "Bajo",
            "confidencialidad": "Baja",
            "disponibilidad": "Baja"
        },
        "proveedor": "AWS y GCP",
        "descripcion": "Ambos ofrecen niveles gratuitos adecuados para entornos variados",
        "puntos": 1
    },
    {
        "condiciones": {
            "confidencialidad": "Alta",
            "mv_tipo": "Optimización de memoria"
        },
        "proveedor": [
            "GCP",
            "Azure"
        ],
        "descripcion": "GCP ofrece Confidential VMs y Azure permite Always Encrypted en VMs optimizadas, ideales para cargas sensibles en memoria",
        "puntos": 1
    }
]

def cumple_condicion_struct(res, condiciones):
    return all(res.get(k) == v for k, v in condiciones.items())
