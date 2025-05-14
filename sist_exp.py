# from libs.experta.experta import *
from experta import Fact, KnowledgeEngine, Rule, Field, AS

import sys
import os

# Asegura que la versión local se cargue primero
ruta_local = os.path.abspath("libs/experta")
if ruta_local not in sys.path:
    sys.path.insert(0, ruta_local)

class Sintomas(Fact):
    """Clase que representa los sintomas reportados por el paciente"""
    pass

class DiagnosticoMedico(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.diagnostico_realizado = False  # Flag para evitar diagnóstico desconocido si ya hay uno válido
        self.evaluacion_final = False  # Nuevo atributo

    @Rule(Sintomas(fiebre=True, tos=True, dolor_garganta=True, congestion_nasal=True), salience=5)
    def diagnostico_gripe(self):
        print("🩺 Diagnóstico: Posible GRIPE. Se recomienda reposo e hidratación.")
        self.diagnostico_realizado = True

    @Rule(Sintomas(fiebre=True, tos=True, dificultad_respirar=True, perdida_olfato=True), salience=10)
    def diagnostico_covid(self):
        print("⚠️ Diagnóstico: Posible COVID-19. Consulte a un médico y hágase una prueba.")
        self.diagnostico_realizado = True

    @Rule(Sintomas(fiebre=True, dolor_cabeza=True, dolor_muscular=True, sarpullido=False), salience=8)
    def diagnostico_dengue(self):
        print("🚨 Diagnóstico: Posible DENGUE. Consulte a un médico de inmediato.")
        self.diagnostico_realizado = True

    @Rule(Sintomas(fiebre=True, tos=True, dolor_pecho=True, dificultad_respirar=True), salience=9)
    def diagnostico_neumonia(self):
        print("⚠️ Diagnóstico: Posible NEUMONÍA. Se recomienda una evaluación médica urgente.")
        self.diagnostico_realizado = True

    @Rule(Sintomas(dolor_cabeza=True, sensibilidad_luz=True, nauseas=True), salience=6)
    def diagnostico_migraña(self):
        print("🧠 Diagnóstico: Posible MIGRAÑA. Evite la luz fuerte y descanse.")
        self.diagnostico_realizado = True

    # @Rule(AS.fact << Sintomas(), salience=1)
    # def diagnostico_desconocido(self, fact):
    #     if not self.diagnostico_realizado:  # Solo se muestra si no hubo diagnóstico
    #         print("❓ No se encontró un diagnóstico claro. Consulte con un médico para más información.")
    #         print(f"📌 Hechos insertados en el motor: {fact}")
    @Rule(AS.fact << Sintomas(), salience=1)
    def diagnostico_desconocido(self, fact):
        if not self.diagnostico_realizado and self.evaluacion_final:
            print("❓ No se encontró un diagnóstico claro. Consulte con un médico para más información.")
            print(f"📌 Hechos insertados en el motor: {fact}")

# 🏥 FUNCION PRINCIPAL

def ejecutar_diagnostico():
    motor = DiagnosticoMedico()
    sintomas_usuario = {}

    lista_sintomas = [
        ("fiebre", "¿Tienes fiebre? (si/no): "),
        ("tos", "¿Tienes tos? (si/no): "),
        ("dolor_garganta", "¿Te duele la garganta? (si/no): "),
        ("congestion_nasal", "¿Tienes congestión nasal? (si/no): "),
        ("dificultad_respirar", "¿Tienes dificultad para respirar? (si/no): "),
        ("perdida_olfato", "¿Perdiste el olfato? (si/no): "),
        ("dolor_cabeza", "¿Tienes dolor de cabeza? (si/no): "),
        ("dolor_muscular", "¿Te duelen los músculos? (si/no): "),
        ("sarpullido", "¿Tienes sarpullido? (si/no): "),
        ("dolor_pecho", "¿Sientes dolor en el pecho? (si/no): "),
        ("sensibilidad_luz", "¿Te molesta la luz? (si/no): "),
        ("nauseas", "¿Tienes náuseas? (si/no): ")
    ]

    for clave, pregunta in lista_sintomas:
        respuesta = input(pregunta).strip().lower()
        sintomas_usuario[clave] = (respuesta == "si")

        motor.reset()
        motor.evaluacion_final = False  # Evaluación intermedia
        motor.declare(Sintomas(**sintomas_usuario))
        motor.run()

        if motor.diagnostico_realizado:
            return  # Salimos si ya hubo diagnóstico

    # Si llegamos aquí, no hubo diagnóstico, hacer evaluación final
    motor.reset()
    motor.evaluacion_final = True
    motor.declare(Sintomas(**sintomas_usuario))
    motor.run()


# Ejecutar el sistema experto
if __name__ == "__main__":
    ejecutar_diagnostico()
