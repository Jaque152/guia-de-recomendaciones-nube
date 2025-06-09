# -*- coding: utf-8 -*-
"""
Reglas combinacionales estructuradas para proveedores de nube.
Cada regla incluye condiciones explícitas que deben cumplirse en el cuestionario.
"""

reglas_combinacionales = [
    ##------------MV---------------##
    {
        "condiciones": {
            "costo_texto": "Bajo",
            "mv_tipo": "Optimización de CPU"
        },
        "proveedor": "Azure",
        "descripcion": "Azure tiene mejores precios en MV CPU-Optimized con núcleos físicos",
        "puntos": 1
    },
    {
        "condiciones": {
            "costo_texto": "Bajo",
            "mv_tipo":"Propósito General"
        },
        "proveedor": "GCP",
        "descripcion": "GCP ofrece instancias Spot VMs con precios bajos y créditos iniciales de $300 USD duarante 90 días ",
        "puntos": 1
    },
    {
        "condiciones": {
            "mv_tipo": "Optimización de memoria",
            "mv_sistemas": "Linux"
        },
        "proveedor": "Azure",
        "descripcion": "Azure ofrece instancias de alta memoria para Linux, ideales para cargas analíticas, bases de datos y SAP.",
        "puntos": 1
    },
    {
        "condiciones": {
            "mv_tipo": "Optimización de memoria",
            "mv_sistemas": "Windows"
        },
        "proveedor": "AWS",
        "descripcion": "AWS ofrece instancias que soportan Windows y son recomendadas para cargas de alto consumo de memoria.",
        "puntos": 1
    },
    {
        "condiciones": {
            "mv_tipo": "Aceleradas por GPU",
            "mv_sistemas": "Linux"
        },
        "proveedor": "AWS",
        "descripcion": "AWS tiene una amplia gama de instancias GPU para Linux (g5, p4) ideales para ML, rendering y simulación científica.",
        "puntos": 1
    },
    {
        "condiciones": {
            "mv_tipo": "Optimización de almacenamiento",
            "mv_sistemas": "Windows"
        },
        "proveedor": "GCP",
        "descripcion": "GCP ofrece almacenamiento local SSD con alto rendimiento para Windows, útil en cargas intensivas de lectura/escritura.",
        "puntos": 1
    },
    {
        "condiciones": {
            "mv_tipo": "Optimización de almacenamiento",
            "costo_texto": "Alto",
            "confidencialidad_texto": "Alta"
        },
        "proveedor": "AWS",
        "descripcion": "AWS ofrece instancias con discos cifrados por hardware y doble capa KMS-SSM, ideales cuando el nivel de costos permite máxima protección.",
        "puntos": 1
    },
     {
        "condiciones": {
            "confidencialidad_texto": "Alta",
            "mv_tipo": "Optimización de almacenamiento"
        },
        "proveedor": "AWS",
        "descripcion": "Las instancias con discos NVMe en AWS cifran los datos en reposo mediante XTS-AES-256 en módulos de hardware con claves efímeras únicas que se destruyen al apagar la instancia.",
        "puntos": 1
    },
    {
        "condiciones": {
            "mv_requiere": "Sí",
            "confidencialidad_texto": [
                "Media",
                "Alta"
            ]
        },
        "proveedor": "Azure",
        "descripcion": "Puede habilitar el cifrado en reposo en sus máquinas virtuales Linux y Windows y discos duros virtuales (VHD) alojados en Azure mediante Azure Disk Encryption",
        "puntos": 1

    },
    {
        "condiciones": {
            "confidencialidad_texto": "Alta",
            "mv_tipo": "Optimización de memoria"
        },
        "proveedor": [
            "GCP",
            "Azure"
        ],
        "descripcion": "GCP ofrece Confidential VMs y Azure permite Always Encrypted en VMs optimizadas, ideales para cargas sensibles en memoria",
        "puntos": 1
    },
    ##-------------------------------------------------------------------------------------------------------
    ##----------------CONTENEDORES-------------------------------
    {
        "condiciones": {
            "contenedores": "Sí", 
            "confidencialidad_texto": ["Alta", "Media"]
        },
        "proveedor": "GCP",
        "descripcion": "Google Kubernetes Engine (GKE) admite claves de cifrado administradas por el usuario, VPC Service Controls e integración con IAM para garantizar confidencialidad elevada.",
        "puntos": 1
    },
    {
        "condiciones": {
            "contenedores": "Sí", 
            "confidencialidad_texto": ["Alta", "Media"]
        },
        "proveedor": "Azure",
        "descripcion": "Azure Kubernetes Service (AKS) permite proteger datos mediante Azure Key Vault, control de acceso basado en roles (RBAC) y Azure Active Directory para gestionar los usuarios y el acceso a recursos.",
        "puntos": 1
    },
    {
        "condiciones": {
            "contenedores": "Sí", 
            "confidencialidad_texto": ["Alta", "Media"]
        },
        "proveedor": "AWS",
        "descripcion": "Elastic Kubernetes Service (EKS) soporta cifrado con AWS KMS e IAM Roles for Service Accounts (IRSA) para control de accesos.",
        "puntos": 1
    },
    {
        "condiciones": {
            "contenedores": "Sí", 
            "confidencialidad_texto": "Media"},
        "proveedor": "GCP",
        "descripcion": "Google Kubernetes Engine (GKE) cifra datos en reposo de forma predeterminada, con control de acceso mediante IAM.",
        "puntos": 1
    },
    {
        "condiciones": {
            "contenedores": "Sí", 
            "confidencialidad_texto": "Media"},
        "proveedor": "Azure",
        "descripcion": "Azure Kubernets Services (AKS) proporciona cifrado estándar y control de acceso basado en roles (RBAC).",
        "puntos": 1
    },
    {
        "condiciones": {
            "contenedores": "Sí", 
            "confidencialidad_texto": "Media"},
        "proveedor": "AWS",
        "descripcion": "Elastic Kubernetes Service (EKS) cifra recursos básicos con KMS y configura IAM sin políticas avanzadas.",
        "puntos": 1
    },
    {
        "condiciones": {
            "contenedores": "Sí", 
            "confidencialidad_texto": "Baja"},
        "proveedor": "GCP",
        "descripcion": "Google Kubernetes Engine (GKE) en modo estándar usa claves gestionadas por Google sin configuración personalizada",
        "puntos": 1
    },
    {
        "condiciones": {
            "contenedores": "Sí", 
            "confidencialidad_texto": "Baja"},
        "proveedor": "Azure",
        "descripcion": "Azure Kubernets Services (AKS) permite cifrado básico con claves gestionadas por Microsoft.",
        "puntos": 1
    },
    {
        "condiciones": {
            "contenedores": "Sí", 
            "confidencialidad_texto": "Baja"},
        "proveedor": "AWS",
        "descripcion": "Elastic Kubernetes Service (EKS) ofrece cifrado predeterminado sin necesidad de configurar KMS.",
        "puntos": 1
    },
   {
        "condiciones": {
            "contenedores": "Sí", 
            "costo_texto": "Bajo"},
        "proveedor": "Azure",
        "descripcion": "AKS permite plan gratuito en el plano de control; es decir, no cobra la gestión central a diferencia de GKE y soporta nodos spot para reducir costos de ejecución.",
        "puntos": 1
    },

    ##-----------------------------------------------------------
    ##----------------ALMACENAMIENTO-----------------------------
    {
        "condiciones": {
            "confidencialidad_texto":"Alta",
            "almacenamiento":"Objetos"
        },
        "proveedor": "AWS",
        "descripcion": "AWS permite doble capa de cifrado (DSSE-KMS) con claves personalizadas",
        "puntos": 1
    },
    {
        "condiciones": {
            "disponibilidad_texto":"Alta",
            "almacenamiento":"Objetos"
        },
        "proveedor": "Azure",
        "descripcion": "Azure Blob Storage soporta replicación geográfica activa (RA-GRS) y rendimiento escalable",
        "puntos": 1
    },
    {
        "condiciones": {
            "confidencialidad_texto":"Alta",
            "almacenamiento":"Archivos",
        },
        "proveedor": "GCP",
        "descripcion": "Cifrado en reposo, permite integración con Cloud KMS para claves de cifrado gestionadas por el cliente",
        "puntos": 1
    },
    {
        "condiciones": {
            "confidencialidad_texto":"Alta",
            "almacenamiento":"Bloques"
        },
        "proveedor": "Azure",
        "descripcion": "Cuenta con Azure Disk Encryption",
        "puntos": 1
    },
    ##------------------------------------------------------------------------------
    ##---------------------BASES DE DATOS ------------------------------------------
    {
        "condiciones": {
            "bd_tipo": "Relacional",
            "bd_motor_relacional": "Oracle",
            "costo_texto": "Medio"
        },
        "proveedor": "AWS",
        "descripcion": "AWS RDS soporta más motores incluyendo Oracle ",
        "puntos": 1
    },
    {
        "condiciones": {
            "confidencialidad_texto": "Alta",
            "bd_tipo": "Relacional"
        },
        "proveedor": "Azure",
        "descripcion": "Azure SQL Database implementa Always Encrypted y permite el control completo de claves mediante Key Vault.",
        "puntos": 1
    },
    {
        "condiciones": {
            "confidencialidad_texto": "Media",
            "disponibilidad_texto":"Alta",
            "bd_tipo": "Relacional"
        },
        "proveedor": "Azure",
        "descripcion": "Azure SQL Database ofrece Always Encrypted y geo-replicación",
        "puntos": 1
    },
    {
        "condiciones": {
            "confidencialidad_texto": "Alta",
            "bd_tipo": "Relacional"
        },
        "proveedor": "AWS",
        "descripcion": "Amazon RDS permite cifrado en reposo mediante TDE (Transparent Data Encryption) y control de claves mediante KMS, asegurando confidencialidad avanzada.",
        "puntos": 1
    },
    {
        "condiciones": {
            "confidencialidad_texto": "Media",
            "bd_tipo": "Relacional",
            "costo_texto": "Bajo"
        },
        "proveedor": "GCP",
        "descripcion": "GCP cifra automáticamente los datos almacenados en Cloud SQL con AES-256, ideal para proyectos con un costo bajo que buscan protección estándar.",
        "puntos": 1
    },
    {
        "condiciones": {
            "bd_tipo": "No relacional",
            "confidencialidad_texto":"Alta"
        },
        "proveedor": "Azure",
        "descripcion": "Cifrado transparente de datos en reposo y en tránsito; además, cuenta con Azure Private Link y VNet service endpoints",
        "puntos": 1
    },
    {
        "condiciones": {
            "bd_tipo": "No relacional",
            "costo_texto": "Bajo"
        },
        "proveedor": "GCP",
        "descripcion": "Firestore de GCP ofrece autoajuste, modelo serverless y facturación por uso",
        "puntos": 1
    },
    
    ##------------------------------------------------------------------
    ##-------------INTELIGENCIA ARTIFICIAL------------------------------
    {
        "condiciones": {
            "confidencialidad_texto": "Alta",
            "ia_tipo": "Uso general"
        },
        "proveedor": "GCP",
        "descripcion": "Vertex AI soporta CMEK para proteger datos y modelos ML",
        "puntos": 1
    },
    {
        "condiciones": {
            "costo_texto": "Bajo",
            "vision_lugares": "Sí"
        },
        "proveedor": "GCP",
        "descripcion": "GCP ofrece OCR avanzado y 1000 imágenes gratis al mes",
        "puntos": 1
    },
    {
        "condiciones": {
            "disponibilidad_texto":"Alta",
            "ia_tipo": "Uso general"
        },
        "proveedor": "Azure",
        "descripcion": "Azure Machine Learning incluye AutoML y modelos híbridos replicables",
        "puntos": 1
    },
    {
        "condiciones": {
            "bd_requiere": "Sí",
            "bd_tipo":["No relacional"],
            "ia_requiere":"Sí",
            "ia_tipo": ["Uso general", "Especializado"],
            "integridad_texto":"Alta"
        },
        "proveedor": "GCP",
        "descripcion": "GCP es fuerte en soluciones de Big Data y análisis con servicios como BigQuery, Cloud Firestore/Bigtable, y Vertex AI, que garantizan la integridad de datos para cargas analíticas",
        "puntos": 1
    },
    ##--------------------------------------------------------------------------------------------------
    ##------------------------------WEB SCRAPING--------------------------------------------------------
    {
        "condiciones": {
            "scraping": "Sí",
            "disponibilidad_texto": "Alta"
        },
        "proveedor": "GCP",
        "descripcion": "Cloud Functions + Puppeteer junto con Cloud Scheduler garantizan ejecución escalable y continua.",
        "puntos": 1
    },
    {
        "condiciones": {
            "scraping": "Sí",
            "costo_texto": "Bajo"
        },
        "proveedor": "AWS",
        "descripcion": "AWS Lambda tiene costos bajos por ejecución, ideal para scraping ligero con Scrapy.",
        "puntos": 1
    },
   
    ##--------------------------------------------------------------------------------------------------
    ##------------------------------GENERALES-----------------------------------------------------------
    { "condiciones": {
            "disponibilidad_texto":"Alta",
            "costo_texto":"Alto"
        },
        "proveedor": "AWS",
        "descripcion": "AWS ofrece mayor disponibilidad al contar con más Zonas y Regiones",
        "puntos": 1
    },
    {
        "condiciones": {
            "confidencialidad_texto": "Media",
            "costo_texto": "Bajo"
        },
        "proveedor": "GCP",
        "descripcion": "GCP cifra automáticamente todos los datos en reposo mediante AES-256 y la biblioteca criptográfica Tink con validación FIPS 140-2, sin costo adicional ni configuración extra.",
        "puntos": 1
    },
    {
        "condiciones": {
            "costo_texto": "Alto",
            "confidencialidad_texto": "Alta",
            "disponibilidad_texto": "Alta"
        },
        "proveedor": "GCP",
        "descripcion": "GCP combina Confidential VMs, escalado global y precios competitivos",
        "puntos": 1
    },
    {
        "condiciones": {
            "costo_texto": "Medio",
            "confidencialidad_texto": "Media",
            "disponibilidad_texto": "Media"
        },
        "proveedor": "Azure",
        "descripcion": "Azure permite claves gestionadas por el cliente, geo-replicación y modelos de precios flexibles",
        "puntos": 1
    },
    {
        "condiciones": {
            "costo_texto": "Bajo",
            "confidencialidad_texto": "Baja",
            "disponibilidad_texto": "Baja"
        },
        "proveedor": [
            "AWS",
            "GCP"
        ],
        "descripcion": "Ambos ofrecen niveles gratuitos adecuados para entornos variados",
        "puntos": 1
    },
    {
        "condiciones": {
            "disponibilidad_texto": "Alta",
            "contenedores":"Sí"
        },
        "proveedor": "GCP",
        "descripcion": "GCP ofrece alta disponibilidad predeterminada en servicios regionales con replicación automática entre zonas.",
        "puntos": 1
    },
    {
        "condiciones": {
            "disponibilidad_texto": "Alta",
            "mv_requiere":"Sí"
        },
        "proveedor": "AWS",
        "descripcion": "AWS garantiza disponibilidad de 99.99 en EC2.",
        "puntos": 1
    },
    {
        "condiciones": {
            "disponibilidad_texto": "Alta",
            "bd_tipo":"Relacional"
        },
        "proveedor": "AWS",
        "descripcion": "AWS garantiza multizona en servicios críticos como RDS.",
        "puntos": 1
    },
    {
        "condiciones": {
            "disponibilidad_texto": "Alta",
            "contenedores":"Sí"
        },
        "proveedor": "AWS",
        "descripcion": "AWS garantiza multizona en servicios críticos como Elastic Kubernets Services (EKS).",
        "puntos": 1
    },
    {
        "condiciones": {
            "disponibilidad_texto": "Alta"
        },
        "proveedor": "Azure",
        "descripcion": "Azure asegura 99.95% de disponibilidad en servicios con respaldo zonal como AKS y SQL Database.",
        "puntos": 1
    },
    ##---------------------------------------------------------------------------------------------
    ##-------------------INTEGRIDAD-------------------------------------##
    
    {
        "condiciones": {
            "mv_requiere": "Sí",
            "bd_requiere": "Sí",
            "bd_tipo": "Relacional",
            "integridad_texto": "Alta"
        },
        "proveedor": "Azure",
        "descripcion": "Si se ejecuta SQL Server sobre una VM en Azure, puede configurarse Always Encrypted con integración a Key Vault.",
        "puntos": 1
    },
    {
        "condiciones": {
            "mv_requiere": "Sí",
            "integridad_texto": ["Media", "Alta"]
        },
        "proveedor": "Azure",
        "descripcion": "Las máquinas virtuales en redes privadas pueden integrarse con Key Vault para gestionar claves y validar la integridad del acceso.",
        "puntos": 1
    },
    {
        "condiciones": {
            "almacenamiento": "Archivos",
            "integridad_texto": "Alta"
        },
        "proveedor": ["Azure", "AWS"],
        "descripcion": "Azure Files y Amazon EFS soportan snapshots consistentes y validación POSIX para asegurar integridad de archivos.",
        "puntos": 1
    },
    {
        "condiciones": {
            "bd_no_relacional": "Sí",
            "integridad_texto": ["Media", "Alta"]
        },
        "proveedor": ["GCP", "AWS", "Azure"],
        "descripcion": "Servicios como DynamoDB, Cosmos DB y Firestore ofrecen consistencia eventual o fuerte, backups consistentes y validación interna de integridad.",
        "puntos": 1
    }, 
    {
        "condiciones": {
            "ia_tipo": "Uso general",
            "integridad_texto": "Alta"
        },
        "proveedor": ["AWS", "Azure", "GCP"],
        "descripcion": "SageMaker, Vertex AI y Azure ML permiten trazabilidad completa de modelos, validación de datasets y auditoría de procesos de entrenamiento.",
        "puntos": 1
    },
    {
        "condiciones": {
            "almacenamiento": "Objetos",
            "integridad_texto": "Alta"
        },
        "proveedor": "AWS",
        "descripcion": "AWS S3 Object Lock proporciona un modelo WORM (Write-Once-Read-Many) para garantizar la inmutabilidad y la integridad de los datos.",
        "puntos": 1
    },
    ##---------------------------------------------------------------------------------------------
    ##-------------------Reglas de advertencia--------------------------##
    {
        "condiciones": {
            "mv_tipo":"Aceleradas por GPU",
            "mv_sistemas": "Windows"
        },
        "proveedor": [
            "GCP",
            "Azure",
            "AWS"
        ],
        "descripcion": "Windows es soportado, pero requiere drivers específicos y configuración manual.",
        "puntos": 0
    },
    {
        "condiciones": {
            "mv_sistemas": "MacOs"
        },
        "proveedor": [
            "GCP",
            "Azure"
        ],
        "descripcion": "Tenga en cuenta que solo AWS ofrece instancias nativas con soporte para macOS.",
        "puntos": 0
    },
    {
        "condiciones": {
            "mv_tipo": "Optimización de CPU",
            "mv_sistemas": "MacOs"
        },
        "proveedor": [
            "AWS",
            "GCP",
            "Azure"
        ],
        "descripcion": "No se pueden ejecutar MVs de optimización de CPU con MacOS. MacOS solo está disponible en instancias dedicadas para desarrollo Apple.",
        "puntos": 0
    },
    {
        "condiciones": {
            "mv_tipo": "Aceleradas por GPU",
            "sistema_operativo": "MacOs"
        },
        "proveedor":[
            "AWS",
            "GCP",
            "Azure"
        ],
        "descripcion": "Actualmente, no hay soporte para ejecutar MacOs en instancias GPU en ningún proveedor de nube.",
        "puntos": 0
    },
    {
        "condiciones": {
            "mv_tipo": "Optimización de almacenamiento",
            "mv_sistemas": "MacOs"
        },
        "proveedor": [
            "AWS",
            "GCP",
            "Azure"
        ],
        "descripcion": "MacOS solo puede ejecutarse en instancias específicas dedicadas. No es compatible con instancias optimizadas por almacenamiento.",
        "puntos": 0
    },
    {
        "condiciones": {
            "mv_sistemas": "MacOs",
            "mv_autoescalamiento": "Sí"
        },
        "proveedor": [
                "AWS",
                "GCP",
                "Azure"
            ],
        "descripcion": "Las instancias MacOs dedicadas en AWS no permiten autoescalamiento. Solo pueden ejecutarse de forma individual y estática.",
        "puntos": 0
    },
    {
        "condiciones": {
            "mv_tipo": "Aceleradas por GPU",
            "mv_autoescalamiento": "Sí"
        },
        "proveedor": [
                "AWS",
                "GCP",
                "Azure"
        ],
        "descripcion": "El autoescalamiento en instancias GPU no es eficiente ni recomendado",
        "puntos": 0 
    },
    {
        "condiciones": {
            "mv_tipo": "Optimización de almacenamiento",
            "mv_autoescalamiento": "Sí"
        },
        "proveedor": [
                "AWS",
                "GCP",
                "Azure"
        ],
        "descripcion": "Las instancias optimizadas para almacenamiento generalmente no escalan de forma automática debido a sus características dedicadas de disco.",
        "puntos": 0
    },
    {
        "condiciones": {
            "confidencialidad_texto": "Alta",
            "costo_texto": "Bajo"
        },
        "proveedor": ["AWS","GCP","Azure"],
        "descripcion": "Los servicios con confidencialidad avanzada suelen requerir configuración de claves propias, módulos de hardware especializados, lo cual eleva el costo. Se recomienda aumentar el nivel de costos.",
        "puntos": 0
    },
    {
        "condiciones":{
            "disponibilidad_texto": "Alta", 
            "costo_texto": "Bajo"
        },
        "proveedor": ["AWS","GCP","Azure"],
        "descripcion": "Lograr alta disponibilidad generalmente implica costos más altos por la redundancia de recursos. Es importante alinear el nivel de costos  con los requisitos de disponibilidad.",
        "puntos": 0

    },
    {
        "condiciones":{
            "enfoque_seguridad": [
                "Confidencialidad",
                "Ambos"
            ], 
            "mv_requiere": "No",
            "almacenamiento_requiere": "No",
            "bd_requiere":"No",
            "ia_requiere":"No",
            "scraping_requiere":"No"
        },
        "proveedor": ["AWS","GCP","Azure"],
        "descripcion": "Ha indicado un alto enfoque en confidencialidad, pero no ha seleccionado servicios clave donde esta característica es crítica.",
        "puntos": 0

    }
    
]

# def cumple_condicion_struct(res, condiciones):
#     return all(res.get(k) == v for k, v in condiciones.items())

def cumple_condicion_struct(res, condiciones):
    for k, v in condiciones.items():
        user_response = res.get(k)
        
        # Si la condición es una lista 
        if isinstance(v, list):
            # Comprueba si la respuesta del usuario está en esa lista
            if user_response not in v:
                return False
        # Si la respuesta del usuario es una lista 
        elif isinstance(user_response, list):
            # Comprueba si el valor requerido por la regla está en la lista de respuestas
            if v not in user_response:
                return False
        # Comparación simple
        else:
            if user_response != v:
                return False
    return True