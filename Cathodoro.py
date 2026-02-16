import customtkinter as ctk
import tkinter as tk
from PIL import Image
import os
import sys
import time 
import platform 

 ##----------------------------------------Variables Del Temporizador---------------------------------------

#Variables de Tiempo (En segundos)
pomodoro = 25*60
descanso_corto= 5*60
descanso_largo = 10*60
tick = 1

#Variables de funcionamiento
timer = None
tiempo = pomodoro
reps = 1
corriendo= False

#Variables para conteo de pomodoros/descansos 
c_pomodoro = 0
c_descanso = 0
c_descanso_largo= 0

#Variables para Configuraciones de Widgets
ventana_config = None
oracion_visible = False

#Detección del Sistema (Para sonidos)
sistema_actual = platform.system()

#----------------------------------------Funciónes Del Temporizador---------------------------------------

#Funcion de detección de sistema (Para sonidos)
if sistema_actual == "Windows":
    import winsound
elif sistema_actual == "Linux":
    import subprocess

def iniciar_contador():
    global tiempo,corriendo,c_pomodoro,c_descanso,c_descanso_largo,timer
    
    if not corriendo:
        corriendo=True
        boton_stop.configure(text="| |",command=parar_contador)

        if tiempo <= 0:
            if (reps % 8) == 0:
                tiempo = descanso_largo
                condicion_pomodoro.configure(text="Descanso Largo...")
            elif (reps % 2) == 0:
                tiempo = descanso_corto
                condicion_pomodoro.configure(text="Descanso...")
            else:
                tiempo = pomodoro
                condicion_pomodoro.configure(text="Ora et labora...")
            
        informacion_pomodoro.configure(text=f"Pomodoro {c_pomodoro} | Descanso {c_descanso} | Descanso largo {c_descanso_largo}")
        timer = app.after(tick, rebajar_contador) #SIGO SIN ENTENDER PERO LO ARREGLOO


def rebajar_contador():
    global tiempo,reps,corriendo,timer,c_pomodoro, c_descanso, c_descanso_largo
    if not corriendo:
        return
    
    if tiempo > 0:
        tiempo -= 1
    
    #Actualización del Cronometro de la GUI
    tiempo_seg = tiempo % 60 #numeros del 1 al 60
    tiempo_min = tiempo // 60 
    str_seg=f"{tiempo_seg:02d}"
    str_min=f"{tiempo_min:02d}"
    numeros.configure(text=f"{str_min}:{str_seg}")

    if tiempo > 0:

        #tiempo -=1 #Nota error: Al apretar repetidamente el boton de bajar el volumen, bajabamos el volumen manualmente
                  #Mi solución anterior, lo que hacia era Restar y despues Esperaba, por tanto, para solucionarlo
                  #primero corremos el inicio de contador despues de un segundo , y luego en la función de bajar el contador, restamos un segundo, ya que esperamos para entrar otro
        timer = app.after(tick,rebajar_contador) #cada 1000ms ejecuta rebajar contador
    else:
        print(f"Buscando audio en: {ruta_sonido}")
        reproducir_sonido(ruta_sonido)
        #Contadores visuales
        if (reps % 8) == 0:
            c_descanso_largo += 1 
        elif (reps % 2) == 0:
            c_descanso += 1      
        else:
            c_pomodoro += 1
        
        informacion_pomodoro.configure(text=f"Pomodoro {c_pomodoro} | Descanso {c_descanso} | Descanso largo {c_descanso_largo}")
        reps += 1
        corriendo =False
        timer = None
        boton_stop.configure(text="▶", command=iniciar_contador)

        if (reps % 2) == 0:
            condicion_pomodoro.configure(text="¡Tiempo! Toca descanso")
        else:
            condicion_pomodoro.configure(text="¡A trabajar!")
        


def parar_contador():
    global timer,corriendo
   
    if timer is not None: #Paramos el contador si es que existe un timer activo 
        app.after_cancel(timer)
        timer = None 
    corriendo = False

    boton_stop.configure(text="▶",command=iniciar_contador)
    
