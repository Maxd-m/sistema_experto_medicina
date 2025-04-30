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

    @Rule(AS.fact << Sintomas(), salience=1)
    def diagnostico_desconocido(self, fact):
        if not self.diagnostico_realizado:  # Solo se muestra si no hubo diagnóstico
            print("❓ No se encontró un diagnóstico claro. Consulte con un médico para más información.")
            print(f"📌 Hechos insertados en el motor: {fact}")

# 🏥 FUNCION PRINCIPAL
def ejecutar_diagnostico():
    motor = DiagnosticoMedico()
    motor.reset()
    print("Usando Fact desde:", Fact.__module__)

    # Pedir sintomas al usuario
    # creo que aqui es donde se deberia implemenar el arbol/red para que no haga todas las preguntas
    sintomas_usuario = {
        "fiebre": input("¿Tienes fiebre? (si/no): ").strip().lower() == "si",
        "tos": input("¿Tienes tos? (si/no): ").strip().lower() == "si",
        "dolor_garganta": input("¿Te duele la garganta? (si/no): ").strip().lower() == "si",
        "congestion_nasal": input("¿Tienes congestión nasal? (si/no): ").strip().lower() == "si",
        "dificultad_respirar": input("¿Tienes dificultad para respirar? (si/no): ").strip().lower() == "si",
        "perdida_olfato": input("¿Perdiste el olfato? (si/no): ").strip().lower() == "si",
        "dolor_cabeza": input("¿Tienes dolor de cabeza? (si/no): ").strip().lower() == "si",
        "dolor_muscular": input("¿Te duelen los músculos? (si/no): ").strip().lower() == "si",
        "sarpullido": input("¿Tienes sarpullido? (si/no): ").strip().lower() == "si",
        "dolor_pecho": input("¿Sientes dolor en el pecho? (si/no): ").strip().lower() == "si",
        "sensibilidad_luz": input("¿Te molesta la luz? (si/no): ").strip().lower() == "si",
        "nauseas": input("¿Tienes náuseas? (si/no): ").strip().lower() == "si"
    }

    # Insertar hechos en el sistema
    # print(f"\n🔎 Hechos insertados en el sistema: {sintomas_usuario}\n")
    motor.declare(Sintomas(**sintomas_usuario))

    # Ejecutar motor de reglas
    motor.run()

# Ejecutar el sistema experto
if __name__ == "__main__":
    ejecutar_diagnostico()
