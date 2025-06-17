
import unittest
from logica_cuestionario import (
    evaluar_respuestas,
    obtener_nivel_confidencialidad,
    obtener_servicios_relevantes,
    construir_servicio_detallado
)
from reglas_combinacionales import cumple_condicion_struct

class TestFuncionesUnitarias(unittest.TestCase):

    def test_evaluar_respuestas_mv_mac(self):
        res = {
            "mv_requiere": "Sí",
            "mv_sistemas": ["MacOs"],
            "mv_tipo": "Propósito General",
            "costo": 3,
            "disponibilidad": 3,
            "confidencialidad": 3,
            "enfoque_seguridad": "Confidencialidad"
        }
        scores, razones, _ = evaluar_respuestas(res)
        self.assertGreaterEqual(scores["AWS"], 1)
        self.assertTrue(any("MacOS" in r for r in razones["AWS"]))

    def test_cumple_condicion_struct_oracle(self):
        condiciones = {
            "bd_tipo": "Relacional",
            "bd_motor_relacional": "Oracle",
            "costo_texto": "Medio"
        }
        entrada = condiciones.copy()
        self.assertTrue(cumple_condicion_struct(entrada, condiciones))

    def test_obtener_nivel_confidencialidad_s3(self):
        niveles, max_nivel = obtener_nivel_confidencialidad("Amazon S3", "AWS", 3)
        self.assertEqual(max_nivel, 3)
        self.assertEqual(len(niveles), 3)
        for nivel in niveles:
            self.assertIn("reposo", nivel)
            self.assertIn("transito", nivel)

    def test_obtener_servicios_relevantes_cpu(self):
        respuestas = {
            "mv_requiere": "Sí",
            "mv_tipo": "Optimización de CPU"
        }
        servicios = obtener_servicios_relevantes(respuestas, "AWS")
        self.assertTrue(all(s["tipo"] == "Optimización de CPU" for s in servicios))

    def test_construir_servicio_detallado_s3(self):
        servicio = construir_servicio_detallado("Amazon S3", "AWS")
        self.assertEqual(servicio["nombre"], "Amazon S3")
        self.assertIn("costo_aproximado", servicio)
        self.assertIn("regiones_disponibles", servicio)

if __name__ == "__main__":
    unittest.main()
