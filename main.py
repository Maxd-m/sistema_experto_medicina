import sys
import os
from tkinter import Tk, Frame, Label, Button, IntVar, Checkbutton, Canvas, Scrollbar, LEFT, RIGHT, BOTH, Y, VERTICAL, \
    ttk, messagebox
from PIL import ImageTk, Image, ImageSequence
from PIL.Image import Resampling
from fontTools.unicodedata import block

from firebase import DiagnosticoDB
from modules.voz_manager import VozManager
from modules.whatsapp_manager import WhatsAppManager
from modules.sistema_experto import ejecutar_diagnostico, DiagnosticoMedico, Sintomas

class MenuPrincipal:
    def __init__(self):
        self.voz = VozManager()
        self.whatsapp = WhatsAppManager()
        self.ejecutando = True
        self.db = DiagnosticoDB('key.json')
        self.diagnosticos_base = None
        self.diagnosticos_definidos = None
        self.posibles_diagnosticos = None

    def mostrar_bienvenida(self):
        """Es el mensaje de bienvenida"""
        print("\n" + "=" * 60)
        print("🏥 SISTEMA EXPERTO DE DIAGNÓSTICO MÉDICO")
        print("📞 Interfaz de Voz Simulada")
        print("=" * 60)

        mensaje_bienvenida = """
        Bienvenido al sistema de diagnóstico médico.
        Este sistema le ayudará con dos opciones principales.
        Por favor, escuche atentamente las opciones del menú.
        """

        self.voz.hablar(mensaje_bienvenida)

    def mostrar_menu(self):
        """Muestra las opciones del menú por voz"""
        mensaje_menu = """
        Menú principal. Tiene dos opciones:

        Opción uno: Agendar una cita médica.

        Opción dos: Iniciar diagnóstico médico con nuestro sistema experto.

        Por favor, diga "opción uno" para agendar cita, o "opción dos" para diagnóstico.
        """

        self.voz.hablar(mensaje_menu)

        # Mostrar menú visual también
        print("\n📋 MENÚ PRINCIPAL:")
        print("1️⃣  Agendar cita médica")
        print("2️⃣  Sistema experto de diagnóstico")
        print("\n🎤 Diga su opción...")

    def procesar_opcion_1(self):
        """Maneja la opción de agendar la cita"""
        print("\n" + "-" * 40)
        print("📅 AGENDAR CITA MÉDICA")
        print("-" * 40)

        self.voz.hablar("Ha seleccionado agendar cita médica.")

        # Mostrar información de la clínica
        self.whatsapp.mostrar_info_cita()

        # Solicitar número de teléfono
        numero = self.whatsapp.solicitar_numero_telefono(self.voz)

        if numero:
            self.voz.hablar("Perfecto. Procederé a agendar su cita y enviar la confirmación por WhatsApp.")

            # Intentar agendar la cita
            if self.whatsapp.agendar_cita(numero):
                self.voz.hablar("""
                Su cita ha sido agendada exitosamente. 
                En breve recibirá la confirmación en su WhatsApp con todos los detalles.
                Gracias por elegir nuestros servicios.
                """)
                self.db.guardar('pacientes', numero)
            else:
                self.voz.hablar("""
                Lo siento, hubo un problema al agendar su cita. 
                Por favor intente más tarde o contacte directamente a la clínica.
                """)
        else:
            self.voz.hablar("No se pudo procesar su solicitud de cita. Regresando al menú principal.")

    def procesar_opcion_2(self):
        """Maneja la opción del sistema experto"""
        print("\n" + "-" * 40)
        print("🔬 SISTEMA EXPERTO DE DIAGNÓSTICO")
        print("-" * 40)

        self.voz.hablar("""
        Ha seleccionado el sistema experto de diagnóstico médico.
        Este sistema le hará una serie de preguntas sobre sus síntomas
        para ayudar a identificar posibles condiciones médicas.
        """)

        self.voz.hablar("""
        Recuerde que este sistema es solo una herramienta de apoyo
        y no reemplaza la consulta con un médico profesional.
        """)

        self.voz.hablar("Comenzando con las preguntas del diagnóstico.")

        try:
            # Ejecutar el sistema experto con integración de voz
            self.ejecutar_sistema_experto_con_voz()

        except Exception as e:
            print(f"❌ Error en el sistema experto: {e}")
            self.voz.hablar("Lo siento, hubo un error en el sistema de diagnóstico. Regresando al menú principal.")

    def ejecutar_sistema_experto_con_voz(self):
        motor = DiagnosticoMedico(self.diagnosticos_base, self.diagnosticos_definidos)
        motor.set_sintomas()

        # Integrar VozManager con el sistema experto
        motor.voz_manager = self.voz

        print("🔬 Iniciando diagnóstico médico...")
        self.voz.hablar("Voy a hacerle algunas preguntas sobre sus síntomas. Responda con sí o no.")

        while not motor.diagnostico_realizado:
            sintomas_a_preguntar = motor.siguiente_sintoma_a_preguntar()

            if not sintomas_a_preguntar:
                break

            siguiente = sintomas_a_preguntar[0]

            # Usar el sistema de voz para preguntar
            pregunta = f"¿Tiene {siguiente.replace('_', ' ')}?"
            respuesta = self.voz.escuchar_si_no(pregunta)

            # Registrar respuesta
            motor.sintomas_usuario[siguiente] = respuesta

            # Procesar diagnóstico
            motor.reset()
            motor.declare(Sintomas(**motor.sintomas_usuario))
            motor.run()

        self.anunciar_resultado_diagnostico(motor)

        self.voz.hablar("Diagnóstico completado. Gracias por usar nuestro sistema.")

    def anunciar_resultado_diagnostico(self, motor):
        if len(motor.diagnosticos_posibles) == 0:
            mensaje = "No se encontró un diagnóstico claro..."

        elif len(motor.diagnosticos_posibles) == 1:
            diagnostico = list(motor.diagnosticos_posibles)[0]
            mensaje = f"El diagnóstico más probable es: {diagnostico}..."
            if info_adicional := self.db.leer(f'informacion/{diagnostico}'):
                mensaje += info_adicional
        else:
            #diagnosticos = ', '.join(motor.diagnosticos_posibles)
            mensaje = 'Se encontró más de un posible diagnóstico.'
            for diagnostico in list(motor.diagnosticos_posibles):
                mensaje += f"Un diagnóstico es: {diagnostico}..."
                if info_adicional := self.db.leer(f'informacion/{diagnostico}'):
                    mensaje += info_adicional
                mensaje += "..."
            #mensaje = f"Los posibles diagnósticos son: {diagnosticos}..."

        # Leerlo
        self.voz.hablar(mensaje)

    def manejar_opcion_invalida(self):
        self.voz.hablar("""
        Lo siento, no entendí su opción. 
        Por favor diga "uno" para agendar cita, o "dos" para diagnóstico médico.
        """)

    def confirmar_salida(self):
        """Simular el reinicio"""
        self.voz.hablar("¿Desea realizar otra consulta?")
        respuesta = self.voz.escuchar_si_no("¿Quiere volver al menú principal?")
        return respuesta

    def ejecutar(self):
        try:
            # Initialization
            self.db.guardar('pacientes', '442223034')
            self.diagnosticos_base = self.db.leer_base()
            self.diagnosticos_definidos = self.db.leer_definidos()

            self.mostrar_bienvenida()

            while self.ejecutando:
                self.mostrar_menu()

                # Escuchar opción del usuario
                opcion = self.voz.escuchar_opcion_menu()

                if opcion == 1:
                    self.procesar_opcion_1()
                elif opcion == 2:
                    self.procesar_opcion_2()
                elif opcion is None:
                    self.manejar_opcion_invalida()
                    continue
                else:
                    self.manejar_opcion_invalida()
                    continue

                # Preguntar si quiere continuar
                if not self.confirmar_salida():
                    self.ejecutando = False

            # Despedida
            self.voz.despedirse()

        except KeyboardInterrupt:
            print("\n\n⚠️  Sistema interrumpido por el usuario")
            self.voz.hablar("Sistema interrumpido. Hasta luego.")

        except Exception as e:
            print(f"\n❌ Error crítico: {e}")
            self.voz.hablar("Lo siento, ocurrió un error crítico. El sistema se cerrará.")

        finally:
            print("\n👋 Gracias por usar el Sistema de Diagnóstico Médico")
            print("🏥 Clínica San Rafael - Sistema desarrollado para fines educativos")


