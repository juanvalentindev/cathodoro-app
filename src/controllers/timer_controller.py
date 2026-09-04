import platform
import os
import sys

# Detección del Sistema (Para sonidos)
sistema_actual = platform.system()
if sistema_actual == "Windows":
    import winsound
elif sistema_actual == "Linux":
    import subprocess

class CathodoroController:
    def __init__(self, modelo, vista):
        self.modelo = modelo
        self.vista = vista
        self.timer_id = None 
        
        ## Resolvemos la ruta del sonido
        if getattr(sys, 'frozen', False):
            ruta_raiz = os.path.dirname(sys.executable)
        else:
            # Subimos 3 niveles: controllers -> src -> raíz del proyecto
            ruta_raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            
        # Apuntamos a la nueva carpeta assets
        self.ruta_sonido = os.path.join(ruta_raiz, "assets", "audio", "pomodoro_ping.wav")

        # Conectar los botones de la vista con los métodos del controlador
        self.vista.boton_stop.configure(command=self.toggle_contador)
        self.vista.boton_reset.configure(command=self.reset_contador)
        self.vista.boton_siguiente.configure(command=self.saltar_instancia)
        self.vista.boton_configuracion.configure(command=self.abrir_configuracion)
        
        # Inicializar la vista con los datos del modelo
        self.actualizar_textos_vista()

    def toggle_contador(self):
        """Alterna entre iniciar y pausar el temporizador."""
        if not self.modelo.corriendo:
            self.modelo.corriendo = True
            self.vista.boton_stop.configure(text="| |")
            self.tick()
        else:
            self.parar_contador()

    def tick(self):
        """Bucle principal que se ejecuta cada segundo."""
        if not self.modelo.corriendo:
            return
            
        if self.modelo.decrementar_tiempo():
            self.actualizar_reloj()
            # Ejecutamos este mismo método cada 1000ms
            self.timer_id = self.vista.after(1000, self.tick)
        else:
            self.finalizar_fase()

    def finalizar_fase(self):
        """Maneja lo que ocurre cuando el tiempo llega a cero."""
        if self.modelo.sonido_activo:
            self.reproducir_sonido()
            
        self.modelo.avanzar_instancia()
        self.modelo.corriendo = False
        self.timer_id = None
        
        # Prepara la siguiente fase y actualiza la GUI
        mensaje_fase = self.modelo.preparar_siguiente_fase()
        self.vista.condicion_pomodoro.configure(text=mensaje_fase)
        self.actualizar_textos_vista()
        
        # Auto-iniciar la siguiente fase 
        self.toggle_contador() 

    def parar_contador(self):
        self.modelo.corriendo = False
        if self.timer_id is not None:
            self.vista.after_cancel(self.timer_id)
            self.timer_id = None
        self.vista.boton_stop.configure(text="▶")

    def reset_contador(self):
        self.parar_contador()
        mensaje_fase = self.modelo.preparar_siguiente_fase()
        self.vista.condicion_pomodoro.configure(text=mensaje_fase)
        self.actualizar_textos_vista()

    def saltar_instancia(self):
        self.parar_contador()
        self.modelo.reps += 1
        self.reset_contador()

    def actualizar_reloj(self):
        """Calcula minutos y segundos y los envía a la vista."""
        tiempo = self.modelo.tiempo_actual
        tiempo_seg = tiempo % 60
        tiempo_min = tiempo // 60
        self.vista.numeros.configure(text=f"{tiempo_min:02d}:{tiempo_seg:02d}")

    def actualizar_textos_vista(self):
        """Actualiza el reloj y el contador de pomodoros en la GUI."""
        self.actualizar_reloj()
        texto_info = f"Pomodoro {self.modelo.c_pomodoro} | Descanso {self.modelo.c_descanso} | Descanso largo {self.modelo.c_descanso_largo}"
        self.vista.informacion_pomodoro.configure(text=texto_info)

    def reproducir_sonido(self):
        if sistema_actual == "Windows":
            winsound.PlaySound(self.ruta_sonido, winsound.SND_ASYNC)
        elif sistema_actual == "Linux":
            subprocess.Popen(["aplay", "-q", self.ruta_sonido])
    
    def abrir_configuracion(self):
        """Prepara los datos actuales y le dice a la vista que dibuje la ventana de ajustes."""
        valores_actuales = {
            'pomodoro': self.modelo.pomodoro,
            'corto': self.modelo.descanso_corto,
            'largo': self.modelo.descanso_largo,
            'sonido': self.modelo.sonido_activo
        }
        # Le mandamos los valores actuales y qué función ejecutar al apretar "Guardar"
        self.vista.abrir_ventana_configuracion(valores_actuales, self.guardar_configuracion)
        
    def guardar_configuracion(self):
        """Lee los datos ingresados en la vista, los valida y actualiza el modelo."""
        try:
            nuevo_pomodoro = int(self.vista.entrada_pomodoro.get()) * 60
            nuevo_corto = int(self.vista.entrada_descanso_corto.get()) * 60
            nuevo_largo = int(self.vista.entrada_descanso_largo.get()) * 60
            nuevo_sonido = bool(self.vista.switch_sonido.get())
            
            if nuevo_pomodoro <= 0 or nuevo_corto <= 0 or nuevo_largo <= 0:
                print("Los tiempos deben ser mayores a 0")
                return 
            
            if nuevo_pomodoro > 99 or nuevo_corto > 99 or nuevo_largo > 99:
                return
            
            # Verificamos si cambió algún tiempo para saber si hay que resetear el reloj
            cambio_tiempo = (nuevo_pomodoro != self.modelo.pomodoro or 
                             nuevo_corto != self.modelo.descanso_corto or 
                             nuevo_largo != self.modelo.descanso_largo)

            # Actualizamos el modelo
            self.modelo.actualizar_configuracion(nuevo_pomodoro, nuevo_corto, nuevo_largo, nuevo_sonido)
            
            if cambio_tiempo:
                self.reset_contador()
                
            # Cerramos la ventanita
            self.vista.ventana_config.destroy()
            
        except ValueError:
            print("ERROR: Ingresá solo números enteros")