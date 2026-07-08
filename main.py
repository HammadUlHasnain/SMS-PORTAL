import flet as ft
import requests

WEB_APP_URL = 'https://script.google.com/macros/s/AKfycbzUbPZwZgL4W1TWdD02iPyZdcgKI-O6QojaKPrVABILIp-O4bBc7cdlDM6tCdxQVXwi/exec'

def main(page: ft.Page):
    page.title = "ERP Manager App"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 400
    page.window.height = 700

    # State variables
    manager_data = {"id": None, "department": None}

    # UI Components
    username_field = ft.TextField(label="Username", autofocus=True)
    password_field = ft.TextField(label="Password", password=True, can_reveal_password=True)
    login_error = ft.Text(color=ft.colors.RED, visible=False)
    
    sales_list = ft.ListView(expand=1, spacing=10, padding=20)
    progress_ring = ft.ProgressRing(visible=False)

    def show_snack(msg, color):
        page.overlay.append(ft.SnackBar(ft.Text(msg), bgcolor=color, open=True))
        page.update()

    def fetch_pending_sales():
        sales_list.controls.clear()
        progress_ring.visible = True
        page.update()

        try:
            payload = {"action": "get_pending", "department": manager_data["department"]}
            res = requests.post(WEB_APP_URL, json=payload)
            
            if res.status_code == 200:
                data = res.json()
                if not data:
                    sales_list.controls.append(ft.Text("No pending sales for your department.", size=16))
                
                for sale in data:
                    sales_list.controls.append(
                        ft.Card(
                            content=ft.Container(
                                padding=15,
                                content=ft.Column([
                                    ft.Text(f"Sale ID: {sale['SaleID']}", weight=ft.FontWeight.BOLD),
                                    ft.Text(f"Item: {sale['ItemDetails']}"),
                                    ft.Text(f"Amount: Rs {sale['Amount']}", color=ft.colors.GREEN),
                                    ft.ElevatedButton(
                                        "Approve Sale", 
                                        icon=ft.icons.CHECK,
                                        style=ft.ButtonStyle(color=ft.colors.WHITE, bgcolor=ft.colors.GREEN_700),
                                        on_click=lambda e, sid=sale['SaleID']: approve_sale(sid)
                                    )
                                ])
                            )
                        )
                    )
        except Exception as e:
            show_snack("Failed to fetch data. Check internet.", ft.colors.RED)
            
        progress_ring.visible = False
        page.update()

    def approve_sale(sale_id):
        progress_ring.visible = True
        page.update()
        try:
            payload = {"action": "approve", "SaleID": sale_id, "ManagerID": manager_data["id"]}
            res = requests.post(WEB_APP_URL, json=payload)
            if res.status_code == 200:
                show_snack("Sale Approved Successfully!", ft.colors.GREEN)
                fetch_pending_sales() # Refresh the list automatically
        except Exception:
            show_snack("Approval failed.", ft.colors.RED)
        
        progress_ring.visible = False
        page.update()

    def handle_login(e):
        # NOTE: Real scenario me login DB se verify hona chahiye. 
        # Abhi testing ke liye hardcode condition hai based on your dummy data.
        if username_field.value == "boss" and password_field.value == "admin":
            manager_data["id"] = 2  # 'boss' user ID in SQL
            manager_data["department"] = "Hardware"
            
            page.controls.clear()
            page.add(
                ft.SafeArea(
                    ft.Column([
                        ft.Row([
                            ft.Text(f"Welcome, {username_field.value.upper()}", size=24, weight=ft.FontWeight.BOLD),
                            ft.IconButton(icon=ft.icons.REFRESH, on_click=lambda e: fetch_pending_sales())
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Text(f"Dept: {manager_data['department']}", color=ft.colors.GREY),
                        ft.Divider(),
                        progress_ring,
                        sales_list
                    ], expand=True)
                )
            )
            fetch_pending_sales()
        else:
            login_error.value = "Invalid credentials or not a Manager!"
            login_error.visible = True
            page.update()

    # Login View Setup
    page.add(
        ft.SafeArea(
            ft.Container(
                padding=30,
                content=ft.Column([
                    ft.Icon(ft.icons.LOCK_PERSON, size=80, color=ft.colors.BLUE),
                    ft.Text("Manager Login", size=30, weight=ft.FontWeight.BOLD),
                    username_field,
                    password_field,
                    login_error,
                    ft.ElevatedButton("Login", width=200, height=50, on_click=handle_login)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )
        )
    )

ft.app(target=main)
