from experta import *
from collections import Counter

class Sintomas(Fact): pass

class DiagnosticoMedico(KnowledgeEngine):
    def __init__(self, diagnosticos_base, diagnosticos_definidos):
        super().__init__()
        self.sintomas_usuario = {}
        self.diagnosticos_base = diagnosticos_base
        self.diagnosticos_definidos = diagnosticos_definidos
        self.diagnosticos_posibles = set(diagnosticos_definidos.keys())
        self.diagnostico_realizado = False
        self.sintomas = set()

    def set_sintomas(self):
        todos = set()
        for variantes in self.diagnosticos_definidos.values():
            for sintoma in variantes:
                todos.update(sintoma)
        self.sintomas = todos

    def siguiente_sintoma_a_preguntar(self):
        sintomas_base_faltantes = set()
        sintomas_variante_faltantes = []

        sintoma_ocurrencias = Counter()

        for diag in self.diagnosticos_posibles:
            base = self.diagnosticos_base.get(diag, set())
            for sintoma in base:
                if sintoma not in self.sintomas_usuario:
                    sintomas_base_faltantes.add(sintoma)
                    sintoma_ocurrencias[sintoma] += 1

            for variante in self.diagnosticos_definidos.get(diag, []):
                for sintoma in variante:
                    if sintoma not in self.sintomas_usuario:
                        sintomas_variante_faltantes.append(sintoma)
                        sintoma_ocurrencias[sintoma] += 1

        if sintomas_base_faltantes:
            # Ordenar por rareza (menos diagnósticos lo tienen → más discriminante)
            ordenados = sorted(sintomas_base_faltantes, key=lambda s: sintoma_ocurrencias[s])
            return ordenados
        else:
            ordenados = sorted(set(sintomas_variante_faltantes), key=lambda s: sintoma_ocurrencias[s])
            return ordenados

    def preguntar_sintoma(self, sintoma):
        respuesta = input(f"¿Tienes {sintoma.replace('_', ' ')}? (s/n): ").lower()
        self.sintomas_usuario[sintoma] = respuesta == "s"

    def diagnosticos_por_sintomas(self, sintomas_afirmados: set):
        posibles = set()
        for diag, variantes in self.diagnosticos_definidos.items():
            for variante in variantes:
                if variante.issubset(sintomas_afirmados):
                    posibles.add(diag)
                    break
        return posibles

    def filtrar_diagnostico_tollens(self):
        nuevos_posibles = set()

        for diag, variantes_sintomas in self.diagnosticos_definidos.items():
            base = self.diagnosticos_base[diag]
            if any(s in self.sintomas_usuario and self.sintomas_usuario[s] is False for s in base):
                continue

            sintomas_negados = {s for s, v in self.sintomas_usuario.items() if v is False}

            variante_valida = False
            for variante in variantes_sintomas:
                if variante.isdisjoint(sintomas_negados):
                    variante_valida = True
                    break

            if not variante_valida:
                continue

            nuevos_posibles.add(diag)

        print(nuevos_posibles)
        self.diagnosticos_posibles = nuevos_posibles

    def filtrar_diagnosticos_ponens(self, immediate = False):
        nuevos_posibles = set()

        if not immediate:
            sintomas_reportados = self.sintomas_usuario
        else:
            sintomas_reportados = immediate

        for diag, variantes_sintomas in self.diagnosticos_definidos.items():
            base = self.diagnosticos_base[diag]
            if any(s in self.sintomas_usuario and self.sintomas_usuario[s] is False for s in base):
                continue

            sintomas_extra_afirmados = {s for s, v in self.sintomas_usuario.items() if v is True and s not in base}

            # 3. Verificar variantes válidas
            og_sintomas_extra_afirmados = sintomas_extra_afirmados
            for variante in variantes_sintomas:
                variante_valida = {s for s in variante if s not in base}
                if variante_valida.issubset(og_sintomas_extra_afirmados):
                    sintomas_extra_afirmados -= variante

            if len(sintomas_extra_afirmados) > 0:
                continue

            nuevos_posibles.add(diag)

        print(nuevos_posibles)
        self.diagnosticos_posibles = nuevos_posibles

    @Rule(AS.fact << Sintomas())
    def evaluar_diagnostico(self, fact):
        #self.filtrar_diagnostico_ponens() #para hard filtering
        self.filtrar_diagnostico_tollens() #como trabaja porlog

        if len(self.diagnosticos_posibles) == 0:
            print("No se encontró un diagnóstico claro.")
            self.diagnostico_realizado = True
        elif not self.siguiente_sintoma_a_preguntar():
            valid = False
            aux = {i for i in self.diagnosticos_posibles}
            for diag in aux:
                sintomas_extra = {s for s, v in self.sintomas_usuario.items() if v is True and s not in self.diagnosticos_base[diag]}
                if len(sintomas_extra) == 0:
                    for variante in self.diagnosticos_definidos[diag]:
                        variante_valida = {s for s in variante if s not in self.diagnosticos_base[diag]}
                        if len(variante_valida) == 0:
                            valid = True
                            break
                if len(sintomas_extra) == 0 and not valid:
                    self.diagnosticos_posibles.remove(diag)

            if len(self.diagnosticos_posibles) == 0:
                print("No se encontró un diagnóstico claro.")
            elif len(self.diagnosticos_posibles) == 1:
                diag = list(self.diagnosticos_posibles)[0]
                print(f"Diagnóstico probable: {diag.upper()}")
            else:
                print(f"Posibles diagnósticos: {', '.join(self.diagnosticos_posibles)}")
            self.diagnostico_realizado = True

def ejecutar_diagnostico():
    from firebase import DiagnosticoDB
    db = DiagnosticoDB("../key.json")
    diagnosticos_base = db.leer_base()
    diagnosticos_definidos = db.leer_definidos()

    motor = DiagnosticoMedico(diagnosticos_base, diagnosticos_definidos)
    motor.set_sintomas()
    print(motor.sintomas)
    while not motor.diagnostico_realizado:
        sintomas_a_preguntar = motor.siguiente_sintoma_a_preguntar()

        if not sintomas_a_preguntar:
            break

        siguiente = sintomas_a_preguntar[0]
        motor.preguntar_sintoma(siguiente)

        motor.reset()
        motor.declare(Sintomas(**motor.sintomas_usuario))
        motor.run()


if __name__ == "__main__":
    ejecutar_diagnostico()