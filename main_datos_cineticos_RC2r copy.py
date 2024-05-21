import flet as ft
from fpdf import FPDF
import pandas as pd
import datetime
from modelos import DatosIngresadosCineticos, DatosCineticosMananger

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Tabla de Datos Cinéticos', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

class FormUi(ft.UserControl):
    def __init__(self, page):
        super().__init__(expand=True)
        self.page = page 
        self.data_manager = DatosCineticosMananger()
        self.selected_row = None


        self.search_field = ft.TextField(
            suffix_icon=ft.icons.SEARCH,
            label="Buscar por nombre de data",
            border=ft.InputBorder.UNDERLINE,
            border_color="white",
            label_style=ft.TextStyle(color="white"),
            on_change=self.search_data,
        )

        self.data_table = ft.DataTable(
            expand=True,
            border=ft.border.all(2, "blue"),
            data_row_color={ft.MaterialState.SELECTED: "blue", ft.MaterialState.PRESSED: "black"},
            border_radius=10,
            #show_checkbox_column=True,
            columns=[
                ft.DataColumn(ft.Text("Tiempo", color="blue", weight="bold",overflow=ft.TextOverflow.VISIBLE)),
                ft.DataColumn(ft.Text("Concentración", color="blue", weight="bold",overflow=ft.TextOverflow.VISIBLE)),
                ft.DataColumn(ft.Text("Otra Propiedad", color="blue", weight="bold",overflow=ft.TextOverflow.VISIBLE)),
                ft.DataColumn(ft.Text("Conversión Reactivo Limitante", color="blue", weight="bold",overflow=ft.TextOverflow.VISIBLE)),
                ft.DataColumn(ft.Text("Tipo de Especie", color="blue", weight="bold",overflow=ft.TextOverflow.VISIBLE)),
                ft.DataColumn(ft.Text("ID Condiciones Iniciales", color="blue", weight="bold",overflow=ft.TextOverflow.VISIBLE)),
                ft.DataColumn(ft.Text("Nombre Data", color="blue", weight="bold",overflow=ft.TextOverflow.VISIBLE)),
                ft.DataColumn(ft.Text("Nombre Reacción", color="blue", weight="bold",overflow=ft.TextOverflow.VISIBLE)),
                ft.DataColumn(ft.Text("Especie Química", color="blue", weight="bold",overflow=ft.TextOverflow.VISIBLE)),
            ],
        )

        self.show_data()

        self.table = ft.Container(
            bgcolor="#222222",
            border_radius=10,
            padding=10,
            col=12,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Container(
                        padding=10,
                        content=ft.Row(
                            controls=[
                                self.search_field,                               
                            ]
                        ),
                    ),
                    ft.Column(
                        expand=True,
                        scroll="auto",
                        controls=[
                            ft.ResponsiveRow([self.data_table]),
                        ],
                    ),
                ],
            ),
        )

        self.content = ft.ResponsiveRow(
            controls=[

                self.table,
            ]
        )

    def show_data(self):
        self.data_table.rows = []
        for x in self.data_manager.get_datos():
            self.data_table.rows.append(
                ft.DataRow(
                    on_select_changed=self.get_index,
                    cells=[
                        ft.DataCell(ft.Text(str(x.tiempo))),
                        ft.DataCell(ft.Text(str(x.concentracion))),
                        ft.DataCell(ft.Text(str(x.otra_propiedad))),
                        ft.DataCell(ft.Text(str(x.conversion_reactivo_limitante))),
                        ft.DataCell(ft.Text(x.tipo_especie)),
                        ft.DataCell(ft.Text(str(x.id_condiciones_iniciales))),
                        ft.DataCell(ft.Text(x.nombre_data)),
                        ft.DataCell(ft.Text(x.nombre_reaccion)),
                        ft.DataCell(ft.Text(x.especie_quimica)),
                    ],
                )
            )
        self.update()

    def add_data(self, e):
        dato = DatosIngresadosCineticos(
            tiempo=float(self.tiempo.value),
            concentracion=float(self.concentracion.value),
            otra_propiedad=float(self.otra_propiedad.value),
            conversion_reactivo_limitante=float(self.conversion_reactivo_limitante.value),
            tipo_especie=self.tipo_especie.value,
            id_condiciones_iniciales=int(self.id_condiciones_iniciales.value),
            nombre_data=self.nombre_data.value,
            nombre_reaccion=self.nombre_reaccion.value,
            especie_quimica=self.especie_quimica.value,
        )

        if all([self.tiempo.value, self.concentracion.value, self.otra_propiedad.value, self.conversion_reactivo_limitante.value, self.tipo_especie.value, self.id_condiciones_iniciales.value, self.nombre_data.value, self.nombre_reaccion.value, self.especie_quimica.value]):
            self.data_manager.add_dato(dato)
            self.clean_fields()
            self.show_data()
        else:
            print("Por favor complete todos los campos")

    def get_index(self, e):
        if e.control.selected:
            e.control.selected = False
        else:
            e.control.selected = True
        nombre_data = e.control.cells[6].content.value
        for row in self.data_manager.get_datos():
            if row.nombre_data == nombre_data:
                self.selected_row = row
                break
        self.update()

    def edit_field_text(self, e):
        if self.selected_row:
            self.tiempo.value = str(self.selected_row.tiempo)
            self.concentracion.value = str(self.selected_row.concentracion)
            self.otra_propiedad.value = str(self.selected_row.otra_propiedad)
            self.conversion_reactivo_limitante.value = str(self.selected_row.conversion_reactivo_limitante)
            self.tipo_especie.value = self.selected_row.tipo_especie
            self.id_condiciones_iniciales.value = str(self.selected_row.id_condiciones_iniciales)
            self.nombre_data.value = self.selected_row.nombre_data
            self.nombre_reaccion.value = self.selected_row.nombre_reaccion
            self.especie_quimica.value = self.selected_row.especie_quimica
            self.update()
        else:
            print("Seleccione una fila para editar")

    def update_data(self, e):
        if self.selected_row:
            updated_dato = {
                'tiempo': float(self.tiempo.value),
                'concentracion': float(self.concentracion.value),
                'otra_propiedad': float(self.otra_propiedad.value),
                'conversion_reactivo_limitante': float(self.conversion_reactivo_limitante.value),
                'tipo_especie': self.tipo_especie.value,
                'id_condiciones_iniciales': int(self.id_condiciones_iniciales.value),
                'nombre_data': self.nombre_data.value,
                'nombre_reaccion': self.nombre_reaccion.value,
                'especie_quimica': self.especie_quimica.value,
            }
            self.data_manager.update_dato(self.selected_row.id, updated_dato)
            self.clean_fields()
            self.show_data()
        else:
            print("Seleccione una fila para actualizar")

    def delete_data(self, e):
        if self.selected_row:
            self.data_manager.delete_dato(self.selected_row.id)
            self.clean_fields()
            self.show_data()
        else:
            print("Seleccione una fila para borrar")

    def search_data(self, e):
        search = self.search_field.value.lower()
        filtered_data = list(filter(lambda x: search in x.nombre_data.lower(), self.data_manager.get_datos()))
        self.data_table.rows = []
        if search:
            for x in filtered_data:
                self.data_table.rows.append(
                    ft.DataRow(
                        on_select_changed=self.get_index,
                        cells=[
                            ft.DataCell(ft.Text(str(x.tiempo))),
                            ft.DataCell(ft.Text(str(x.concentracion))),
                            ft.DataCell(ft.Text(str(x.otra_propiedad))),
                            ft.DataCell(ft.Text(str(x.conversion_reactivo_limitante))),
                            ft.DataCell(ft.Text(x.tipo_especie)),
                            ft.DataCell(ft.Text(str(x.id_condiciones_iniciales))),
                            ft.DataCell(ft.Text(x.nombre_data)),
                            ft.DataCell(ft.Text(x.nombre_reaccion)),
                            ft.DataCell(ft.Text(x.especie_quimica)),
                        ],
                    )
                )
            self.update()
        else:
            self.show_data()

    def clean_fields(self):
        self.tiempo.value = ""
        self.concentracion.value = ""
        self.otra_propiedad.value = ""
        self.conversion_reactivo_limitante.value = ""
        self.tipo_especie.value = ""
        self.id_condiciones_iniciales.value = ""
        self.nombre_data.value = ""
        self.nombre_reaccion.value = ""
        self.especie_quimica.value = ""
        self.update()

    def save_pdf(self, e):
        pdf = PDF()
        pdf.add_page()
        column_widths = [20, 40, 40, 40, 40, 40, 40, 40, 40]
        # Agregar filas a la tabla
        datos = self.data_manager.get_datos()
        header = ("Tiempo", "Concentración", "Otra Propiedad", "Conversión Reactivo Limitante", "Tipo Especie", "ID Condiciones Iniciales", "Nombre Data", "Nombre Reacción", "Especie Química")
        pdf.cell(0, 10, 'Datos Cinéticos', 0, 1, 'C')
        for item, width in zip(header, column_widths):
            pdf.cell(width, 10, str(item), border=1)
        pdf.ln()
        for row in datos:
            for item, width in zip([row.tiempo, row.concentracion, row.otra_propiedad, row.conversion_reactivo_limitante, row.tipo_especie, row.id_condiciones_iniciales, row.nombre_data, row.nombre_reaccion, row.especie_quimica], column_widths):
                pdf.cell(width, 10, str(item), border=1)
            pdf.ln()
        file_name = datetime.datetime.now().strftime("DATA %Y-%m-%d_%H-%M-%S") + ".pdf"
        pdf.output(file_name)

    def save_excel(self, e):
        file_name = datetime.datetime.now().strftime("DATA %Y-%m-%d_%H-%M-%S") + ".xlsx"
        datos = self.data_manager.get_datos()
        df = pd.DataFrame([{
            "Tiempo": dato.tiempo,
            "Concentración": dato.concentracion,
            "Otra Propiedad": dato.otra_propiedad,
            "Conversión Reactivo Limitante": dato.conversion_reactivo_limitante,
            "Tipo Especie": dato.tipo_especie,
            "ID Condiciones Iniciales": dato.id_condiciones_iniciales,
            "Nombre Data": dato.nombre_data,
            "Nombre Reacción": dato.nombre_reaccion,
            "Especie Química": dato.especie_quimica,
        } for dato in datos])
        df.to_excel(file_name, index=False)

    def build(self):
        return self.content

def main(page: ft.Page):
    page.bgcolor = "black"
    page.title = "dashboard"
    page.window_min_width = 1100
    page.window_min_height = 500
    form_ui = FormUi(page)
    page.add(form_ui)

#ft.app(main)
ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8585)
