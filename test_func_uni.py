
import unittest
from logica_cuestionario import (
    evaluar_respuestas,
    obtener_servicios_relevantes,
    construir_servicio_detallado
)
from reglas_combinacionales import cumple_condicion_struct

class TestFuncionesUnitarias(unittest.TestCase):

    def test_evaluar_respuestas(self):
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

    def test_regla_combinacional(self):
        res = {
            "bd_tipo": "Relacional",
            "bd_motor_relacional": "Oracle",
            "costo_texto": "Medio"
        }
        self.assertTrue(cumple_condicion_struct(res, {
            "bd_tipo": "Relacional",
            "bd_motor_relacional": "Oracle",
            "costo_texto": "Medio"
        }))

    def test_servicios_relevantes(self):
        res = {
            "mv_requiere": "Sí",
            "mv_tipo": "Optimización de CPU"
        }
        servicios = obtener_servicios_relevantes(res, "AWS")
        self.assertTrue(any("Optimización de CPU" in s["tipo"] for s in servicios))

    def test_construir_servicio(self):
        servicio = construir_servicio_detallado("Amazon S3", "AWS")
        self.assertEqual(servicio["nombre"], "Amazon S3")
        self.assertIn("costo_aproximado", servicio)

if __name__ == '__main__':
    unittest.main()
