import customtkinter as ctk
from PIL import Image
import os
import sys

class CathodoroView(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # ---------------------------------------------------------
        # Configuración de la Ventana Principal
        # ---------------------------------------------------------
        self.title("Cathodoro")
        ctk.set_appearance_mode("Dark")
        self.configure(fg_color=("white", "black"))

        ANCHO = 500
        LARGO = 600

        # Obtención de rutas para las imagenes
        if getattr(sys, 'frozen', False):
            ruta_carpeta = os.path.dirname(sys.executable)
        else:
            ruta_carpeta = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

       
        self.ruta_imagen_blanca = os.path.join(ruta_carpeta, "assets", "images", "imagen_blanca.png")
        self.ruta_imagen_negra = os.path.join(ruta_carpeta, "assets", "images", "imagen_negra.png")
        self.ruta_icono = os.path.join(ruta_carpeta, "assets", "icon.ico")

        try:
            self.iconbitmap(self.ruta_icono)
        except Exception:
            pass

        # Centrar la ventana al crearse
        ancho_pantalla = self.winfo_screenwidth()
        largo_pantalla = self.winfo_screenheight()
        x_sobrante = (ancho_pantalla - ANCHO) // 2
        y_sobrante = (largo_pantalla - LARGO) // 2
        self.geometry(f"{ANCHO}x{LARGO}+{x_sobrante}+{y_sobrante}")

        # ---------------------------------------------------------
        # Contenedores
        # ---------------------------------------------------------
        self.contenedor_maestro = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor_maestro.pack(expand=True, fill="both")
        self.contenedor_maestro.grid_rowconfigure(0, weight=1)
        self.contenedor_maestro.grid_columnconfigure(0, weight=1)

        self.contenedor_principal = ctk.CTkFrame(self.contenedor_maestro, fg_color="transparent")
        self.contenedor_principal.grid(row=0, column=0)

        # ---------------------------------------------------------
        # Elementos Visuales
        # ---------------------------------------------------------
        # Información de los pomodoros
        self.informacion_pomodoro = ctk.CTkLabel(self.contenedor_principal, text="Pomodoro 0 | Descanso 0 | Descanso largo 0", font=("Consolas", 14), text_color=("black", "white"))
        self.informacion_pomodoro.pack(pady=(0,0))

        # Rectángulo principal
        self.rectangulo = ctk.CTkFrame(self.contenedor_principal, fg_color=("white", "black"), border_color=("black", "white"), border_width=2, corner_radius=30)
        self.rectangulo.pack(pady=10, ipadx=25, ipady=0)

        # Imagen
        try:
            imagen_bites_blanca = Image.open(self.ruta_imagen_blanca)
            imagen_bites_negra = Image.open(self.ruta_imagen_negra)
            imagen_pomodoro_objeto = ctk.CTkImage(light_image=imagen_bites_negra, dark_image=imagen_bites_blanca, size=(200, 250))
            self.imagen_pomodoro_label = ctk.CTkLabel(self.rectangulo, text="", image=imagen_pomodoro_objeto)
            self.imagen_pomodoro_label.pack(pady=(20,10))
        except FileNotFoundError:
            print("ERROR NO PUDO ENCONTRARSE LA IMAGEN")

        # Cronómetro
        self.numeros = ctk.CTkLabel(self.rectangulo, text="25:00", font=("Consola", 90), text_color=("black", "white"))
        self.numeros.pack(pady=(5,5))

        # Condición pomodoro
        self.condicion_pomodoro = ctk.CTkLabel(self.rectangulo, text="Ora et labora...", font=("Consolas", 11), text_color=("black", "white"))
        self.condicion_pomodoro.pack()

        # Contenedor para los controles
        self.contenedor_controles = ctk.CTkFrame(self.rectangulo, fg_color="transparent")
        self.contenedor_controles.pack(pady=(0,20))

        # ---------------------------------------------------------
        # Botones (Sin lógica conectada todavía)
        # ---------------------------------------------------------
        self.boton_stop = ctk.CTkButton(self.contenedor_controles, text="▶", font=("Consola", 25), text_color=("black", "white"), fg_color="transparent", width=5, height=5, hover_color=("white", "black"))
        self.boton_stop.grid(row=0, column=0, padx=10, pady=10)

        self.boton_reset = ctk.CTkButton(self.contenedor_controles, text="↻", font=("Consola", 25), text_color=("black", "white"), fg_color="transparent", width=5, height=5, hover_color=("white", "black"))
        self.boton_reset.grid(row=0, column=1, padx=10, pady=10)

        self.boton_siguiente = ctk.CTkButton(self.contenedor_controles, text=">>", font=("Consola", 19), text_color=("black", "white"), fg_color="transparent", width=5, height=5, hover_color=("white", "black"))
        self.boton_siguiente.grid(row=0, column=2, padx=10, pady=10)

        # Botón Oración
        self.oracion_visible = False
        self.oracion_boton = ctk.CTkButton(self.contenedor_principal, text="Oración", text_color=("black", "white"), font=("Consola", 13, "normal"), fg_color=("white", "black"), border_color=("black", "white"), border_width=2, corner_radius=7, hover_color=("white", "black"), command=self.cambio_oracion)
        self.oracion_boton.pack()

        # Botones Inferiores
        self.boton_configuracion = ctk.CTkButton(self, text="⚙", font=("Consolas", 24), width=40, height=40, fg_color="transparent", text_color=("black", "white"), hover_color=("white", "black"))
        self.boton_configuracion.place(relx=0.05, rely=0.95, anchor="sw")

        self.boton_tema = ctk.CTkButton(self, text="☀️", font=("Consolas", 24), width=40, height=40, fg_color="transparent", text_color=("black", "white"), hover_color=("#cccccc", "#333333"), command=self.cambiar_tema)
        self.boton_tema.place(relx=0.95, rely=0.95, anchor="se")

        # ---------------------------------------------------------
        # Widget Oración (Oculto por defecto)
        # ---------------------------------------------------------
        self.widget_oracion = ctk.CTkFrame(self, fg_color=("white", "black"), border_color=("black", "white"), border_width=2, corner_radius=15)
        
        texto_oracion = "Oh Espíritu Santo,\nAmor del Padre, y del Hijo,\nInspírame siempre lo que debo pensar,\nlo que debo decir,\ncómo debo decirlo,\nlo que debo callar,\ncómo debo actuar,\nlo que debo hacer,\npara gloria de Dios,\nbien de las almas\ny mi propia Santificación.\n\nEspíritu Santo,\nDame agudeza\npara entender,\ncapacidad para retener,\nmétodo y facultad para aprender,\nsutileza para interpretar,\ngracia y eficacia para hablar.\nDame acierto al empezar\ndirección al progresar\ny perfección al acabar.\nAmén."
        
        self.label_oracion = ctk.CTkLabel(self.widget_oracion, text=texto_oracion, font=("Consolas", 14, "italic"), text_color=("black", "white"), justify="center")
        self.label_oracion.pack(padx=30, pady=30)

    # ---------------------------------------------------------
    # Métodos Puramente Visuales
    # ---------------------------------------------------------
    def cambiar_tema(self):
        modo_actual = ctk.get_appearance_mode()
        if modo_actual == "Dark":
            ctk.set_appearance_mode("Light")
            self.boton_tema.configure(text="🌙")
        else:
            ctk.set_appearance_mode("Dark")
            self.boton_tema.configure(text="☀️")

    def cambio_oracion(self):
        if not self.oracion_visible:
            self.widget_oracion.place(relx=0.5, rely=0.5, anchor="center")
            self.oracion_visible = True
        else:
            self.widget_oracion.place_forget()
            self.oracion_visible = False
            
    def abrir_ventana_configuracion(self, vals_actuales, comando_guardar):
        # Controla que no se abran más de una ventana a la vez
        if hasattr(self, "ventana_config") and self.ventana_config.winfo_exists():
            self.ventana_config.focus()
            return
            
        # Configuración de la Ventana de Configuración 
        self.ventana_config = ctk.CTkToplevel(self)
        self.ventana_config.title("Ajustes")
        self.ventana_config.geometry("260x400")
        self.ventana_config.configure(fg_color=("white", "black"))
        self.ventana_config.attributes("-topmost", True)

        def aplicar_icono():
            try:
                self.ventana_config.iconbitmap(self.ruta_icono)
            except Exception:
                # Falla silenciosamente en Linux, la ventana simplemente usará el ícono por defecto
                pass

        self.ventana_config.after(200, aplicar_icono)

        # Creamos una ventana scrolleable 
        marco_scroll = ctk.CTkScrollableFrame(self.ventana_config, fg_color="transparent")
        marco_scroll.pack(pady=(10,5), padx=10, fill="both", expand=True)
        
        # Cartel Pomodoro
        ctk.CTkLabel(marco_scroll, text="Pomodoro (minutos):", text_color=("black", "white"), font=("Consolas", 14)).pack(pady=(20, 5))
        self.entrada_pomodoro = ctk.CTkEntry(marco_scroll, width=100, justify="center")
        self.entrada_pomodoro.insert(0, str(vals_actuales['pomodoro'] // 60)) 
        self.entrada_pomodoro.pack()

        # Cartel Descanso Corto
        ctk.CTkLabel(marco_scroll, text="Descanso Corto (minutos):", text_color=("black", "white"), font=("Consolas", 14)).pack(pady=(20, 5))
        self.entrada_descanso_corto = ctk.CTkEntry(marco_scroll, width=100, justify="center")
        self.entrada_descanso_corto.insert(0, str(vals_actuales['corto'] // 60)) 
        self.entrada_descanso_corto.pack()

        # Cartel Descanso Largo 
        ctk.CTkLabel(marco_scroll, text="Descanso Largo (minutos):", text_color=("black", "white"), font=("Consolas", 14)).pack(pady=(20, 5))
        self.entrada_descanso_largo = ctk.CTkEntry(marco_scroll, width=100, justify="center")
        self.entrada_descanso_largo.insert(0, str(vals_actuales['largo'] // 60)) 
        self.entrada_descanso_largo.pack()

        # Interruptor Silencio
        ctk.CTkLabel(marco_scroll, text="", text_color=("black", "white"), font=("Consolas", 14)).pack(pady=(10, 0))
        self.switch_sonido = ctk.CTkSwitch(marco_scroll, text="Campana Activada")
        if vals_actuales['sonido']:
            self.switch_sonido.select()
        else:
            self.switch_sonido.deselect()
        self.switch_sonido.pack()

        # Guardar (Lo conectamos al controlador)
        boton_guardar = ctk.CTkButton(self.ventana_config, text="Guardar", fg_color=("black", "white"), 
                                      text_color=("white", "black"), hover_color=("white", "black"), 
                                      font=("Consolas", 14, "bold"), command=comando_guardar)
        boton_guardar.pack(side="bottom", pady=(5, 15))