import flet as ft
import sqlite3

def main(page:ft.Page):
    page.bgcolor = "#425761"

    conexao = sqlite3.connect("banco_de dados.db")
    cursor = conexao.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS contas_bancarias(
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    titular TEXT NOT NULL,
                    saldo FLOAT NOT NULL,
                    idade TEXT NOT NULL)""")


    def att_pesquisas():
        cursor.execute("SELECT * FROM contas_bancarias")
        contas = cursor.fetchall()

        cards = []

        for id, titular, saldo_, idade_ in contas:

            card = ft.Container(
                col={"xs":12, "sm":6, "md":6, "lg":6},
                height=100,
                border_radius=10,
                bgcolor="#6E93A5",
                padding=20,
                alignment=ft.alignment.center,
                content=ft.Row(
                    spacing=30,
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text("Nome:", weight="bold", color="white"),
                                ft.Text(titular, color="white"),
                            ]
                        ),
                        ft.Column(
                            controls=[
                                ft.Text("Saldo:", weight="bold", color="white"),
                                ft.Text(f"R${saldo_:.2f}", color="white"),
                            ]
                        ),
                        ft.Container(expand=True),
                    ]
                ),
            )

            cards.append(card)

        return ft.ResponsiveRow(controls=cards)



    main_pesquisar = ft.Column(
        expand=True,
        controls=[
            att_pesquisas()
        ],
        scroll="hidden"
    )

    pesquisar_pessoas = ft.TextField(
        hint_text="Pesquisar",
        content_padding=0,
        border_color="transparent",
        hint_style=ft.TextStyle(color="white"),
        cursor_color="white",
        expand=True
    )
    
    total_pessoas=ft.Text(
        value=0,
        weight="bold",
        color="white",
        size=32
    )

    menores = ft.Text(
        value=0,
        color="white",
        weight="bold",
        size=24
    )

    saldo_total=ft.Text(
        value="R$00,00",
        color="white",
        weight="bold",
        size=24
    )

    nome=ft.TextField(
        hint_text="Nome Titular",
        color="white",
        content_padding=0,
        border_color="transparent",
        hint_style=ft.TextStyle(color="white"),
        cursor_color="white",
        expand=True
    )
    idade=ft.TextField(
        hint_text="Idade",
        color="white",
        content_padding=0,
        border_color="transparent",
        hint_style=ft.TextStyle(color="white"),
        cursor_color="white",
        expand=True
    )
    saldo=ft.TextField(
        hint_text="Saldo em dinheiro",
        color="white",
        content_padding=0,
        border_color="transparent",
        hint_style=ft.TextStyle(color="white"),
        cursor_color="white",
        expand=True
    )

    def adicionar(e):
        nome.border_color = "transparent"
        saldo.border_color = "transparent"
        idade.border_color = "transparent"
        main_cont.clean()
        bar_bottom.visible = False
        floating_buttom.visible = False
        main_cont.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            icon_color="white",
                            icon_size=30,
                            on_click=home
                        ),
                        ft.Text(
                            "Cadastrar pessoa",
                            weight="bold",
                            size=30,
                            color="white",
                            text_align="center"
                        )
                    ]
                ),
                ft.Container(
                    padding=10,
                    height=50,
                    border_radius=10,
                    border=ft.border.all(color="white",width=1),
                    content=ft.Row(
                        controls=[
                            ft.Icon(
                                "PEOPLE",
                                color="white"
                            ),
                            nome
                        ]
                    )
                ),
                ft.Container(
                    padding=10,
                    height=50,
                    border_radius=10,
                    border=ft.border.all(color="white",width=1),
                    content=ft.Row(
                        controls=[
                            ft.Icon(
                                ft.Icons.NUMBERS,
                                color="white"
                            ),
                            idade
                        ]
                    )
                ),
                ft.Container(
                    padding=10,
                    height=50,
                    border_radius=10,
                    border=ft.border.all(color="white",width=1),
                    content=ft.Row(
                        controls=[
                            ft.Icon(
                                ft.Icons.ATTACH_MONEY,
                                color="white"
                            ),
                            saldo
                        ]
                    )
                ),
                ft.Container(
                    height=50,
                    alignment=ft.alignment.center,
                    border_radius=10,
                    bgcolor="#6E93A5",
                    content=ft.Text(
                        "Cadastrar",
                        color="white",
                        weight="bold"
                    ),
                    ink=True,
                    on_click=cadastrar
                )
            ]
        )
        page.update()


    def pesquisar_filtros(e):
        cursor.execute("""
            SELECT id,titular, saldo, idade FROM contas_bancarias
            WHERE titular LIKE ?
        """, (pesquisar_pessoas.value,))

        contas = cursor.fetchall()

        nome.border_color = "white"
        saldo.border_color = "white"
        idade.border_color = "white"
        main_pesquisar.controls.clear()


        def delete_pessoa(e):
            cursor.execute(f"""DELETE FROM contas_bancarias
                        WHERE id = ?""",(id,))
            conexao.commit()
            conexao.close()
            main_pesquisar.controls.controls.pop(-1)
            snackbar = ft.SnackBar(ft.Text(f"Titular: {titular} removido com sucesso!"),bgcolor="green",duration=2000)
            page.overlay.append(snackbar)
            snackbar.open = True
            page.update()


        for conta in contas:
            id,titular,saldo_,idade_ = conta

            nome.value = titular
            saldo.value = saldo_
            idade.value = idade_
            
            def editar(e):
                cursor.execute("""UPDATE contas_bancarias
                            SET titular = ?, saldo = ?, idade = ?
                            WHERE id = ?""",(nome.value,saldo.value,idade.value,id))
                close_dlg(e)
                pesquisar_filtros(e)
                snackbar_ = ft.SnackBar(ft.Text(f"Titular: {titular} editado com sucesso!"),bgcolor="green",duration=2000)
                page.overlay.append(snackbar_)
                snackbar_.open = True
                conexao.commit()
                page.update()

            def close_dlg(e):
                dlg_modal.open = False
                e.control.page.update()

            def open_dlg_modal(e):
                e.control.page.overlay.append(dlg_modal)
                dlg_modal.open = True
                e.control.page.update()


            dlg_modal = ft.AlertDialog(
                bgcolor="#1C303A",
                actions_padding=10,
                modal=True,
                title=ft.Text("Editando Conta",color="white"),
                content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            nome,
                        saldo,
                        idade,
                        ft.Container(
                            height=50,
                            alignment=ft.alignment.center,
                            border_radius=10,
                            bgcolor="#6E93A5",
                            content=ft.Text(
                                "Editar",
                                color="white",
                                weight="bold"
                            ),
                            ink=True,
                            on_click=editar
                        ),
                        ft.Container(
                            height=50,
                            alignment=ft.alignment.center,
                            border_radius=10,
                            bgcolor="RED",
                            content=ft.Text(
                                "Cancelar",
                                color="white",
                                weight="bold"
                            ),
                            ink=True,
                            on_click=close_dlg
                        )
                    ]
                ),
                actions_alignment=ft.MainAxisAlignment.END,
                on_dismiss=lambda e: print("Modal dialog dismissed!"),
            )
            att_pesquisas = ft.ResponsiveRow(
                controls=[
                    ft.Container(
                        col={"xs":12,"sm":6,"md":6,"lg":6},
                        height=100,
                        border_radius=10,
                        bgcolor="#6E93A5",
                        padding=20,
                        alignment=ft.alignment.center,
                        content=ft.Row(
                            spacing=30,
                            controls=[
                                ft.Column(
                                    controls=[
                                        ft.Text(
                                            "Nome:",
                                            weight="bold",
                                            color="white"
                                        ),
                                        ft.Text(
                                            value=titular,
                                            color="white",
                                        )
                                    ]
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Text(
                                            "Saldo:",
                                            weight="bold",
                                            color="white"
                                        ),
                                        ft.Text(
                                            value=f"R${saldo_:.2f}",
                                            color="white",
                                        )
                                    ]
                                ),
                                ft.Container(expand=True),
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    icon_color="green",
                                    on_click=open_dlg_modal
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_color="RED",
                                    on_click=delete_pessoa
                                )
                            ]
                        )
                    )
                ]
            )

            main_pesquisar.controls.append(att_pesquisas)
            page.update()



    def pesquisar(e):
        main_cont.clean()
        bar_bottom.visible = True
        floating_buttom.visible = True
        home_btn.content.controls[0].color = "white"
        pesquisar_btn.content.controls[0].color = "#6E93A5"

        def changes_filtros(e):
            main_pesquisar.controls.clear()
            if filtros.value == "Menor de 18 anos":
                main_pesquisar.controls.clear()
                cursor.execute("""SELECT id,titular,saldo,idade FROM contas_bancarias
                           WHERE idade < 18""")
                contas = cursor.fetchall()

                for id, titular, saldo_, idade_ in contas:
                    
                    def editar(e):
                        cursor.execute("""UPDATE contas_bancarias
                                    SET titular = ?, saldo = ?, idade = ?
                                    WHERE id = ?""",(nome.value,saldo.value,idade.value,id))
                        close_dlg(e)
                        pesquisar_filtros(e)
                        snackbar_ = ft.SnackBar(ft.Text(f"Titular: {titular} editado com sucesso!"),bgcolor="green",duration=2000)
                        page.overlay.append(snackbar_)
                        snackbar_.open = True
                        conexao.commit()
                        page.update()

                    def close_dlg(e):
                        dlg_modal.open = False
                        e.control.page.update()

                    def open_dlg_modal(e):
                        e.control.page.overlay.append(dlg_modal)
                        dlg_modal.open = True
                        e.control.page.update()


                    dlg_modal = ft.AlertDialog(
                        bgcolor="#1C303A",
                        actions_padding=10,
                        modal=True,
                        title=ft.Text("Editando Conta",color="white"),
                        content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    nome,
                                saldo,
                                idade,
                                ft.Container(
                                    height=50,
                                    alignment=ft.alignment.center,
                                    border_radius=10,
                                    bgcolor="#6E93A5",
                                    content=ft.Text(
                                        "Editar",
                                        color="white",
                                        weight="bold"
                                    ),
                                    ink=True,
                                    on_click=editar
                                ),
                                ft.Container(
                                    height=50,
                                    alignment=ft.alignment.center,
                                    border_radius=10,
                                    bgcolor="RED",
                                    content=ft.Text(
                                        "Cancelar",
                                        color="white",
                                        weight="bold"
                                    ),
                                    ink=True,
                                    on_click=close_dlg
                                )
                            ]
                        ),
                        actions_alignment=ft.MainAxisAlignment.END,
                        on_dismiss=lambda e: print("Modal dialog dismissed!"),
                    )

                    def delete_pessoa(e):
                        cursor.execute(f"""DELETE FROM contas_bancarias
                                    WHERE id = ?""",(id,))
                        conexao.commit()
                        conexao.close()
                        main_pesquisar.controls.controls.pop(-1)
                        snackbar = ft.SnackBar(ft.Text(f"Titular: {titular} removido com sucesso!"),bgcolor="green",duration=2000)
                        page.overlay.append(snackbar)
                        snackbar.open = True
                        page.update()

                    att_pesquisas = ft.ResponsiveRow(
                        controls=[
                            ft.Container(
                                col={"xs":12,"sm":6,"md":6,"lg":6},
                                height=100,
                                border_radius=10,
                                bgcolor="#6E93A5",
                                padding=20,
                                alignment=ft.alignment.center,
                                content=ft.Row(
                                    spacing=30,
                                    controls=[
                                        ft.Column(
                                            controls=[
                                                ft.Text(
                                                    "Nome:",
                                                    weight="bold",
                                                    color="white"
                                                ),
                                                ft.Text(
                                                    value=titular,
                                                    color="white",
                                                )
                                            ]
                                        ),
                                        ft.Column(
                                            controls=[
                                                ft.Text(
                                                    "Saldo:",
                                                    weight="bold",
                                                    color="white"
                                                ),
                                                ft.Text(
                                                    value=f"R${saldo_:.2f}",
                                                    color="white",
                                                )
                                            ]
                                        ),
                                        ft.Container(expand=True),
                                        ft.IconButton(
                                            icon=ft.Icons.EDIT,
                                            icon_color="green",
                                            on_click=open_dlg_modal
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE,
                                            icon_color="RED",
                                            on_click=delete_pessoa
                                        )
                                    ]
                                )
                            )
                        ]
                    )
                    main_pesquisar.controls.append(att_pesquisas)
                    page.update()

            if filtros.value == "Maior 18 anos":
                cursor.execute("""SELECT id,titular,saldo,idade FROM contas_bancarias
                        WHERE idade > 18""")
                contas = cursor.fetchall()

                for id, titular, saldo_, idade_ in contas:
                    
                    def editar(e):
                        cursor.execute("""UPDATE contas_bancarias
                                    SET titular = ?, saldo = ?, idade = ?
                                    WHERE id = ?""",(nome.value,saldo.value,idade.value,id))
                        close_dlg(e)
                        pesquisar_filtros(e)
                        snackbar_ = ft.SnackBar(ft.Text(f"Titular: {titular} editado com sucesso!"),bgcolor="green",duration=2000)
                        page.overlay.append(snackbar_)
                        snackbar_.open = True
                        conexao.commit()
                        page.update()

                    def close_dlg(e):
                        dlg_modal.open = False
                        e.control.page.update()

                    def open_dlg_modal(e):
                        e.control.page.overlay.append(dlg_modal)
                        dlg_modal.open = True
                        e.control.page.update()


                    dlg_modal = ft.AlertDialog(
                        bgcolor="#1C303A",
                        actions_padding=10,
                        modal=True,
                        title=ft.Text("Editando Conta",color="white"),
                        content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    nome,
                                saldo,
                                idade,
                                ft.Container(
                                    height=50,
                                    alignment=ft.alignment.center,
                                    border_radius=10,
                                    bgcolor="#6E93A5",
                                    content=ft.Text(
                                        "Editar",
                                        color="white",
                                        weight="bold"
                                    ),
                                    ink=True,
                                    on_click=editar
                                ),
                                ft.Container(
                                    height=50,
                                    alignment=ft.alignment.center,
                                    border_radius=10,
                                    bgcolor="RED",
                                    content=ft.Text(
                                        "Cancelar",
                                        color="white",
                                        weight="bold"
                                    ),
                                    ink=True,
                                    on_click=close_dlg
                                )
                            ]
                        ),
                        actions_alignment=ft.MainAxisAlignment.END,
                        on_dismiss=lambda e: print("Modal dialog dismissed!"),
                    )

                    def delete_pessoa(e):
                        cursor.execute(f"""DELETE FROM contas_bancarias
                                    WHERE id = ?""",(id,))
                        conexao.commit()
                        conexao.close()
                        main_pesquisar.controls.controls.pop(-1)
                        snackbar = ft.SnackBar(ft.Text(f"Titular: {titular} removido com sucesso!"),bgcolor="green",duration=2000)
                        page.overlay.append(snackbar)
                        snackbar.open = True
                        page.update()

                    att_pesquisas = ft.ResponsiveRow(
                        controls=[
                            ft.Container(
                                col={"xs":12,"sm":6,"md":6,"lg":6},
                                height=100,
                                border_radius=10,
                                bgcolor="#6E93A5",
                                padding=20,
                                alignment=ft.alignment.center,
                                content=ft.Row(
                                    spacing=30,
                                    controls=[
                                        ft.Column(
                                            controls=[
                                                ft.Text(
                                                    "Nome:",
                                                    weight="bold",
                                                    color="white"
                                                ),
                                                ft.Text(
                                                    value=titular,
                                                    color="white",
                                                )
                                            ]
                                        ),
                                        ft.Column(
                                            controls=[
                                                ft.Text(
                                                    "Saldo:",
                                                    weight="bold",
                                                    color="white"
                                                ),
                                                ft.Text(
                                                    value=f"R${saldo_:.2f}",
                                                    color="white",
                                                )
                                            ]
                                        ),
                                        ft.Container(expand=True),
                                        ft.IconButton(
                                            icon=ft.Icons.EDIT,
                                            icon_color="green",
                                            on_click=open_dlg_modal
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE,
                                            icon_color="RED",
                                            on_click=delete_pessoa
                                        )
                                    ]
                                )
                            )
                        ]
                    )
                    main_pesquisar.controls.append(att_pesquisas)
                    page.update()
            
            if filtros.value == "Menos de R$1.000,00":
                cursor.execute("""SELECT id,titular,saldo,idade FROM contas_bancarias
                        WHERE saldo < 1000""")
                contas = cursor.fetchall()

                for id, titular, saldo_, idade_ in contas:
                    
                    def editar(e):
                        cursor.execute("""UPDATE contas_bancarias
                                    SET titular = ?, saldo = ?, idade = ?
                                    WHERE id = ?""",(nome.value,saldo.value,idade.value,id))
                        close_dlg(e)
                        pesquisar_filtros(e)
                        snackbar_ = ft.SnackBar(ft.Text(f"Titular: {titular} editado com sucesso!"),bgcolor="green",duration=2000)
                        page.overlay.append(snackbar_)
                        snackbar_.open = True
                        conexao.commit()
                        page.update()

                    def close_dlg(e):
                        dlg_modal.open = False
                        e.control.page.update()

                    def open_dlg_modal(e):
                        e.control.page.overlay.append(dlg_modal)
                        dlg_modal.open = True
                        e.control.page.update()


                    dlg_modal = ft.AlertDialog(
                        bgcolor="#1C303A",
                        actions_padding=10,
                        modal=True,
                        title=ft.Text("Editando Conta",color="white"),
                        content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    nome,
                                saldo,
                                idade,
                                ft.Container(
                                    height=50,
                                    alignment=ft.alignment.center,
                                    border_radius=10,
                                    bgcolor="#6E93A5",
                                    content=ft.Text(
                                        "Editar",
                                        color="white",
                                        weight="bold"
                                    ),
                                    ink=True,
                                    on_click=editar
                                ),
                                ft.Container(
                                    height=50,
                                    alignment=ft.alignment.center,
                                    border_radius=10,
                                    bgcolor="RED",
                                    content=ft.Text(
                                        "Cancelar",
                                        color="white",
                                        weight="bold"
                                    ),
                                    ink=True,
                                    on_click=close_dlg
                                )
                            ]
                        ),
                        actions_alignment=ft.MainAxisAlignment.END,
                        on_dismiss=lambda e: print("Modal dialog dismissed!"),
                    )

                    def delete_pessoa(e):
                        cursor.execute(f"""DELETE FROM contas_bancarias
                                    WHERE id = ?""",(id,))
                        conexao.commit()
                        conexao.close()
                        main_pesquisar.controls.controls.pop(-1)
                        snackbar = ft.SnackBar(ft.Text(f"Titular: {titular} removido com sucesso!"),bgcolor="green",duration=2000)
                        page.overlay.append(snackbar)
                        snackbar.open = True
                        page.update()

                    att_pesquisas = ft.ResponsiveRow(
                        controls=[
                            ft.Container(
                                col={"xs":12,"sm":6,"md":6,"lg":6},
                                height=100,
                                border_radius=10,
                                bgcolor="#6E93A5",
                                padding=20,
                                alignment=ft.alignment.center,
                                content=ft.Row(
                                    spacing=30,
                                    controls=[
                                        ft.Column(
                                            controls=[
                                                ft.Text(
                                                    "Nome:",
                                                    weight="bold",
                                                    color="white"
                                                ),
                                                ft.Text(
                                                    value=titular,
                                                    color="white",
                                                )
                                            ]
                                        ),
                                        ft.Column(
                                            controls=[
                                                ft.Text(
                                                    "Saldo:",
                                                    weight="bold",
                                                    color="white"
                                                ),
                                                ft.Text(
                                                    value=f"R${saldo_:.2f}",
                                                    color="white",
                                                )
                                            ]
                                        ),
                                        ft.Container(expand=True),
                                        ft.IconButton(
                                            icon=ft.Icons.EDIT,
                                            icon_color="green",
                                            on_click=open_dlg_modal
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE,
                                            icon_color="RED",
                                            on_click=delete_pessoa
                                        )
                                    ]
                                )
                            )
                        ]
                    )
                    main_pesquisar.controls.append(att_pesquisas)
                    page.update()

            if filtros.value == "Mais de R$1.000,00":
                cursor.execute("""SELECT id,titular,saldo,idade FROM contas_bancarias
                        WHERE saldo > 1000""")
                contas = cursor.fetchall()

                for id, titular, saldo_, idade_ in contas:
                    
                    def editar(e):
                        cursor.execute("""UPDATE contas_bancarias
                                    SET titular = ?, saldo = ?, idade = ?
                                    WHERE id = ?""",(nome.value,saldo.value,idade.value,id))
                        close_dlg(e)
                        pesquisar_filtros(e)
                        snackbar_ = ft.SnackBar(ft.Text(f"Titular: {titular} editado com sucesso!"),bgcolor="green",duration=2000)
                        page.overlay.append(snackbar_)
                        snackbar_.open = True
                        conexao.commit()
                        page.update()

                    def close_dlg(e):
                        dlg_modal.open = False
                        e.control.page.update()

                    def open_dlg_modal(e):
                        e.control.page.overlay.append(dlg_modal)
                        dlg_modal.open = True
                        e.control.page.update()


                    dlg_modal = ft.AlertDialog(
                        bgcolor="#1C303A",
                        actions_padding=10,
                        modal=True,
                        title=ft.Text("Editando Conta",color="white"),
                        content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    nome,
                                saldo,
                                idade,
                                ft.Container(
                                    height=50,
                                    alignment=ft.alignment.center,
                                    border_radius=10,
                                    bgcolor="#6E93A5",
                                    content=ft.Text(
                                        "Editar",
                                        color="white",
                                        weight="bold"
                                    ),
                                    ink=True,
                                    on_click=editar
                                ),
                                ft.Container(
                                    height=50,
                                    alignment=ft.alignment.center,
                                    border_radius=10,
                                    bgcolor="RED",
                                    content=ft.Text(
                                        "Cancelar",
                                        color="white",
                                        weight="bold"
                                    ),
                                    ink=True,
                                    on_click=close_dlg
                                )
                            ]
                        ),
                        actions_alignment=ft.MainAxisAlignment.END,
                        on_dismiss=lambda e: print("Modal dialog dismissed!"),
                    )

                    def delete_pessoa(e):
                        cursor.execute(f"""DELETE FROM contas_bancarias
                                    WHERE id = ?""",(id,))
                        conexao.commit()
                        conexao.close()
                        main_pesquisar.controls.controls.pop(-1)
                        snackbar = ft.SnackBar(ft.Text(f"Titular: {titular} removido com sucesso!"),bgcolor="green",duration=2000)
                        page.overlay.append(snackbar)
                        snackbar.open = True
                        page.update()

                    att_pesquisas = ft.ResponsiveRow(
                        controls=[
                            ft.Container(
                                col={"xs":12,"sm":6,"md":6,"lg":6},
                                height=100,
                                border_radius=10,
                                bgcolor="#6E93A5",
                                padding=20,
                                alignment=ft.alignment.center,
                                content=ft.Row(
                                    spacing=30,
                                    controls=[
                                        ft.Column(
                                            controls=[
                                                ft.Text(
                                                    "Nome:",
                                                    weight="bold",
                                                    color="white"
                                                ),
                                                ft.Text(
                                                    value=titular,
                                                    color="white",
                                                )
                                            ]
                                        ),
                                        ft.Column(
                                            controls=[
                                                ft.Text(
                                                    "Saldo:",
                                                    weight="bold",
                                                    color="white"
                                                ),
                                                ft.Text(
                                                    value=f"R${saldo_:.2f}",
                                                    color="white",
                                                )
                                            ]
                                        ),
                                        ft.Container(expand=True),
                                        ft.IconButton(
                                            icon=ft.Icons.EDIT,
                                            icon_color="green",
                                            on_click=open_dlg_modal
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE,
                                            icon_color="RED",
                                            on_click=delete_pessoa
                                        )
                                    ]
                                )
                            )
                        ]
                    )
                    main_pesquisar.controls.append(att_pesquisas)
                    page.update()
            
            if filtros.value == "Todos":
                cursor.execute("""SELECT id,titular,saldo,idade FROM contas_bancarias""")
                contas = cursor.fetchall()

                for id, titular, saldo_, idade_ in contas:
                    
                    def editar(e):
                        cursor.execute("""UPDATE contas_bancarias
                                    SET titular = ?, saldo = ?, idade = ?
                                    WHERE id = ?""",(nome.value,saldo.value,idade.value,id))
                        close_dlg(e)
                        pesquisar_filtros(e)
                        snackbar_ = ft.SnackBar(ft.Text(f"Titular: {titular} editado com sucesso!"),bgcolor="green",duration=2000)
                        page.overlay.append(snackbar_)
                        snackbar_.open = True
                        conexao.commit()
                        page.update()

                    def close_dlg(e):
                        dlg_modal.open = False
                        e.control.page.update()

                    def open_dlg_modal(e):
                        e.control.page.overlay.append(dlg_modal)
                        dlg_modal.open = True
                        e.control.page.update()


                    dlg_modal = ft.AlertDialog(
                        bgcolor="#1C303A",
                        actions_padding=10,
                        modal=True,
                        title=ft.Text("Editando Conta",color="white"),
                        content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    nome,
                                saldo,
                                idade,
                                ft.Container(
                                    height=50,
                                    alignment=ft.alignment.center,
                                    border_radius=10,
                                    bgcolor="#6E93A5",
                                    content=ft.Text(
                                        "Editar",
                                        color="white",
                                        weight="bold"
                                    ),
                                    ink=True,
                                    on_click=editar
                                ),
                                ft.Container(
                                    height=50,
                                    alignment=ft.alignment.center,
                                    border_radius=10,
                                    bgcolor="RED",
                                    content=ft.Text(
                                        "Cancelar",
                                        color="white",
                                        weight="bold"
                                    ),
                                    ink=True,
                                    on_click=close_dlg
                                )
                            ]
                        ),
                        actions_alignment=ft.MainAxisAlignment.END,
                        on_dismiss=lambda e: print("Modal dialog dismissed!"),
                    )

                    def delete_pessoa(e):
                        cursor.execute(f"""DELETE FROM contas_bancarias
                                    WHERE id = ?""",(id,))
                        conexao.commit()
                        conexao.close()
                        main_pesquisar.controls.controls.pop(-1)
                        snackbar = ft.SnackBar(ft.Text(f"Titular: {titular} removido com sucesso!"),bgcolor="green",duration=2000)
                        page.overlay.append(snackbar)
                        snackbar.open = True
                        page.update()

                    att_pesquisas = ft.ResponsiveRow(
                        controls=[
                            ft.Container(
                                col={"xs":12,"sm":6,"md":6,"lg":6},
                                height=100,
                                border_radius=10,
                                bgcolor="#6E93A5",
                                padding=20,
                                alignment=ft.alignment.center,
                                content=ft.Row(
                                    spacing=30,
                                    controls=[
                                        ft.Column(
                                            controls=[
                                                ft.Text(
                                                    "Nome:",
                                                    weight="bold",
                                                    color="white"
                                                ),
                                                ft.Text(
                                                    value=titular,
                                                    color="white",
                                                )
                                            ]
                                        ),
                                        ft.Column(
                                            controls=[
                                                ft.Text(
                                                    "Saldo:",
                                                    weight="bold",
                                                    color="white"
                                                ),
                                                ft.Text(
                                                    value=f"R${saldo_:.2f}",
                                                    color="white",
                                                )
                                            ]
                                        ),
                                        ft.Container(expand=True),
                                        ft.IconButton(
                                            icon=ft.Icons.EDIT,
                                            icon_color="green",
                                            on_click=open_dlg_modal
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE,
                                            icon_color="RED",
                                            on_click=delete_pessoa
                                        )
                                    ]
                                )
                            )
                        ]
                    )
                    main_pesquisar.controls.append(att_pesquisas)
                    page.update()

        main_cont.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(
                            name="SEARCH",
                            color="white",
                            size=30
                        ),
                        ft.Text(
                            "Pesquisas e Filtros",
                            color="white",
                            weight="bold",
                            size=30
                        )
                    ]
                ),
                ft.Container(
                    height=50,
                    border=ft.border.all(width=1,color="white"),
                    border_radius=10,
                    padding=10,
                    content=ft.Row(
                        controls=[
                            ft.Icon(
                                "SEARCH",
                                color="white"
                            ),
                            pesquisar_pessoas
                        ]
                    )
                ),
                filtros := ft.Dropdown(
                    hint_text="Escolha um filtro",
                    hint_style=ft.TextStyle(color="white"),
                    fill_color="white",
                    border_color="white",
                    options=[
                        ft.dropdown.Option(
                            "Todos"
                        ),
                        ft.dropdown.Option(
                            "Menor de 18 anos"
                        ),
                        ft.dropdown.Option(
                            "Maior 18 anos"
                        ),
                        ft.dropdown.Option(
                            "Menos de R$1.000,00"
                        ),
                        ft.dropdown.Option(
                            "Mais de R$1.000,00"
                        )
                    ],
                    on_change=changes_filtros
                ),
                ft.Container(
                    height=50,
                    alignment=ft.alignment.center,
                    border_radius=10,
                    bgcolor="#6E93A5",
                    content=ft.Icon(
                        "SEARCH",
                        color="white"
                    ),
                    on_click=pesquisar_filtros,
                    ink=True
                ),
                main_pesquisar
            ]
        )
        page.update()

    def parse_valor_brasileiro(valor_str):
        valor_str = valor_str.replace("R$", "").replace(" ", "")  # remove R$
        valor_str = valor_str.replace(".", "")  # remove pontos de milhar
        valor_str = valor_str.replace(",", ".")  # troca vírgula decimal por ponto
        
        try:
            return float(valor_str)
        except:
            return 0.0

    def cadastrar(e):
        saldo_num = parse_valor_brasileiro(saldo.value)
        
        cursor.execute("""
            INSERT INTO contas_bancarias (titular, saldo, idade)
            VALUES (?, ?, ?)
        """, (nome.value, saldo_num, idade.value))
        
        conexao.commit()
        snackbar = ft.SnackBar(ft.Text(f"Titular: {nome.value} Cadastrado com sucesso!"),bgcolor="green",duration=2000)
        page.overlay.append(snackbar)
        snackbar.open = True
        home(e)


    def atualizar_dados():
        cursor.execute("""SELECT * FROM contas_bancarias""")
        pessoas = cursor.fetchall()
        total_pessoas.value = len(pessoas)
        for pessoa in pessoas:
            id,nome,saldo,idade= pessoa
        cursor.execute("""SELECT idade FROM contas_bancarias
                       WHERE idade < 18 """)
        idade_ = cursor.fetchall()
        menores.value = len(idade_)
        cursor.execute("SELECT SUM(saldo) FROM contas_bancarias")
        total = cursor.fetchone()[0] or 0

        saldo_total.value = f"R$ {total:.2f}".replace(".", ",")


    def home(e):
        atualizar_dados()
        main_cont.clean()
        bar_bottom.visible = True
        floating_buttom.visible = True
        home_btn.content.controls[0].color = "#6E93A5"
        pesquisar_btn.content.controls[0].color = "white"
        main_cont.content = ft.Column(
            horizontal_alignment="center",
            controls=[
                ft.Icon(
                    name="HOME",
                    size=50,
                    color="white"
                ),
                ft.ResponsiveRow(
                    controls=[
                        ft.Container(
                            col=12,
                            height=150,
                            padding=10,
                            border_radius=20,
                            bgcolor="#1C303A",
                            content=ft.Column(
                                spacing=20,
                                controls=[
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                        controls=[
                                            ft.Icon(
                                                name=ft.Icons.PERSON,
                                                color="white"
                                            ),
                                            ft.Text(
                                                "Pessoas cadastradas:",
                                                color="white",
                                            ),
                                            ft.Icon(
                                                name=ft.Icons.ARROW_DROP_DOWN,
                                                color="white"
                                            )
                                        ]
                                    ),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                        controls=[
                                            ft.Container(
                                                expand=True,
                                            ),
                                            total_pessoas,
                                            ft.Container(
                                                expand=True,
                                            ),
                                        ]
                                    )
                                ]
                            )
                        ),
                        ft.Container(
                            col={"xs":12,"sm":6,"md":6,"lg":6},
                            height=80,
                            bgcolor="#6E93A5",
                            border_radius=20,
                            padding=10,
                            content=ft.Column(
                                horizontal_alignment="center",
                                spacing=10,
                                controls=[
                                    ft.Text(
                                        "Valor total de Dinheiro",
                                        color="white",
                                    ),
                                    saldo_total
                                ]
                            )
                        ),
                        ft.Container(
                            col={"xs":12,"sm":6,"md":6,"lg":6},
                            height=80,
                            bgcolor="#6E93A5",
                            padding=10,
                            border_radius=20,
                            content=ft.Column(
                                horizontal_alignment="center",
                                spacing=10,
                                controls=[
                                    ft.Text(
                                        "Menores de 18 anos",
                                        color="white",
                                    ),
                                    menores
                                ]
                            )
                        ),
                    ]
                )
            ]
        )
        page.update()


    floating_buttom = ft.FloatingActionButton(
        content=ft.Icon(
            name="ADD",
            color="white"
        ),
        bgcolor="#1C303A",
        on_click=adicionar
    )

    bar_bottom = ft.BottomAppBar(
        bgcolor="#1C303A",
        padding=20,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                home_btn:=ft.Container(
                    content=ft.Column(
                        horizontal_alignment="center",
                        spacing=0,
                        controls=[
                            ft.Icon(
                                name=ft.Icons.HOME,
                                color="white"
                            ),
                            ft.Text(
                                "Home",
                                color="white",
                                text_align=ft.TextAlign.CENTER
                            )
                        ]
                    ),
                    on_click=home,
                    ink=True
                ),
                pesquisar_btn:=ft.Container(
                    content=ft.Column(
                        horizontal_alignment="center",
                        spacing=0,
                        controls=[
                            ft.Icon(
                                name=ft.Icons.SEARCH,
                                color="white"
                            ),
                            ft.Text(
                                "Pesquisar",
                                color="white",
                                text_align=ft.TextAlign.CENTER
                            )
                        ]
                    ),
                    on_click=pesquisar,
                    ink=True
                ),
            ]
        )
    )

    home_btn.content.controls[0].color = "#6E93A5"
    pesquisar_btn.content.controls[0].color = "white"
    main_cont = ft.Container(
        expand=True,
        content = ft.Column(
            horizontal_alignment="center",
            controls=[
                ft.Icon(
                    name="HOME",
                    size=50,
                    color="white"
                ),
                ft.ResponsiveRow(
                    controls=[
                        ft.Container(
                            col=12,
                            height=150,
                            padding=10,
                            border_radius=20,
                            bgcolor="#1C303A",
                            content=ft.Column(
                                spacing=20,
                                controls=[
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                        controls=[
                                            ft.Icon(
                                                name=ft.Icons.PERSON,
                                                color="white"
                                            ),
                                            ft.Text(
                                                "Pessoas cadastradas:",
                                                color="white",
                                            ),
                                            ft.Icon(
                                                name=ft.Icons.ARROW_DROP_DOWN,
                                                color="white"
                                            )
                                        ]
                                    ),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                        controls=[
                                            ft.Container(
                                                expand=True,
                                            ),
                                            total_pessoas,
                                            ft.Container(
                                                expand=True
                                            )
                                        ]
                                    )
                                ]
                            )
                        ),
                        ft.Container(
                            col={"xs":12,"sm":6,"md":6,"lg":6},
                            height=80,
                            bgcolor="#6E93A5",
                            border_radius=20,
                            padding=10,
                            content=ft.Column(
                                horizontal_alignment="center",
                                spacing=10,
                                controls=[
                                    ft.Text(
                                        "Valor total de Dinheiro",
                                        color="white",
                                    ),
                                    saldo_total
                                ]
                            )
                        ),
                        ft.Container(
                            col={"xs":12,"sm":6,"md":6,"lg":6},
                            height=80,
                            bgcolor="#6E93A5",
                            padding=10,
                            border_radius=20,
                            content=ft.Column(
                                horizontal_alignment="center",
                                spacing=10,
                                controls=[
                                    ft.Text(
                                        "Menores de 18 anos",
                                        color="white",
                                    ),
                                    menores
                                ]
                            )
                        ),
                    ]
                )
            ]
        )
    )

    atualizar_dados()
    page.update()

    page.add(
        main_cont,
        bar_bottom,
        floating_buttom
    )

if __name__ == "__main__":
    ft.app(target=main)