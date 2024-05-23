import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import QPropertyAnimation,QEasingCurve
from PyQt6 import QtCore, QtWidgets
from PyQt6.uic import loadUi
from models import *
from repository import *


#importe ui de la ventana principal
from crud_datos_cineticos_ui import Ui_MainWindow
from repository import *

# Crear pantalla principal 
class PantallaCrud(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.id = self.DatosIngresadosCineticos.id
        
        self.DatosIngresadosCineticos = DatosIngresadosCineticos()
        self.DatosCineticosManejador = DatosCineticosManejador()
        # UI elementos

        # ingreso de textos
        self.tiempo = self.ui.tiempo_edit
        self.concentracion = self.ui.concentracion_edit
        self.otra_propiedad = self.ui.otra_propiedad_edit
        self.conversion_reactivo_limitante = self.ui.conversion_reactivo_limitante_edit
        self.tipo_especie = self.ui.tipo_especie_edit
        self.id_condiciones_iniciales = self.ui.id_condiciones_iniciales_edit
        self.nombre_data = self.ui.nombre_data_edit
        self.nombre_reaccion = self.ui.nombre_reaccion_edit
        self.especie_quimica = self.ui.especie_quimica_edit
        # botones
        self.agregar_btn = self.ui.agregar_btn
        self.actualizar_btn = self.ui.actualizar_btn
        self.seleccionar_btn = self.ui.selecionar_btn
        self.buscar_btn = self.ui.buscar_btn
        self.limpiar_btn = self.ui.limpiar_btn
        self.borrar_btn = self.ui.borrar_btn

        # tabla
        self.tabla_datos = self.ui.tableWidget
        self.tabla_datos.setSortingEnabled(False)
        self.lista_botones = self.ui.funciones_frame.findChildren(QPushButton)

        #inicializar signal_slot
        self.init_signal_slot()
        #self.cargar_datos_tabla()
        self.buscar_dato()


    # Conectar botones
    def init_signal_slot(self):
        self.agregar_btn.clicked.connect(self.agregar_dato)
        self.actualizar_btn.clicked.connect(self.actualizar_dato)
        self.seleccionar_btn.clicked.connect(self.seleccionar_dato)
        self.borrar_btn.clicked.connect(self.borrar_dato)
        self.limpiar_btn.clicked.connect(self.limpiar_formulario)
        self.buscar_btn.clicked.connect(self.buscar_dato)


    def cargar_datos_tabla(self):
        pass

    def agregar_dato(self):
        self.boton_desactivado()

        dato = DatosIngresadosCineticos(
            tiempo=float(self.tiempo.text()),
            concentracion=float(self.concentracion.text()),
            otra_propiedad=float(self.otra_propiedad.text()),
            conversion_reactivo_limitante=float(self.conversion_reactivo_limitante.text()),
            tipo_especie=self.tipo_especie.text(),
            id_condiciones_iniciales=int(self.id_condiciones_iniciales.text()),
            nombre_data=self.nombre_data.text(),
            nombre_reaccion=self.nombre_reaccion.text(),
            especie_quimica=self.especie_quimica.text(),
        )

        agregar_resultado = self.DatosCineticosManejador.agregar_dato(dato)

        if agregar_resultado:
            QMessageBox.information(self, "Información", "Datos agregados correctamente", QMessageBox.StandardButton.Ok)
        else:
            QMessageBox.information(self, "Información", "Hubo un problema al agregar los datos", QMessageBox.StandardButton.Ok)

        self.boton_activado()



    def limpiar_formulario(self):
        #limpia formulario
        self.tiempo.clear()
        self.concentracion.clear()
        self.otra_propiedad.clear()
        self.conversion_reactivo_limitante.clear()
        self.tipo_especie.clear()
        self.id_condiciones_iniciales.clear()
        self.nombre_data.clear()
        self.nombre_reaccion.clear()
        self.especie_quimica.clear()
        self.id.clear()
        self.id.setEnabled(True)



    def seleccionar_dato(self):
        selecionar_fila = self.tabla_datos.currentRow()
        if selecionar_fila != -1:
            self.id.setEnabled(False)
            id = self.tabla_datos.item(selecionar_fila, 0).text().strip()
            tiempo = self.tabla_datos.item(selecionar_fila, 1).text().strip()
            concentracion = self.tabla_datos.item(selecionar_fila, 2).text().strip()
            otra_propiedad = self.tabla_datos.item(selecionar_fila, 3).text().strip()
            conversion_reactivo_limitante = self.tabla_datos.item(selecionar_fila, 4).text().strip()
            tipo_especie = self.tabla_datos.item(selecionar_fila, 5).text().strip()
            id_condiciones_iniciales = self.tabla_datos.item(selecionar_fila, 6).text().strip()
            nombre_data = self.tabla_datos.item(selecionar_fila, 7).text().strip()
            nombre_reaccion = self.tabla_datos.item(selecionar_fila, 8).text().strip()
            especie_quimica = self.tabla_datos.item(selecionar_fila, 9).text().strip()

            self.tiempo.setText(tiempo)
            self.concentracion.setText(concentracion)
            self.otra_propiedad.setText(otra_propiedad)
            self.conversion_reactivo_limitante.setText(conversion_reactivo_limitante)
            self.tipo_especie.setText(tipo_especie)
            self.id_condiciones_iniciales.setText(id_condiciones_iniciales)
            self.nombre_data.setText(nombre_data)
            self.nombre_reaccion.setText(nombre_reaccion)
            self.especie_quimica.setText(especie_quimica)
        else:
            QMessageBox.information(self, "Información", "Seleccione una fila", QMessageBox.StandardButton.Ok)
            return



    def actualizar_dato(self):
        #cactualiza datos
        nuevo_dato = self.consultar_datos_ingresados_cineticos()
        dato = DatosIngresadosCineticos(
            tiempo=float(self.tiempo.text()),
            concentracion=float(self.concentracion.text()),
            otra_propiedad=float(self.otra_propiedad.text()),
            conversion_reactivo_limitante=float(self.conversion_reactivo_limitante.text()),
            tipo_especie=self.tipo_especie.text(),
            id_condiciones_iniciales=int(self.id_condiciones_iniciales.text()),
            nombre_data=self.nombre_data.text(),
            nombre_reaccion=self.nombre_reaccion.text(),
            especie_quimica=self.especie_quimica.text(),
        )

        if nuevo_dato["id"]:
            actualiza_resultado = self.DatosCineticosManejador.actualizar_dato(nuevo_dato["id"], dato)

    def borrar_dato(self):
        fila_seleccionada = self.tabla_datos.currentRow()
        if fila_seleccionada != -1:
            opcion_seleccionada = QMessageBox.question(self, "Eliminar dato", "¿Estás seguro de eliminar el dato?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if opcion_seleccionada == QMessageBox.StandardButton.Yes:
                id = self.tabla_datos.item(fila_seleccionada, 0).text().strip()
                borrar_resultado = self.DatosCineticosManejador.borrar_dato(id)
                if borrar_resultado:
                    QMessageBox.information(self, "Información", "Dato eliminado correctamente", QMessageBox.StandardButton.Ok)
                    self.buscar_dato()
                else:
                    QMessageBox.information(self, "Información", "Hubo un problema al eliminar el dato", QMessageBox.StandardButton.Ok)



    def buscar_dato(self):
        self.consultar_datos_ingresados_cineticos()

        datos_resultados = self.DatosCineticosManejador.consultar_datos()
        self.mostrar_datos_tabla(datos_resultados)



    def boton_desactivado(self):
        for button in self.lista_botones:
            button.setDisabled(True)

    def boton_activado(self):
        for button in self.lista_botones:
            button.setDisabled(False)

    def consultar_datos_ingresados_cineticos(self):
        #proviene de el formulario
        id_datos_ingresados_cineticos = self.id.text().strip()
        tiempo = self.tiempo.text().strip()
        concentracion = self.concentracion.text().strip()
        otra_propiedad = self.otra_propiedad.text().strip()
        conversion_reactivo_limitante = self.conversion_reactivo_limitante.text().strip()
        tipo_especie = self.tipo_especie.text().strip()
        id_condiciones_iniciales = self.id_condiciones_iniciales.text().strip()
        nombre_data = self.nombre_data.text().strip()
        nombre_reaccion = self.nombre_reaccion.text().strip()
        especie_quimica = self.especie_quimica.text().strip()

        datos_ingresados_cineticos = {
            'id': id_datos_ingresados_cineticos,
            'tiempo': tiempo,
            'concentracion': concentracion,
            'otra_propiedad': otra_propiedad,
            'conversion_reactivo_limitante': conversion_reactivo_limitante,
            'tipo_especie': tipo_especie,
            'id_condiciones_iniciales': id_condiciones_iniciales,
            'nombre_data': nombre_data,
            'nombre_reaccion': nombre_reaccion,
            'especie_quimica': especie_quimica
        
        }
    def comprobar_datos(self, id_datos_ingresados_cineticos,nombre_data):
        #comprobar si el id existe
        resultado = self.DatosCineticosManejador.consultar_dato_por_id_conjunto_datos(id_datos_ingresados_cineticos,nombre_data)
        
        return resultado
    
    def mostrar_datos_tabla(self,resultados):
        if resultados:
            self.tabla_datos.setRowCount(0)
            self.tabla_datos.setColumnCount(len(resultados))

            for fila, info in enumerate(resultados):
                info_lista = info["id", "tiempo", "concentracion", "otra_propiedad", "conversion_reactivo_limitante", "tipo_especie", "id_condiciones_iniciales", "nombre_data", "nombre_reaccion", "especie_quimica"]
                for columna, item in enumerate(info_lista):
                    celda_item = QTableWidgetItem(str(item))
                    self.tabla_datos.setItem(fila, columna, celda_item)
        else:
            self.tabla_datos.setRowCount(0)
            QMessageBox.information(self, "Información", "No se encontraron datos", QMessageBox.StandardButton.Ok)
            return

#entrada de aplicacion
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PantallaCrud()
    window.show()
    sys.exit(app.exec())