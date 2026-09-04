import json
import os
import sys

class CathodoroModel:
    def __init__(self):
        # Definimos los tiempos por defecto (en segundos)
        self.pomodoro = 25 * 60
        self.descanso_corto = 5 * 60
        self.descanso_largo = 10 * 60
        self.sonido_activo = True
        
        # Obtenemos la ruta raíz para guardar el archivo config.json junto a las carpetas src/ y assets/
        if getattr(sys, 'frozen', False):
            self.ruta_raiz = os.path.dirname(sys.executable)
        else:
            # Sube 3 niveles: models -> src -> raíz
            self.ruta_raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            
        self.ruta_config = os.path.join(self.ruta_raiz, "config.json")
        
        # Intentamos cargar la configuración antes de arrancar
        self.cargar_configuracion_local()

        # Variables de funcionamiento actuales
        self.tiempo_actual = self.pomodoro
        self.reps = 1
        self.corriendo = False
        
        # Variables para conteo estadístico
        self.c_pomodoro = 0
        self.c_descanso = 0
        self.c_descanso_largo = 0

    def cargar_configuracion_local(self):
        """Lee el archivo config.json si existe y sobrescribe los valores por defecto."""
        if os.path.exists(self.ruta_config):
            try:
                with open(self.ruta_config, "r", encoding="utf-8") as archivo:
                    datos = json.load(archivo)
                    self.pomodoro = datos.get("pomodoro", self.pomodoro)
                    self.descanso_corto = datos.get("descanso_corto", self.descanso_corto)
                    self.descanso_largo = datos.get("descanso_largo", self.descanso_largo)
                    self.sonido_activo = datos.get("sonido_activo", self.sonido_activo)
            except Exception as e:
                print(f"Error al leer la configuración, usando valores por defecto: {e}")

    def guardar_configuracion_local(self):
        """Toma los valores actuales y los guarda en config.json."""
        datos = {
            "pomodoro": self.pomodoro,
            "descanso_corto": self.descanso_corto,
            "descanso_largo": self.descanso_largo,
            "sonido_activo": self.sonido_activo
        }
        try:
            with open(self.ruta_config, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=4)
        except Exception as e:
            print(f"Error al guardar la configuración: {e}")

    def decrementar_tiempo(self):
        if self.corriendo and self.tiempo_actual > 0:
            self.tiempo_actual -= 1
            return True
        return False

    def avanzar_instancia(self):
        if (self.reps % 8) == 0:
            self.c_descanso_largo += 1 
        elif (self.reps % 2) == 0:
            self.c_descanso += 1      
        else:
            self.c_pomodoro += 1
            
        self.reps += 1

    def preparar_siguiente_fase(self):
        if (self.reps % 8) == 0:
            self.tiempo_actual = self.descanso_largo
            return "Descanso Largo..."
        elif (self.reps % 2) == 0:
            self.tiempo_actual = self.descanso_corto
            return "Descanso..."
        else:
            self.tiempo_actual = self.pomodoro
            return "Ora et labora..."

    def actualizar_configuracion(self, nuevo_pomodoro, nuevo_corto, nuevo_largo, nuevo_sonido):
        """Actualiza las preferencias desde la ventana de ajustes y las guarda en disco."""
        self.pomodoro = nuevo_pomodoro
        self.descanso_corto = nuevo_corto
        self.descanso_largo = nuevo_largo
        self.sonido_activo = nuevo_sonido
        
        # Se llama automáticamente al guardar en la interfaz
        self.guardar_configuracion_local()