from models.timer import CathodoroModel
from views.main_view import CathodoroView
from controllers.timer_controller import CathodoroController

def main():
    modelo = CathodoroModel()
    vista = CathodoroView()
    controlador = CathodoroController(modelo, vista)
    
    vista.mainloop()

if __name__ == "__main__":
    main()