#interfaz
    def precargar_frames_gif(self):
        self.db.guardar('pacientes', '442223034')
        self.diagnosticos_base = self.db.leer_base()
        self.diagnosticos_definidos = self.db.leer_definidos()
        gif = Image.open("carga.gif")
        self.frames_gif_global = []

        for i in range(min(gif.n_frames, 60)):
            gif.seek(i)
            frame = gif.copy().convert('RGBA')
            frame = frame.resize(
            (self.ventana_doctor.winfo_screenwidth(), self.ventana_doctor.winfo_screenheight()-700),
            Resampling.LANCZOS
            )
            self.frames_gif_global.append(ImageTk.PhotoImage(frame))

    def transicion_carga(self, rapidez ,callback=None):
        self.callback = callback
        for widget in self.ventana_doctor.winfo_children():
            widget.destroy()

        self.frame_carga = Frame(self.ventana_doctor, bg='white')
        self.frame_carga.pack(fill='both', expand=True)
        imagen = Image.open("fondo_carga.png")
        imagen = imagen.resize(
            (self.ventana_doctor.winfo_screenwidth(), self.ventana_doctor.winfo_screenheight()),
            Resampling.LANCZOS
        )
        self.bg_image = ImageTk.PhotoImage(imagen)
        fondo_label = Label(self.frame_carga, image=self.bg_image)
        fondo_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.frames_gif = self.frames_gif_global  # reutiliza los precargados
        self.total_frames = len(self.frames_gif)
        self.gif_index = 0
        self.label_gif = Label(self.frame_carga, bg='black')
        self.label_gif.pack(pady=200)

        self.label_porcentaje = Label(self.frame_carga, text="0%", font=("Arial", 30), bg='#07141a', fg='white')
        self.label_porcentaje.pack(pady=20)

        self.porcentaje = 0
        self.actualizar_gif()
        self.actualizar_porcentaje(rapidez)

    def actualizar_gif(self):
        if not hasattr(self, 'label_gif') or not self.label_gif.winfo_exists():
            return  # El label ya no existe, se cerró o destruyó
        frame = self.frames_gif[self.gif_index]
        self.label_gif.configure(image=frame)
        self.gif_index = (self.gif_index + 1) % self.total_frames
        self.ventana_doctor.after(70, self.actualizar_gif)

    def actualizar_porcentaje(self, rapidez):
        if self.porcentaje <= 100:
            self.label_porcentaje.config(text=f"{self.porcentaje}%")
            self.porcentaje += 2
            self.ventana_doctor.after(rapidez, lambda: self.actualizar_porcentaje(rapidez))
        else:
            if self.callback:  # CORREGIDO el nombre
                self.callback()

    def interfaz_doctor(self):
        self.ventana_doctor = Tk()
        self.ventana_doctor.state('zoomed')
        self.ventana_doctor.title('Diagnóstico médico')
        self.precargar_frames_gif()
        label_titulo = Label(self.ventana_doctor, text='Sistema Experto de Medicina',
                             fg='black', bg='#abdff4', font=('Arial', 30))
        label_titulo.pack(fill='x')

        frame_inicio = Frame(self.ventana_doctor, width=800, height=600)
        frame_inicio.pack(fill='both', expand=True)

        imagen = Image.open("fondo.png")
        imagen = imagen.resize(
            (self.ventana_doctor.winfo_screenwidth(), self.ventana_doctor.winfo_screenheight()),
            Resampling.LANCZOS
        )
        self.bg_image = ImageTk.PhotoImage(imagen)

        fondo_label = Label(frame_inicio, image=self.bg_image)
        fondo_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        boton_comenzar = Button(frame_inicio, text='Comenzar diagnóstico',
                                fg='white', bg='black', font=('Arial', 18),
                                command=self.transicion_carga_a_diagnostico)
        boton_comenzar.place(relx=0.5, rely=0.5, anchor='center')

        self.ventana_doctor.mainloop()

    def transicion_carga_a_diagnostico(self):
        self.transicion_carga(25,callback=self.cambiar_frame_sintomas)

    def cambiar_frame_sintomas(self):
        from tkinter import messagebox  # Asegúrate de tenerlo si lo necesitas

        self.diagnostico = DiagnosticoMedico(self.diagnosticos_base, self.diagnosticos_definidos)

        for widget in self.ventana_doctor.winfo_children():
            widget.destroy()

        # TÍTULO
        label_tit = Label(
            self.ventana_doctor,
            text="Selecciona los síntomas que padece el paciente",
            fg="white",
            bg="#114051",
            font=('Arial', 40),
            width=self.ventana_doctor.winfo_screenwidth()
        )
        label_tit.pack()

        # CONTENEDOR PRINCIPAL
        contenedor = Frame(self.ventana_doctor, bg='black')
        contenedor.pack(fill='both', expand=True)

        # ========== FRAME SÍNTOMAS ========== #
        frame_sintomas = Frame(contenedor, bg='black')
        frame_sintomas.pack(side='left', fill='both', expand=True)

        canvas = Canvas(frame_sintomas, bg="black", highlightthickness=0)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame_sintomas, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame desplazable
        frame_sintomas_base = Frame(canvas, bg='black')

        # Fondo dentro del frame desplazable
        fondo_label = Label(frame_sintomas_base)
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
        fondo_label.lower()  # Moverlo al fondo

        ventana_interna = canvas.create_window((0, 0), window=frame_sintomas_base, anchor='nw')

        def ajustar_fondo():
            frame_sintomas_base.update_idletasks()
            ancho = frame_sintomas_base.winfo_width()
            alto = frame_sintomas_base.winfo_height()

            if ancho > 1 and alto > 1:
                imagen = Image.open("fondo2.png").resize((ancho, alto), Resampling.LANCZOS)
                self.bg_image3 = ImageTk.PhotoImage(imagen)
                fondo_label.configure(image=self.bg_image3)
            else:
                fondo_label.after(30, ajustar_fondo)

        fondo_label.after(30, ajustar_fondo)

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def on_canvas_configure(event):
            canvas.itemconfig(ventana_interna, width=event.width)

        frame_sintomas_base.bind("<Configure>", on_frame_configure)
        canvas.bind("<Configure>", on_canvas_configure)

        # Crear checkboxes
        self.vars_sintomas = []
        for sintoma in self.diagnostico.get_sintomas_base():
            var = IntVar()
            chk = Checkbutton(
                frame_sintomas_base,
                text=sintoma,
                font=('Arial', 16),
                variable=var,
                anchor='w',
                justify='left',
                wraplength=800,
                bg='#08374b',
                fg='white',
                selectcolor='black'
            )
            chk.pack(fill='x', padx=20, pady=5)
            self.vars_sintomas.append((var, sintoma))

        # Botones
        frame_botones = Frame(frame_sintomas_base, bg='#063539')
        frame_botones.pack(pady=20)

        boton_resetear = Button(
            frame_botones, text='Resetear',
            font=('Arial', 14),
            bg='#c28d18',
            fg='white',
            command=self.resetea_sintomas
        )
        boton_resetear.grid(row=0, column=0, padx=10)

        boton_verificar = Button(
            frame_botones, text='Diagnosticar',
            font=('Arial', 14),
            bg='#1c5460',
            fg='white',
            command=self.verificar_seleccion_sintomas
        )
        boton_verificar.grid(row=0, column=1, padx=10)

        # ========== FRAME ROBOT ========== #
        frame_robot = Frame(contenedor, width=self.ventana_doctor.winfo_screenwidth() / 2.5)
        frame_robot.pack(side='left', fill='both')

        imagen = Image.open("robot1.png").resize(
            (int(self.ventana_doctor.winfo_screenwidth() / 2.5), int(self.ventana_doctor.winfo_screenheight())),
            Resampling.LANCZOS
        )
        self.bg_robot1 = ImageTk.PhotoImage(imagen)
        fondo_label_robot = Label(frame_robot, image=self.bg_robot1)
        fondo_label_robot.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Scroll con mouse
        if self.ventana_doctor.tk.call('tk', 'windowingsystem') == 'x11':
            canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
            canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))
        else:
            canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

    def verificar_seleccion_sintomas(self):
        seleccionados = [var.get() for var, _ in self.vars_sintomas if var.get() == 1]

        if not seleccionados:
            messagebox.showwarning("Advertencia", "Debe seleccionar al menos un síntoma.")
        else:
            self.transicion_carga_a_ver_sintomas_definidos()

    def resetea_sintomas(self):
        for var, _ in self.vars_sintomas:
            var.set(0)

    def cambiar_frame_sintomas_definidos(self):
        for widget in self.ventana_doctor.winfo_children():
            widget.destroy()

        # TÍTULO
        label_tit = Label(
            self.ventana_doctor,
            text="Selecciona los síntomas que también podría tener el paciente",
            fg="white",
            bg="#114051",
            font=('Arial', 40),
            width=self.ventana_doctor.winfo_screenwidth()
        )
        label_tit.pack()

        # CONTENEDOR PRINCIPAL
        contenedor = Frame(self.ventana_doctor, bg='black')
        contenedor.pack(fill='both', expand=True)

        # ========== FRAME IZQUIERDO (SÍNTOMAS) ========== #
        frame_izquierdo = Frame(contenedor, bg='black')
        frame_izquierdo.pack(side='left', fill='both', expand=True)

        canvas = Canvas(frame_izquierdo, bg="black", highlightthickness=0)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        # Scrollbar personalizada
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Vertical.TScrollbar",
                        gripcount=0,
                        background="black",
                        darkcolor="#00313d",
                        lightcolor="#00313d",
                        troughcolor="#000000",
                        bordercolor="#000000",
                        arrowcolor="black")

        scrollbar = ttk.Scrollbar(frame_izquierdo, orient=VERTICAL, command=canvas.yview, style="Vertical.TScrollbar")
        scrollbar.pack(side=RIGHT, fill=Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame desplazable
        frame_sintomas_def = Frame(canvas, bg='black')
        ventana_interna = canvas.create_window((0, 0), window=frame_sintomas_def, anchor='nw')

        # Fondo dentro del frame desplazable
        fondo_label = Label(frame_sintomas_def, bg="black")
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
        fondo_label.lower()

        def ajustar_fondo():
            frame_sintomas_def.update_idletasks()
            ancho = frame_izquierdo.winfo_width()
            alto_canvas = frame_izquierdo.winfo_height()
            alto_real = frame_sintomas_def.winfo_height()

            if alto_real < alto_canvas:
                frame_sintomas_def.config(height=alto_canvas)

            if ancho > 1 and alto_real > 1:
                imagen = Image.open("fondo2.png").resize((ancho, max(alto_real, alto_canvas)), Resampling.LANCZOS)
                self.bg_image3 = ImageTk.PhotoImage(imagen)
                fondo_label.configure(image=self.bg_image3)
            else:
                fondo_label.after(30, ajustar_fondo)

        fondo_label.after(30, ajustar_fondo)

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def on_canvas_configure(event):
            canvas.itemconfig(ventana_interna, width=event.width)

        frame_sintomas_def.bind("<Configure>", on_frame_configure)
        canvas.bind("<Configure>", on_canvas_configure)

        # ====== SÍNTOMAS DEFINIDOS (Checkbuttons) ======
        self.vars_sintomas_def = []
        for sintoma in self.diagnostico.get_sintomas_variante_faltantes():
            var = IntVar()
            chk = Checkbutton(
                frame_sintomas_def,
                text=sintoma,
                font=('Arial', 16),
                variable=var,
                anchor='w',
                justify='left',
                wraplength=800,
                bg='#08374b',
                fg='white',
                selectcolor='black'
            )
            chk.pack(fill='x', padx=20, pady=5)
            self.vars_sintomas_def.append((var, sintoma))

        # ====== BOTONES ======
        frame_botones = Frame(frame_sintomas_def, bg='#063539')
        frame_botones.pack(pady=20)

        boton_resetear = Button(
            frame_botones, text='Resetear',
            font=('Arial', 14),
            bg='#c28d18',
            fg='white',
            command=self.resetea_sintomas_def
        )
        boton_resetear.grid(row=0, column=0, padx=10)

        boton_verificar = Button(
            frame_botones, text='Diagnosticar',
            font=('Arial', 14),
            bg='#1c5460',
            fg='white',
            command=self.transicion_a_resultado
        )
        boton_verificar.grid(row=0, column=1, padx=10)

        boton_saltar = Button(
            frame_botones, text='Continuar sin más sintomas',
            font=('Arial', 14),
            bg='#259c8a',
            fg='white',
            command=self.transicion_a_resultado
        )
        boton_saltar.grid(row=0, column=2, padx=10)

        # ========== FRAME DERECHO (Robot) ========== #
        frame_derecho = Frame(contenedor, width=self.ventana_doctor.winfo_screenwidth() / 2.5)
        frame_derecho.pack(side='left', fill='both')

        imagen_robot = Image.open("robot1.png").resize(
            (int(self.ventana_doctor.winfo_screenwidth() / 2.5), int(self.ventana_doctor.winfo_screenheight())),
            Resampling.LANCZOS
        )
        self.bg_derecha = ImageTk.PhotoImage(imagen_robot)
        fondo_der = Label(frame_derecho, image=self.bg_derecha)
        fondo_der.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Scroll con mouse
        if self.ventana_doctor.tk.call('tk', 'windowingsystem') == 'x11':
            canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
            canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))
        else:
            canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

    def resetea_sintomas_def(self):
        for var, _ in self.vars_sintomas_def:
            var.set(0)

    def mostrar_diagnostico(self):
        for widget in self.ventana_doctor.winfo_children():
            widget.destroy()

        # === SELECCIÓN DE FONDO SEGÚN RESULTADO ===
        if len(self.diagnostico.diagnosticos_posibles) == 0:
            fondo_path = "fondo_nada.png"
            robot_path = "diagnostico_mal.png"
            color_texto = 'red'
            resultado_texto = "No se encontró un diagnóstico claro."
        elif len(self.diagnostico.diagnosticos_posibles) == 1:
            fondo_path = "fondo_definido.png"
            robot_path = "diagnostico_hecho.png"
            color_texto = 'green'
            diag = list(self.diagnostico.diagnosticos_posibles)[0]
            resultado_texto = f"Diagnóstico probable: {diag.upper()}"
        else:
            fondo_path = "fondo_probables.png"
            robot_path = "diagnostico_confuso.png"
            color_texto = 'orange'
            resultado_texto = "No se encontró un diagnóstico específico."

        imagen_fondo = Image.open(fondo_path).resize(
            (int(self.ventana_doctor.winfo_screenwidth() * 0.6), self.ventana_doctor.winfo_screenheight()),
            Resampling.LANCZOS
        )
        self.bg_izq_diag = ImageTk.PhotoImage(imagen_fondo)

        imagen_robot = Image.open(robot_path).resize(
            (int(self.ventana_doctor.winfo_screenwidth() * 0.4), self.ventana_doctor.winfo_screenheight()),
            Resampling.LANCZOS
        )
        self.bg_der_diag = ImageTk.PhotoImage(imagen_robot)

        # === CONTENEDOR PRINCIPAL HORIZONTAL ===
        contenedor = Frame(self.ventana_doctor)
        contenedor.pack(fill='both', expand=True)

        # === FRAME IZQUIERDO (Texto diagnóstico) ===
        frame_izq = Frame(contenedor, bg='black')
        frame_izq.pack(side='left', fill='both', expand=True)

        frame_resultado = Frame(frame_izq, bg='white')
        fondo_izq = Label(frame_resultado, image=self.bg_izq_diag)
        fondo_izq.place(relx=0, rely=0, relwidth=1, relheight=1)
        frame_resultado.pack(fill='both', expand=True, padx=40, pady=40)

        if len(self.diagnostico.diagnosticos_posibles) <= 1:
            Label(frame_resultado, text=resultado_texto, font=("Arial", 18, 'bold'), bg='white', fg=color_texto).pack(
                pady=10)
        else:
            Label(frame_resultado, text=resultado_texto, font=("Arial", 18), bg='white', fg=color_texto).pack(pady=10)
            Label(frame_resultado, text="Posibles diagnósticos:", font=("Arial", 16), bg='white').pack(pady=(10, 5))
            for diag in self.diagnostico.diagnosticos_posibles:
                Label(frame_resultado, text=f"- {diag}", font=("Arial", 14), bg='white').pack(anchor='w', padx=20)

        self.diagnostico.sintomas_usuario.clear()

        # === BOTONES ===
        Button(frame_resultado, text="Volver a diagnosticar", font=("Arial", 14),
               command=self.transicion_carga_a_diagnostico, fg='white',bg="#03535d").pack(pady=20)
        Button(frame_resultado, text="Salir", bg='#951717', fg='white',font=("Arial", 14), command=self.ventana_doctor.destroy).pack()

        # === FRAME DERECHO (Imagen robot) ===
        frame_der = Frame(contenedor, width=int(self.ventana_doctor.winfo_screenwidth() * 0.4))
        frame_der.pack(side='left', fill='both')

        fondo_der = Label(frame_der, image=self.bg_der_diag)
        fondo_der.place(relx=0, rely=0, relwidth=1, relheight=1)

    def transicion_carga_a_ver_sintomas_definidos(self):
        seleccionados = [s for var, s in self.vars_sintomas if var.get() == 1]
        self.diagnostico.sintomas_usuario = {s: True for s in seleccionados}
        self.diagnostico.reset()
        self.diagnostico.declare(Sintomas(**self.diagnostico.sintomas_usuario))
        self.diagnostico.run()
        self.diagnostico.filtrar_diagnosticos_ponens()
        # Si ya no hay síntomas definidos por mostrar, ir directo a mostrar_diagnostico
        if not self.diagnostico.get_sintomas_variante_faltantes():
            self.transicion_carga(40, callback=self.mostrar_diagnostico)
        else:
            self.transicion_carga(60, callback=self.cambiar_frame_sintomas_definidos)
    def transicion_a_resultado(self):
            # Obtener síntomas definidos adicionales seleccionados
            seleccionados_nuevos = [s for var, s in self.vars_sintomas_def if var.get() == 1]

            # Agregar o actualizar al diccionario existente
            self.diagnostico.sintomas_usuario.update({s: True for s in seleccionados_nuevos})
            self.diagnostico.reset()
            self.diagnostico.declare(Sintomas(**self.diagnostico.sintomas_usuario))
            self.diagnostico.run()
            self.diagnostico.filtrar_diagnosticos_ponens()
            print(self.diagnostico.diagnosticos_posibles)
            self.transicion_carga(40, callback=self.mostrar_diagnostico)

def main():
    menu = MenuPrincipal()
    menu.interfaz_doctor()
if __name__ == "__main__":
    main()