def reset_contador():
    global timer,tiempo

    parar_contador()
    corriendo = False
    boton_stop.configure(text="▶", command=iniciar_contador)

    if (reps % 8) == 0:
        tiempo = descanso_largo
        condicion_pomodoro.configure(text="Descanso Largo...")
    elif (reps % 2) == 0:
        tiempo = descanso_corto
        condicion_pomodoro.configure(text="Descanso...")
    else:
        tiempo = pomodoro
        condicion_pomodoro.configure(text="Ora et labora...")
    tiempo_min = tiempo // 60
    tiempo_seg = tiempo % 60
    numeros.configure(text=f"{tiempo_min:02d}:{tiempo_seg:02d}")
    informacion_pomodoro.configure(text=f"Pomodoro {c_pomodoro} | Descanso {c_descanso} | Descanso largo {c_descanso_largo}")

def saltar_instancia():
    
    global reps, c_pomodoro, c_descanso, c_descanso_largo
    
    parar_contador()
    
    #Nota_dev 1: al saltar la instancia, no se ha terminado el pomodoro, por tanto no tiene sentido aumentar su cantidad...
    if (reps % 8) == 0:
        c_descanso_largo += 1 
    elif (reps % 2) == 0:
        c_descanso += 1       
    else:
        c_pomodoro += 1       
        
    reps += 1
    
    reset_contador()
                
