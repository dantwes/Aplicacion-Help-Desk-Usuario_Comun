import sys
from PyQt6 import QtWidgets, uic, QtCore

class KintsugiTerminal(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # 1. Cargamos el cascarón visual de Qt Designer
        uic.loadUi("ventana_helpdesk.ui", self)
        
        # 2. Conectamos los botones de tu barra lateral con el contenedor de la derecha
        # .setCurrentIndex(int) le dice al QStackedWidget qué número de página mostrar
        self.btn_menu_redes.clicked.connect(lambda: self.paginas_contenido.setCurrentIndex(0))
        self.btn_menu_monitoreo.clicked.connect(lambda: self.paginas_contenido.setCurrentIndex(1))
        self.btn_menu_info.clicked.connect(lambda: self.paginas_contenido.setCurrentIndex(2))
        self.btn_menu_sensores.clicked.connect(lambda: self.paginas_contenido.setCurrentIndex(3))
        self.btn_action_ping.clicked.connect(lambda: self.pag_ping.setCurrentIndex(1))
        # 3. Mensaje inicial de consola para saber que todo cargó bien
        print("Kintsugi Terminal iniciada correctamente.")

        self.ping_action_ping.clicked.connect(self.iniciar_ping)
        
        # 2. Creamos el proceso invisible que ejecutará los comandos de Windows
        self.proceso_sistema = QtCore.QProcess(self)
        
        # 3. Le decimos al proceso que cuando reciba texto de la CMD, ejecute "leer_consola"
        self.proceso_sistema.readyReadStandardOutput.connect(self.leer_consola)

    def iniciar_ping(self):
        # Capturamos la IP que escribiste en la caja de texto
        direccion_ip = self.txt_ping_ping.text()
        
        if not direccion_ip:
            self.consola_resultados.setText("Por favor, escribe una dirección IP o dominio válido.")
            return

        self.consola_resultados.clear()
        self.consola_resultados.append(f"Haciendo ping a: {direccion_ip}...\n")
        
        # Ejecutamos el comando nativo de Windows: ping direccion_ip
        # El parámetro "-n 4" le dice que solo mande 4 paquetes (comportamiento estándar)
        self.proceso_sistema.start("ping", [direccion_ip, "-n", "4"])

    def leer_consola(self):
        # Lee lo que la CMD invisible de Windows está respondiendo
        lineas_texto = self.proceso_sistema.readAllStandardOutput().data().decode('cp1252', errors='ignore')
        # Lo añade directamente a tu cuadro grande de texto en la interfaz
        self.consola_resultados.append(lineas_texto)

# Configuración estándar para arrancar la interfaz gráfica
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = KintsugiTerminal()
    ventana.show()
    sys.exit(app.exec())
