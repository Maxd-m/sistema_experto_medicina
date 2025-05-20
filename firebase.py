import firebase_admin
from firebase_admin import credentials, db

class DiagnosticoDB:
    def __init__(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate("key.json")
            firebase_admin.initialize_app(cred)

    def leer_diagnosticos(self, rama: str) -> dict:
        ref = db.reference(rama)
        datos = ref.get()
        return datos if datos else {}

    def guardar_diagnosticos(self, rama: str, data: dict):
        ref = db.reference(rama)
        ref.set(data)

    def adicionar_diagnostico(self, rama: str, nombre_diag: str, sintomas):
        ref = db.reference(f"{rama}/{nombre_diag}")
        ref.set(sintomas)

    def agregar_variante_completa(self, nombre_diag: str, sintomas_variante: set):
        ref_base = db.reference(f"diagnosticos_base/{nombre_diag}")
        base = ref_base.get()

        if base is None:
            raise ValueError(f"No se encontró la base para el diagnóstico '{nombre_diag}'.")

        set_base = set(base)
        variante_completa = set_base | sintomas_variante
        variante_lista = list(variante_completa)

        ref_def = db.reference(f"diagnosticos_definidos/{nombre_diag}")
        variantes = ref_def.get()

        if variantes is None:
            variantes = []

        if variante_lista not in variantes:
            variantes.append(variante_lista)
            ref_def.set(variantes)
        else:
            print("La variante ya existe.")