def abrir_configuracion ():

    global ventana_config,ruta_icono
    
    #Controla que no se abran mas de una ventana
    if ventana_config is not None and ventana_config.winfo_exists():
        ventana_config.focus()
        return
        
    #Configuración de la Ventana de Configuración 
    ventana_config = ctk.CTkToplevel(app)
    ventana_config.title("Ajustes")
    ventana_config.geometry("230x335")
    ventana_config.configure(fg_color=("white", "black"))
    ventana_config.attributes("-topmost", True)

    #Busca el icono para la ventana de ajustes
    try:
        ventana_config.after(200, lambda: ventana_config.iconbitmap(ruta_icono))
    except Exception:
        pass #Si no lo encuentra no carga nada


    def guardar_ajustes():
        global pomodoro,descanso_largo,descanso_corto

        try:
            nuevo_pomodoro = int(entrada_pomodoro.get()) * 60
            nuevo_descanso_corto = int(entrada_descanso_corto.get()) * 60
            nuevo_descanso_largo = int(entrada_descanso_largo.get()) * 60

            if nuevo_pomodoro <= 0 or nuevo_descanso_corto <= 0 or nuevo_descanso_largo <= 0:
                #print("Los tiempos deben ser mayores a 0") #Nota_dev 2: Agregar popup
                return
            
            pomodoro = nuevo_pomodoro
            descanso_corto = nuevo_descanso_corto
            descanso_largo = nuevo_descanso_largo

            reset_contador()
            ventana_config.destroy()

        except ValueError:
            print("ERROR")
    
    #Cartel Pomodoro
    ctk.CTkLabel(ventana_config, text="Pomodoro (minutos):", text_color=("black", "white"), font=("Consolas", 14)).pack(pady=(20, 5))
    entrada_pomodoro = ctk.CTkEntry(ventana_config, width=100, justify="center")
    entrada_pomodoro.insert(0, str(pomodoro // 60)) 
    entrada_pomodoro.pack()

    #Cartel Descanso Corto
    ctk.CTkLabel(ventana_config, text="Descanso Corto (minutos):", text_color=("black", "white"), font=("Consolas", 14)).pack(pady=(20, 5))
    entrada_descanso_corto = ctk.CTkEntry(ventana_config, width=100, justify="center")
    entrada_descanso_corto.insert(0, str(descanso_corto // 60)) 
    entrada_descanso_corto.pack()

    #Cartel Descanso Largo 
    ctk.CTkLabel(ventana_config, text="Descanso Largo (minutos):", text_color=("black", "white"), font=("Consolas", 14)).pack(pady=(20, 5))
    entrada_descanso_largo = ctk.CTkEntry(ventana_config, width=100, justify="center")
    entrada_descanso_largo.insert(0, str(descanso_largo // 60)) 
    entrada_descanso_largo.pack()

    #Guardar
    boton_guardar = ctk.CTkButton(ventana_config, text="Guardar", fg_color=("black", "white"), text_color=("white", "black"), 
                                  hover_color=("white", "black"), font=("Consolas", 14, "bold"), command=guardar_ajustes)
    boton_guardar.pack(pady=30)

def cambiar_tema():
    modo_actual = ctk.get_appearance_mode()
    
    if modo_actual == "Dark":
        ctk.set_appearance_mode("Light")
        boton_tema.configure(text="🌙") 
    else:
        ctk.set_appearance_mode("Dark")
        boton_tema.configure(text="☀️")

def cambio_oracion():
        global oracion_visible

        if oracion_visible== False:
            widget_oracion.place(relx=0.5, rely=0.5, anchor="center")
            oracion_visible = True
        else:
            widget_oracion.place_forget()
            oracion_visible = False

def reproducir_sonido(ruta_sonido):

    if sistema_actual == "Windows":
        winsound.PlaySound(ruta_sonido,winsound.SND_ASYNC)
    elif sistema_actual == "Linux":
        subprocess.Popen(["aplay","-q",ruta_sonido])

#----------------------------------------Configuración del GUI--------------------------------------------
app = ctk.CTk()
app.title("Cathodoro")
ctk.set_appearance_mode("Dark")
app.configure(fg_color=("white", "black"))

##Variables de la ventana 
ANCHO = 500
LARGO = 600

#Obtención de rutas para las imagenes/sonidos
if getattr(sys, 'frozen', False):
    ruta_carpeta = os.path.dirname(sys.executable)
else:
    ruta_carpeta = os.path.dirname(os.path.realpath(__file__))

ruta_imagen_blanca = os.path.join(ruta_carpeta,"assets_pomodoro","imagen_blanca.png")
ruta_imagen_negra = os.path.join(ruta_carpeta,"assets_pomodoro","imagen_negra.png")
ruta_icono = os.path.join(ruta_carpeta, "icon.ico")
ruta_sonido = os.path.join(ruta_carpeta,"wav_pomodoro","pomodoro_ping.wav")

try:
    app.iconbitmap(ruta_icono)
except Exception:
    pass

#Centrar la ventana al crearse
ancho_pantalla = app.winfo_screenwidth()
largo_pantalla = app.winfo_screenheight()
x_sobrante = (ancho_pantalla - ANCHO)// 2 #Como son pixeles, realizamos una división entera.
y_sobrante = (largo_pantalla - LARGO)// 2
app.geometry(f"{ANCHO}x{LARGO}+{x_sobrante}+{y_sobrante}") #La f toma el valor de los strings y los convierte a su valor entero
#(ANCHO X LARGO) es la altura de la ventana
# +x_sobrante+y_sobrante, donde esta colocada la ventana

#Crear CTkFrame como contenedor invisible para mantener la relación de aspecto
contenedor_maestro = ctk.CTkFrame(app,fg_color="transparent")
contenedor_maestro.pack(expand=True, fill="both")

contenedor_maestro.grid_rowconfigure(0,weight=1) #Creamos una super celda 0, que ocupa todo el espacio, para que al escalarse no modifique el contenido adentro
contenedor_maestro.grid_columnconfigure(0,weight=1)

contenedor_principal = ctk.CTkFrame(contenedor_maestro,fg_color="transparent")
contenedor_principal.grid(row = 0,column=0)

#Contenido del Pomodoro
#Información de los pomodoros
informacion_pomodoro = ctk.CTkLabel(contenedor_principal,text="Pomodoro 0 | Descanso 0 | Descanso largo 0",font=("Consolas",14),text_color=("black", "white"))
informacion_pomodoro.pack(pady=(0,0))

#Rectangulo principal
rectangulo = ctk.CTkFrame(contenedor_principal,fg_color=("white", "black"),border_color=("black", "white"),border_width=2,corner_radius=30) 
rectangulo.pack(pady=10, ipadx=25, ipady=0)

#Imagen
imagen_pomodoro_objeto = None
try:
    imagen_bites_blanca = Image.open(ruta_imagen_blanca)
    imagen_bites_negra = Image.open(ruta_imagen_negra)
    imagen_pomodoro_objeto = ctk.CTkImage(light_image=imagen_bites_negra, dark_image=imagen_bites_blanca,size=(200, 250))
except FileNotFoundError:
    print("ERROR NO PUDO ENCONTRARSE LA IMAGEN")

if imagen_pomodoro_objeto is not None:
    imagen_pomodoro_label=ctk.CTkLabel(rectangulo,text="",image=imagen_pomodoro_objeto)
    imagen_pomodoro_label.pack(pady=(20,10))

#Cronometro
numeros = ctk.CTkLabel(rectangulo,text="25:00",font=("Consola",90),text_color=("black", "white"))
numeros.pack(pady=(5,5))

#Condición pomodoro
condicion_pomodoro=ctk.CTkLabel(rectangulo,text="Ora et labora...",font=("Consolas",11),text_color=("black", "white"))
condicion_pomodoro.pack()

#Contenedor para los controles
contenedor_controles = ctk.CTkFrame(rectangulo,fg_color="transparent")
contenedor_controles.pack(pady=(0,20))

#Boton de Stop
boton_stop= ctk.CTkButton(
        contenedor_controles,
        text="▶",
        font=("Consola",25),
        text_color=("black", "white"),
        fg_color="transparent",
        width = 5,
        height=5,
        #border_width=2,
        #border_color="white",
        #corner_radius=0,
        hover_color=("white", "black"),
        command=iniciar_contador
        )
boton_stop.grid(row=0,column=0,padx=10,pady=10)

#Boton de Reset 
boton_reset= ctk.CTkButton(
        contenedor_controles,
        text="↻",
        font=("Consola",25),
        text_color=("black", "white"),
        fg_color="transparent",
        width = 5,
        height=5,
        #border_width=2,
        #border_color="white",
        #corner_radius=0,
        hover_color=("white", "black"),
        command=reset_contador
        )
boton_reset.grid(row=0,column=1,padx=10,pady=10)

#Boton de Siguiente

boton_siguiente= ctk.CTkButton(
        contenedor_controles,
        text=">>",
        font=("Consola",19),
        text_color=("black", "white"),
        fg_color="transparent",
        width = 5,
        height=5,
        #border_width=2,
        #border_color="white",
        #corner_radius=0,
        hover_color=("white", "black"),
        command=saltar_instancia
        )
boton_siguiente.grid(row=0,column=2,padx=10,pady=10)

#...
oracion_boton = ctk.CTkButton(contenedor_principal,
                       text ="Oración",
                       text_color=("black", "white"),
                       font=("Consola", 13, "normal"),
                       fg_color=("white", "black"),
                       border_color=("black", "white"),
                       border_width=2,
                       corner_radius=7,
                       hover_color=("white", "black"),
                       command=cambio_oracion
)
oracion_boton.pack()

#Boton Configuración
boton_configuracion = ctk.CTkButton(
    app, 
    text="⚙", 
    font=("Consolas", 24),
    width=40, 
    height=40,
    fg_color="transparent",
    text_color=("black", "white"),
    hover_color=("white", "black"),
    command=abrir_configuracion 
)
boton_configuracion.place(relx=0.05, rely=0.95, anchor="sw")

boton_tema = ctk.CTkButton(
    app, 
    text="☀️", 
    font=("Consolas", 24),
    width=40, 
    height=40,
    fg_color="transparent",
    text_color=("black", "white"),
    hover_color=("#cccccc", "#333333"),
    command=cambiar_tema
)
boton_tema.place(relx=0.95, rely=0.95, anchor="se")

widget_oracion = ctk.CTkFrame(app, fg_color=("white", "black"), border_color=("black", "white"), border_width=2, corner_radius=15)

texto_oracion = """Oh Espíritu Santo,
Amor del Padre, y del Hijo,
Inspírame siempre lo que debo pensar,
lo que debo decir,
cómo debo decirlo,
lo que debo callar,
cómo debo actuar,
lo que debo hacer,
para gloria de Dios,
bien de las almas
y mi propia Santificación.

Espíritu Santo,
Dame agudeza
para entender,
capacidad para retener,
método y facultad para aprender,
sutileza para interpretar,
gracia y eficacia para hablar.
Dame acierto al empezar
dirección al progresar
y perfección al acabar.
Amén."""

label_oracion = ctk.CTkLabel(
    widget_oracion, 
    text=texto_oracion, 
    font=("Consolas", 14, "italic"), 
    text_color=("black", "white"),
    justify="center"
)
label_oracion.pack(padx=30, pady=30)

app.mainloop()

