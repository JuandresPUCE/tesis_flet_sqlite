import flet as ft
import time

class AnimatedApp(ft.UserControl):
    def __init__(self,page):
        super().__init__()
        self.page=page

        self.color_container = ft.colors.BLACK87
        self.color_items = ft.colors.BLUE
        self.color_selecr_items = ft.colors.BLUE_400
        self.color_icons_ligth = ft.colors.BLACK
        self.color_icons_dark = ft.colors.WHITE


        self.animation_style = ft.animation.Animation(100, ft.AnimationCurve.EASE_IN_TO_LINEAR)

        self.mode_switch = ft.Switch(
            value=True,
            on_change= self.mode_change_update,

        )


        self.bt_home= ft.Container(
            width=70,
            height=60,
            bgcolor=self.color_container,
            border_radius=10,
            alignment=ft.alignment.center,
            content=ft.IconButton(icon=ft.icons.HOME,
                                  icon_color=self.color_icons_dark,
                                  on_click=self.bar_icons)
        )

        self.frame_title = ft.Container(
            expand=True,
            height=60,
            bgcolor=self.color_container,
            border_radius=10,
            alignment=ft.alignment.center,
            content=ft.Text("test", size=30)
        )

        self.navigation = ft.Container(
            bgcolor=self.color_container,
            animate_size=self.animation_style,
            width=200,
            border_radius=10,
            padding=20,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        expand=True,
                        content=ft.Column(
                            spacing=10,
                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            controls=[

                            ]
                        )
                    )
                ]
            )


        )

        self.page.add(ft.Column(
            expand=True,
            controls=[
                ft.Row(
                    controls=[
                        self.bt_home,
                        self.frame_title,
                    ]
                ),
                ft.Row(
                    controls=[
                        self.bt_home,
                    ]
                ),

                    ]           
        ))

    def bar_icons(self):
        pass

    def mode_change_update(self):
        pass



ft.app(target=AnimatedApp)