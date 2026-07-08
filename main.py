import flet as ft
import requests
import threading
import json
import sqlite3
import socket
import os
import time
import webbrowser
from datetime import date, datetime

# ─────────────────────────────────────────────
# CONFIG & DB
# ─────────────────────────────────────────────
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwWwH57yGAGEu-79p12898wCLPO2WGDER44Otm9cV6P1sugL25__4uyHDZ4kIU2Tv7x/exec"
SESSION_FILE = "session.json"
DB_FILE = "sms_local.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS attendance_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course TEXT NOT NULL,
        date TEXT NOT NULL,
        synced INTEGER DEFAULT 0,
        created_at TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS attendance_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER,
        student_id TEXT,
        student_name TEXT,
        status TEXT,
        FOREIGN KEY (session_id) REFERENCES attendance_sessions(id)
    )''')
    conn.commit()
    conn.close()

def save_session(data):
    with open(SESSION_FILE, "w") as f:
        json.dump(data, f)

def get_session():
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r") as f:
                return json.load(f)
        except:
            return None
    return None

def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

def check_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

init_db()

# ─────────────────────────────────────────────
# THEME TOKENS (Navy + Gold)
# ─────────────────────────────────────────────
BG_DEEP     = "#0A0E1A"
BG_CARD     = "#141828"
BG_INPUT    = "#0A0E1A"
ACCENT      = "#F5C842"
ACCENT_DARK = "#C9A227"
BLUE        = "#4A90D9"
BLUE_DARK   = "#2C5F8A"
TEXT_MAIN   = "#F0F4FF"
TEXT_MUTED  = "#8899BB"
TEXT_DIM    = "#445577"
BORDER      = "#FFFFFF0D"
BORDER_GOLD = "#F5C84233"
SUCCESS     = "#4ADE80"
ERROR_C     = "#F87171"
WARNING_C   = "#FACC15"

# ─────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────
STUDENTS_LIST = [
    {"id": "BAI-23S-001", "name": "Tilha Ayub"},
    {"id": "BAI-24S-024", "name": "Priya Maheshwari"},
    {"id": "BAI-24F-011", "name": "Kelash Menghwar"},
    {"id": "BAI-24F-603", "name": "Waqar Nohari"},
    {"id": "BAI-24F-604", "name": "Hamza Ali"},
    {"id": "BAI-24F-608", "name": "Mangha Ram"},
    {"id": "BAI-24F-609", "name": "Muhammad Owais"},
    {"id": "BAI-24F-612", "name": "Hadia Hakim"},
    {"id": "BAI-24F-617", "name": "Hammad Ul Hasnain"},
    {"id": "BAI-24F-623", "name": "Yousuf Hasan Khan"},
    {"id": "BAI-24F-625", "name": "Hamid Ali"},
    {"id": "BAI-24F-631", "name": "Farzain Ahmed"},
    {"id": "BAI-24F-632", "name": "Muhammad Saad Chohan"},
    {"id": "BAI-24F-633", "name": "Masharib Ali"},
    {"id": "BAI-24F-634", "name": "Muhammad Saqib"},
    {"id": "BAI-24F-636", "name": "Muhammad Owais Ansari"},
    {"id": "BAI-24F-637", "name": "Waseem Ahmed"},
    {"id": "BAI-24F-640", "name": "Muhammad Ismail"},
    {"id": "BAI-24F-641", "name": "Sherjeel Ahmed"},
    {"id": "BAI-24F-642", "name": "Zeeshan Mirza"},
    {"id": "BAI-24F-643", "name": "Muhammad Owais Waqar"},
    {"id": "BAI-24F-644", "name": "Uzaifa Zulfiqar"},
    {"id": "BAI-24F-645", "name": "Harman Ali Khan"},
    {"id": "BAI-24F-646", "name": "Abdul Rehman"},
    {"id": "BAI-24F-647", "name": "Najeeb Ullah"},
    {"id": "BAI-24F-648", "name": "Aakash Kumar"},
    {"id": "BAI-24F-649", "name": "Muhammad Taha"},
    {"id": "BAI-24F-651", "name": "Syed Arqum Hussain"},
    {"id": "BAI-24F-652", "name": "Eraj Sohail"},
    {"id": "BAI-24F-653", "name": "Manish Veljee"},
    {"id": "BAI-24F-655", "name": "Shahzaib Awan"},
    {"id": "BAI-24F-657", "name": "Disha Rani"},
    {"id": "BAI-24F-662", "name": "Aiman Atif"},
    {"id": "BAI-24F-663", "name": "Muhammad Sabeeh Imtiaz"},
    {"id": "BAI-24F-664", "name": "Muhammad Moeed"},
    {"id": "BAI-24F-666", "name": "Ayaz Ali"},
    {"id": "BAI-24F-667", "name": "Muhammad Shoaib Mughal"},
    {"id": "BAI-24F-668", "name": "Urwa Khan"},
    {"id": "BAI-24S-009", "name": "Muhammad Yaseen"},
]

COURSES = [
    ("ANN", "ANN & Deep Learning"),
    ("ANN-LAB", "ANN & Deep Learning - Lab"),
    ("ABM", "Agent Based Modelling"),
    ("ABM-LAB", "ABM - Lab"),
    ("OS", "Operating System"),
    ("OS-LAB", "OS - Lab"),
    ("KRR", "Knowledge Rep. & Reasoning"),
    ("ToA", "Theory of Automata"),
    ("ITM", "Intro to Management"),
]

ADMIN_COURSES = [
    ("ANN", "ANN & Deep Learning"),
    ("ABM", "Agent Based Modelling"),
    ("OS", "Operating System"),
    ("KRR", "Knowledge Rep. & Reasoning"),
    ("ToA", "Theory of Automata"),
    ("ITM", "Intro to Management"),
]

LAB_MAP = {
    "ANN": ("ANN_LAB", "ANN Lab"),
    "ABM": ("ABM_LAB", "ABM Lab"),
    "OS":  ("OS_LAB", "OS Lab"),
}

CALENDAR_EVENTS = [
    ("Commencement of Classes", "Mon, 9th Feb 2026", "Sun, 7th Jun 2026", SUCCESS),
    ("Mid-Term Examinations", "Mon, 6th Apr 2026", "Sun, 12th Apr 2026", WARNING_C),
    ("Final Term Examinations", "Mon, 8th Jun 2026", "Sun, 14th Jun 2026", ERROR_C),
]

# ─────────────────────────────────────────────
# SHARED UI HELPERS
# ─────────────────────────────────────────────

def custom_divider():
    return ft.Container(height=1, bgcolor=BORDER, margin=ft.Margin.symmetric(vertical=6, horizontal=0))

def section_title(text: str):
    return ft.Text(
        text.upper(), size=15,
        weight=ft.FontWeight.BOLD,
        color=TEXT_MUTED, font_family="monospace",
    )

def make_textfield(hint: str, password=False, ref=None, keyboard_type=None, label=None, value=None, read_only=False):
    return ft.TextField(
        hint_text=hint,
        password=password,
        can_reveal_password=password,
        ref=ref,
        keyboard_type=keyboard_type,
        label=label,
        label_style=ft.TextStyle(color=TEXT_MUTED, size=11) if label else None,
        value=value,
        bgcolor=BG_INPUT,
        border_color=BORDER_GOLD,
        focused_border_color=ACCENT,
        color=TEXT_MAIN,
        hint_style=ft.TextStyle(color=TEXT_DIM),
        border_radius=10,
        content_padding=ft.Padding.symmetric(horizontal=14, vertical=12),
        text_style=ft.TextStyle(size=13, color=TEXT_MAIN),
        read_only=read_only
    )

def make_dropdown(hint: str, options_list, ref=None, on_select=None, expand=False):
    return ft.Dropdown(
        ref=ref,
        hint_text=hint,
        bgcolor=BG_INPUT,
        border_color=BORDER_GOLD,
        focused_border_color=ACCENT,
        color=TEXT_MAIN,
        hint_style=ft.TextStyle(color=TEXT_DIM),
        border_radius=10,
        options=[ft.dropdown.Option(k, v) for k, v in options_list],
        content_padding=ft.Padding.symmetric(horizontal=14, vertical=10),
        text_style=ft.TextStyle(size=12, color=TEXT_MAIN),
        on_select=on_select,
        expand=expand,
    )

class ScaleButton(ft.Container):
    def __init__(self, text: str, on_click=None, icon=None, expand=False, width=None, bgcolor=ACCENT_DARK, color=TEXT_MAIN, padding=None):
        row_items = []
        if icon:
            row_items.append(ft.Icon(icon, size=15, color=color))
        row_items.append(
            ft.Text(text.upper(), size=12, weight=ft.FontWeight.BOLD, color=color)
        )
        
        if padding is None:
            padding = ft.Padding.symmetric(horizontal=20, vertical=12)
            
        super().__init__(
            content=ft.Row(row_items, alignment=ft.MainAxisAlignment.CENTER, spacing=8),
            bgcolor=bgcolor,
            border_radius=10,
            padding=padding,
            ink=True,
            on_click=self._animate_and_click,
            scale=1.0,
            animate_scale=ft.Animation(100, ft.AnimationCurve.EASE_OUT),
            expand=expand,
            width=width,
            alignment=ft.Alignment.CENTER
        )
        self.external_click = on_click

    def _animate_and_click(self, e):
        self.scale = 0.95
        self.update()
        time.sleep(0.1)
        self.scale = 1.0
        self.update()
        if self.external_click:
            self.external_click(e)

def glass_card(content, padding=16, border_top_color=None):
    if border_top_color:
        border = ft.Border.only(
            top=ft.BorderSide(3, border_top_color),
            left=ft.BorderSide(1, BORDER_GOLD),
            right=ft.BorderSide(1, BORDER_GOLD),
            bottom=ft.BorderSide(1, BORDER_GOLD),
        )
    else:
        border = ft.Border.all(1, BORDER_GOLD)
    return ft.Container(
        content=content,
        bgcolor=BG_CARD,
        border_radius=16,
        border=border,
        padding=padding,
        animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT)
    )

def status_pill(text: str, color: str):
    return ft.Container(
        content=ft.Text(
            text.upper(), size=9,
            weight=ft.FontWeight.BOLD, color=color,
        ),
        bgcolor=color + "22",
        border=ft.Border.all(1, color + "55"),
        border_radius=6,
        padding=ft.Padding.symmetric(horizontal=8, vertical=3),
    )

def spinner_row(message="Loading...", ref=None):
    return ft.Row(
        [
            ft.ProgressRing(color=ACCENT, width=20, height=20, stroke_width=2),
            ft.Text(message, color=ACCENT, size=12, weight=ft.FontWeight.BOLD),
        ],
        ref=ref,
        visible=False,
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER,
    )

class ShimmerCard(ft.Container):
    def __init__(self, height=60, width=None, expand=False):
        super().__init__(
            bgcolor=BORDER_GOLD,
            border_radius=12,
            height=height, width=width, expand=expand,
            opacity=0.4,
            animate_opacity=ft.Animation(600, ft.AnimationCurve.EASE_IN_OUT)
        )
        self.running = True

    def did_mount(self):
        def animate_shimmer():
            while self.running and getattr(self, "page", None):
                self.opacity = 0.8 if self.opacity == 0.4 else 0.4
                try:
                    self.update()
                    time.sleep(0.6)
                except:
                    break
        threading.Thread(target=animate_shimmer, daemon=True).start()

    def will_unmount(self):
        self.running = False

# ─────────────────────────────────────────────
# ROLE SELECTION
# ─────────────────────────────────────────────

def build_role_selection(on_student, on_admin):
    header = ft.Column(
        [
            ft.Row(
                [
                    ft.Container(
                        content=ft.Icon(ft.Icons.HEXAGON, color=BG_DEEP, size=24),
                        width=50, height=50,
                        bgcolor=ACCENT,
                        border_radius=14,
                        alignment=ft.Alignment.CENTER,
                    ),
                    ft.Column(
                        [
                            ft.Text("POWERED BY", size=9, color=ACCENT_DARK,
                                    weight=ft.FontWeight.BOLD, font_family="monospace"),
                            ft.Text("HEXALABS", size=24, color=TEXT_MAIN,
                                    weight=ft.FontWeight.BOLD, font_family="monospace"),
                        ],
                        spacing=0,
                    ),
                ],
                spacing=14,
            ),
            ft.Container(height=10),
            ft.Text("SMS PORTAL", size=38, weight=ft.FontWeight.BOLD,
                    color=TEXT_MAIN, font_family="monospace"),
            ft.Text("SPRING 2026", size=16, weight=ft.FontWeight.BOLD,
                    color=ACCENT, font_family="monospace"),
            ft.Container(height=6),
            ft.Container(
                content=ft.Text(
                    "Centralized academic management for BS Artificial Intelligence",
                    size=12, color=TEXT_MUTED,
                ),
                border=ft.Border.only(left=ft.BorderSide(3, ACCENT)),
                padding=ft.Padding.only(left=12, top=4, bottom=4, right=0),
            ),
        ],
        spacing=4,
    )

    student_card = ft.Container(
        content=ft.Row(
            [
                ft.Column(
                    [
                        ft.Text("Student Portal", size=20, weight=ft.FontWeight.BOLD,
                                color=TEXT_MAIN, font_family="monospace"),
                        ft.Text("Access Dashboard & Attendance", size=12, color=TEXT_MUTED),
                    ],
                    expand=True, spacing=4,
                ),
                ft.Container(
                    content=ft.Icon(ft.Icons.ARROW_FORWARD, color=BG_DEEP, size=18),
                    width=42, height=42,
                    bgcolor=ACCENT,
                    border_radius=21,
                    alignment=ft.Alignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor=BG_CARD,
        border=ft.Border.all(2, BORDER_GOLD),
        border_radius=16,
        padding=ft.Padding.symmetric(horizontal=20, vertical=20),
        ink=True,
        on_click=on_student,
    )

    admin_card = ft.Container(
        content=ft.Row(
            [
                ft.Column(
                    [
                        ft.Text("Admin Console", size=16, weight=ft.FontWeight.BOLD,
                                color=TEXT_MUTED, font_family="monospace"),
                        ft.Text("RESTRICTED ACCESS", size=10, color=TEXT_DIM,
                                font_family="monospace"),
                    ],
                    expand=True, spacing=4,
                ),
                ft.Icon(ft.Icons.TERMINAL, color=TEXT_DIM, size=20),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor="#0f172acc",
        border=ft.Border.all(1, BORDER),
        border_radius=16,
        padding=ft.Padding.symmetric(horizontal=20, vertical=16),
        ink=True,
        on_click=on_admin,
    )

    return ft.Container(
        content=ft.Column(
            [
                ft.Container(height=30),
                header,
                ft.Container(height=36),
                student_card,
                ft.Container(height=14),
                admin_card,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            spacing=0,
        ),
        expand=True,
        bgcolor=BG_DEEP,
        padding=ft.Padding.symmetric(horizontal=24, vertical=0),
    )

# ─────────────────────────────────────────────
# STUDENT LOGIN PAGE
# ─────────────────────────────────────────────
def build_student_login(on_login, on_back):
    roll_ref     = ft.Ref[ft.TextField]()
    password_ref = ft.Ref[ft.TextField]()
    error_ref    = ft.Ref[ft.Text]()

    def handle_login(e):
        roll = (roll_ref.current.value or "").strip().upper()
        pwd = (password_ref.current.value or "")
        
        found = False
        name = ""
        for s in STUDENTS_LIST:
            if s["id"] == roll:
                found = True
                name = s["name"]
                break
                
        if found and pwd == f"@BAI{roll[-3:]}":
            error_ref.current.visible = False
            error_ref.current.update()
            save_session({"role": "student", "roll": roll, "name": name})
            on_login(e)
        else:
            error_ref.current.visible = True
            
            # Simple shake animation effect
            error_ref.current.offset = ft.Offset(0.05, 0)
            error_ref.current.update()
            time.sleep(0.05)
            error_ref.current.offset = ft.Offset(-0.05, 0)
            error_ref.current.update()
            time.sleep(0.05)
            error_ref.current.offset = ft.Offset(0, 0)
            error_ref.current.update()

    form = ft.Column(
        [
            ft.Text(
                "STUDENT LOGIN", size=24,
                weight=ft.FontWeight.BOLD, color=ACCENT,
                font_family="monospace",
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(
                width=60, height=3,
                bgcolor=ACCENT, border_radius=2,
                alignment=ft.Alignment.CENTER,
            ),
            ft.Container(height=8),
            make_textfield("Roll Number (e.g. BAI-24F-617)", ref=roll_ref),
            ft.Container(height=8),
            make_textfield("Password", password=True, ref=password_ref),
            ft.Container(height=4),
            ft.Text(
                "⚠  INVALID CREDENTIALS",
                ref=error_ref,
                color=ERROR_C, size=12,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
                visible=False,
                animate_offset=ft.Animation(50, ft.AnimationCurve.BOUNCE_OUT)
            ),
            ft.Container(height=8),
            ScaleButton("LOGIN", on_click=handle_login,
                       icon=ft.Icons.LOGIN, expand=True, bgcolor=ACCENT, color=BG_DEEP),
        ],
        spacing=6,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
    )

    return ft.Container(
        content=ft.Column(
            [
                ft.Container(height=20),
                ft.IconButton(
                    ft.Icons.ARROW_BACK_IOS,
                    icon_color=TEXT_MUTED,
                    on_click=on_back,
                ),
                ft.Container(height=16),
                glass_card(
                    ft.Container(content=form, padding=8),
                    padding=24,
                    border_top_color=ACCENT,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            spacing=0,
        ),
        expand=True,
        bgcolor=BG_DEEP,
        padding=ft.Padding.symmetric(horizontal=24, vertical=0),
    )


# ─────────────────────────────────────────────
# ADMIN LOGIN PAGE
# ─────────────────────────────────────────────

def build_admin_login(on_login, on_back):
    username_ref = ft.Ref[ft.TextField]()
    password_ref = ft.Ref[ft.TextField]()
    error_ref    = ft.Ref[ft.Text]()

    def handle_login(e):
        u = (username_ref.current.value or "").strip().upper()
        p = (password_ref.current.value or "")
        if u == "SA" and p == "123":
            error_ref.current.visible = False
            error_ref.current.update()
            save_session({"role": "admin"})
            on_login(e)
        else:
            error_ref.current.visible = True
            error_ref.current.update()

    form = ft.Column(
        [
            ft.Text(
                "ADMIN CONSOLE", size=24,
                weight=ft.FontWeight.BOLD, color=ACCENT,
                font_family="monospace",
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(
                width=60, height=3,
                bgcolor=ACCENT, border_radius=2,
                alignment=ft.Alignment.CENTER,
            ),
            ft.Container(height=8),
            make_textfield("USERNAME", ref=username_ref),
            ft.Container(height=8),
            make_textfield("PASSWORD", password=True, ref=password_ref),
            ft.Container(height=4),
            ft.Text(
                "⚠  ACCESS DENIED",
                ref=error_ref,
                color=ERROR_C, size=12,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
                visible=False,
            ),
            ft.Container(height=8),
            ScaleButton("ACCESS", on_click=handle_login,
                       icon=ft.Icons.LOCK_OPEN, expand=True),
        ],
        spacing=6,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
    )

    return ft.Container(
        content=ft.Column(
            [
                ft.Container(height=20),
                ft.IconButton(
                    ft.Icons.ARROW_BACK_IOS,
                    icon_color=TEXT_MUTED,
                    on_click=on_back,
                ),
                ft.Container(height=16),
                glass_card(
                    ft.Container(content=form, padding=8),
                    padding=24,
                    border_top_color=ERROR_C,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            spacing=0,
        ),
        expand=True,
        bgcolor=BG_DEEP,
        padding=ft.Padding.symmetric(horizontal=24, vertical=0),
    )

# ─────────────────────────────────────────────
# STUDENT DASHBOARD
# ─────────────────────────────────────────────
def build_student_dashboard(page: ft.Page, on_exit, on_calc):
    session_data = get_session() or {}
    s_name = session_data.get("name", "Student")
    s_roll = session_data.get("roll", "BAI-000")

    # 1. HOME TAB COMPONENTS
    overall_val = ft.Text("--%", size=26, color=ACCENT, weight=ft.FontWeight.BOLD, font_family="monospace")
    
    def fetch_overall():
        if check_internet():
            try:
                resp = requests.get(f"{WEB_APP_URL}?action=studentReport&studentId={s_roll}&course=OVERALL", timeout=15).json()
                pct = resp.get("percentage", 0)
                overall_val.value = f"{pct}%"
                overall_val.color = SUCCESS if pct >= 75 else (WARNING_C if pct >= 50 else ERROR_C)
            except:
                overall_val.value = "ERR"
        else:
            overall_val.value = "OFF"
        if getattr(page, 'update', None):
            page.update()

    threading.Thread(target=fetch_overall, daemon=True).start()

    ann_col = ft.Column([ShimmerCard(height=50), ShimmerCard(height=50)], spacing=8)
    
    def fetch_announcements():
        anns = []
        if check_internet():
            try:
                resp = requests.get(f"{WEB_APP_URL}?action=getAnnouncements", timeout=15).json()
                anns = resp.get("announcements", [])
            except:
                pass
        
        if not anns:
            anns = [
                {"title": "Spring 2026", "body": "Spring 2026 semester is in progress. Stay consistent!"},
                {"title": "Mid-terms", "body": "Mid-terms: April 6–12, 2026"},
                {"title": "Finals", "body": "Finals: June 8–14, 2026"}
            ]
            
        ui_items = []
        for a in anns:
            ui_items.append(
                glass_card(
                    ft.Column([
                        ft.Text(a["title"], weight=ft.FontWeight.BOLD, color=ACCENT, size=13),
                        ft.Text(a["body"], color=TEXT_MAIN, size=11)
                    ], spacing=2),
                    padding=12
                )
            )
        ann_col.controls = ui_items
        if getattr(page, 'update', None):
            page.update()

    threading.Thread(target=fetch_announcements, daemon=True).start()

    home_tab = ft.Column([
        ft.Container(
            content=ft.Column([
                ft.Text(f"Welcome back,", size=14, color=TEXT_MUTED),
                ft.Text(s_name, size=22, weight=ft.FontWeight.BOLD, color=TEXT_MAIN),
                status_pill(s_roll, ACCENT)
            ], spacing=2),
            bgcolor=BG_CARD, border_radius=16, border=ft.Border.all(1, BORDER_GOLD),
            padding=20
        ),
        ft.Row([
            ft.Container(
                content=ft.Column([
                    ft.Text("OVERALL ATTENDANCE", size=9, color=TEXT_DIM, font_family="monospace", weight=ft.FontWeight.BOLD),
                    overall_val
                ], spacing=2),
                bgcolor=BG_CARD, border_radius=16, border=ft.Border.all(1, BORDER_GOLD),
                padding=16, expand=True
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("SEMESTER PROGRESS", size=9, color=TEXT_DIM, font_family="monospace", weight=ft.FontWeight.BOLD),
                    ft.Text("Week 4/18", size=18, color=TEXT_MAIN, weight=ft.FontWeight.BOLD, font_family="monospace"),
                    ft.ProgressBar(value=4/18, color=ACCENT, bgcolor=BORDER_GOLD, height=6)
                ], spacing=6),
                bgcolor=BG_CARD, border_radius=16, border=ft.Border.all(1, BORDER_GOLD),
                padding=16, expand=True
            )
        ], spacing=10),
        section_title("Announcements"),
        ann_col,
        section_title("Quick Links"),
        ft.Row([
            ScaleButton("CMS", icon=ft.Icons.WEB, expand=True, on_click=lambda e: webbrowser.open("http://cms.smiu.edu.pk:9991/psp/ps/?cmd=login")),
            ScaleButton("Drive", icon=ft.Icons.FOLDER, expand=True, on_click=lambda e: webbrowser.open("https://drive.google.com/drive/folders/1j6m8OBurmBCiZ9Ll55DQ64Taf-BcNGXF?usp=drive_link")),
            ScaleButton("GPA", icon=ft.Icons.CALCULATE, expand=True, on_click=on_calc),
        ], spacing=10)
    ], spacing=16, scroll=ft.ScrollMode.AUTO, expand=True)

    # 2. ATTENDANCE TAB
    course_ref   = ft.Ref[ft.Dropdown]()
    loader_ref   = ft.Ref[ft.Row]()
    result_ref   = ft.Ref[ft.Column]()
    att_err_ref  = ft.Ref[ft.Text]()
    res_total    = ft.Ref[ft.Text]()
    res_present  = ft.Ref[ft.Text]()
    res_bar      = ft.Ref[ft.Container]()
    res_pct      = ft.Ref[ft.Text]()
    res_details  = ft.Ref[ft.Column]()

    def do_check(e):
        course = course_ref.current.value or ""
        att_err_ref.current.visible = False
        result_ref.current.visible  = False
        
        if not course:
            att_err_ref.current.value   = "Please select a Course."
            att_err_ref.current.visible = True
            page.update()
            return

        loader_ref.current.visible = True
        page.update()

        def fetch():
            try:
                url  = f"{WEB_APP_URL}?action=studentReport&studentId={s_roll}&course={course}"
                resp = requests.get(url, timeout=25)
                data = resp.json()
                if data.get("error"):
                    att_err_ref.current.value   = data["error"]
                    att_err_ref.current.visible = True
                else:
                    total   = data.get("total",      0)
                    present = data.get("present",    0)
                    pct     = data.get("percentage", 0)

                    res_total.current.value   = str(total)
                    res_present.current.value = str(present)
                    res_pct.current.value     = f"{pct}%"

                    bar_color = SUCCESS if pct >= 75 else (WARNING_C if pct >= 50 else ERROR_C)
                    res_bar.current.bgcolor = bar_color
                    res_bar.current.width   = max(4, int((pct / 100) * 300))
                    res_pct.current.color   = bar_color

                    detail_rows = []
                    for d in reversed(data.get("details", [])):
                        clr = SUCCESS if d.get("status") == "Present" else ERROR_C
                        detail_rows.append(
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Text(d.get("date", ""), size=11, color=TEXT_MUTED, font_family="monospace", expand=True),
                                        status_pill(d.get("status", ""), clr),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                bgcolor="#1e293b", border=ft.Border.all(1, BORDER), border_radius=8,
                                padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                            )
                        )
                    if not detail_rows:
                        detail_rows.append(ft.Text("No session records found.", size=11, color=TEXT_DIM))
                    res_details.current.controls = detail_rows
                    result_ref.current.visible   = True
            except Exception as ex:
                att_err_ref.current.value   = f"Connection failed. Try again."
                att_err_ref.current.visible = True
            finally:
                loader_ref.current.visible = False
                page.update()

        threading.Thread(target=fetch, daemon=True).start()

    result_panel = ft.Column(
        [
            ft.Row([
                ft.Text("Total Classes:", size=12, color=TEXT_MUTED, expand=True),
                ft.Text("0", ref=res_total, size=16, weight=ft.FontWeight.BOLD, color=TEXT_MAIN, font_family="monospace"),
            ]),
            ft.Row([
                ft.Text("Attended:", size=12, color=TEXT_MUTED, expand=True),
                ft.Text("0", ref=res_present, size=16, weight=ft.FontWeight.BOLD, color=TEXT_MAIN, font_family="monospace"),
            ]),
            custom_divider(),
            ft.Text("ATTENDANCE %", size=9, color=TEXT_DIM, font_family="monospace", weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Stack([
                    ft.Container(bgcolor=BG_INPUT, border_radius=8, expand=True),
                    ft.Container(ref=res_bar, bgcolor=SUCCESS, border_radius=8, height=14, width=0, animate=ft.Animation(800, ft.AnimationCurve.EASE_OUT)),
                ]),
                height=14, border_radius=8, border=ft.Border.all(1, BORDER), clip_behavior=ft.ClipBehavior.HARD_EDGE,
            ),
            ft.Text("0%", ref=res_pct, size=20, weight=ft.FontWeight.BOLD, color=SUCCESS, font_family="monospace", text_align=ft.TextAlign.RIGHT),
            custom_divider(),
            ft.Text("SESSION DETAILS", size=9, color=TEXT_DIM, font_family="monospace", weight=ft.FontWeight.BOLD),
            ft.Column(ref=res_details, spacing=6, scroll=ft.ScrollMode.AUTO, height=200),
        ],
        ref=result_ref, visible=False, spacing=8,
    )

    attendance_tab = ft.Column([
        section_title("Check Attendance"),
        glass_card(
            ft.Column([
                make_textfield("Roll No", value=s_roll, read_only=True),
                ft.Container(height=8),
                make_dropdown("Select Module...", COURSES, ref=course_ref),
                ft.Container(height=10),
                ScaleButton("CHECK", on_click=do_check, icon=ft.Icons.SEARCH, expand=True),
                ft.Container(height=8),
                spinner_row("Fetching data...", ref=loader_ref),
                ft.Text("", ref=att_err_ref, color=ERROR_C, size=12, weight=ft.FontWeight.BOLD, visible=False),
                result_panel,
            ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)
        )
    ], spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)

    # 3. SCHEDULE TAB
    def cal_row(event, start, end, color):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(event, size=13, weight=ft.FontWeight.BOLD, color=color),
                    ft.Row(
                        [
                            ft.Column([
                                ft.Text("START", size=9, color=TEXT_DIM, font_family="monospace"),
                                ft.Text(start, size=11, color=TEXT_MAIN, weight=ft.FontWeight.BOLD),
                            ], spacing=2),
                            ft.VerticalDivider(color=BORDER_GOLD, width=1),
                            ft.Column([
                                ft.Text("END", size=9, color=TEXT_DIM, font_family="monospace"),
                                ft.Text(end, size=11, color=TEXT_MAIN, weight=ft.FontWeight.BOLD),
                            ], spacing=2),
                        ], spacing=16
                    ),
                ], spacing=8
            ),
            bgcolor=color + "15", border=ft.Border.all(1, color + "44"), border_radius=12, padding=14,
        )

    schedule_tab = ft.Column([
        section_title("Academic Calendar"),
        ft.Column([cal_row(*ev) for ev in CALENDAR_EVENTS], spacing=10),
        ft.Container(height=10),
        section_title("Weekly Timeline"),
        glass_card(
            ft.Text("Timetable will be updated soon.", size=13, color=TEXT_MUTED, text_align=ft.TextAlign.CENTER),
            padding=ft.Padding.symmetric(vertical=40, horizontal=20)
        )
    ], spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)

    # 4. SETTINGS TAB
    def do_logout(e):
        clear_session()
        on_exit(e)

    settings_tab = ft.Column([
        section_title("Account Settings"),
        glass_card(ft.Column([
            ft.Text(s_name, size=18, weight=ft.FontWeight.BOLD, color=TEXT_MAIN),
            ft.Text(s_roll, size=12, color=TEXT_MUTED, font_family="monospace")
        ])),
        ft.Container(height=10),
        glass_card(ft.Column([
            ft.Row([ft.Icon(ft.Icons.LOCK, color=ACCENT, size=18), ft.Text("Change Password", color=TEXT_MAIN, weight=ft.FontWeight.BOLD)], spacing=10),
            ft.Text("To change your password, please contact the class admin.", size=11, color=TEXT_MUTED)
        ])),
        ft.Container(height=20),
        ScaleButton("LOGOUT", on_click=do_logout, icon=ft.Icons.LOGOUT, bgcolor=ERROR_C, expand=True)
    ], spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)

    # Main Tab Controller
    tabs = {
        "home": home_tab,
        "attendance": attendance_tab,
        "schedule": schedule_tab,
        "settings": settings_tab
    }
    
    for k, v in tabs.items():
        v.visible = False
    tabs["home"].visible = True

    content_area = ft.Container(content=ft.Column(list(tabs.values()), expand=True), expand=True)

    def switch_tab(tab_name):
        for k, v in tabs.items():
            v.visible = (k == tab_name)
        page.update()

    def bottom_nav_item(icon, label, target_tab):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, size=24, color=TEXT_MAIN),
                ft.Text(label, size=10, color=TEXT_MAIN, weight=ft.FontWeight.BOLD)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=2),
            expand=True, ink=True,
            on_click=lambda e: switch_tab(target_tab),
            padding=ft.Padding.symmetric(vertical=8, horizontal=0)
        )

    bottom_nav = ft.Container(
        content=ft.Row([
            bottom_nav_item(ft.Icons.HOME, "Home", "home"),
            bottom_nav_item(ft.Icons.PIE_CHART, "Attendance", "attendance"),
            bottom_nav_item(ft.Icons.CALENDAR_MONTH, "Schedule", "schedule"),
            bottom_nav_item(ft.Icons.SETTINGS, "Settings", "settings"),
        ]),
        bgcolor=BG_CARD, border=ft.Border.only(top=ft.BorderSide(1, BORDER_GOLD)),
        padding=ft.Padding.symmetric(vertical=4, horizontal=8)
    )

    top_bar = ft.Container(
        content=ft.Row(
            [
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.GRID_VIEW, color=BG_DEEP, size=16),
                        width=36, height=36, bgcolor=ACCENT, border_radius=10, alignment=ft.Alignment.CENTER,
                    ),
                    ft.Text("SMS-AI5B", size=16, weight=ft.FontWeight.BOLD, color=TEXT_MAIN, font_family="monospace"),
                ], spacing=10, expand=True),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor=BG_DEEP, border=ft.Border.only(bottom=ft.BorderSide(1, BORDER_GOLD)),
        padding=ft.Padding.symmetric(horizontal=16, vertical=10),
    )

    return ft.Container(
        content=ft.Column(
            [
                top_bar,
                ft.Container(content=content_area, expand=True, padding=ft.Padding.symmetric(horizontal=16, vertical=12)),
                bottom_nav
            ],
            spacing=0, expand=True,
        ),
        expand=True, bgcolor=BG_DEEP,
    )

# ─────────────────────────────────────────────
# GPA CALCULATOR PLACEHOLDER
# ─────────────────────────────────────────────
def build_gpa_calculator(on_back):
    return ft.Container(
        content=ft.Column([
            ft.Container(height=20),
            ft.IconButton(ft.Icons.ARROW_BACK_IOS, icon_color=TEXT_MUTED, on_click=on_back),
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.CALCULATE, size=60, color=ACCENT),
                    ft.Text("GPA Calculator", size=24, weight=ft.FontWeight.BOLD, color=TEXT_MAIN),
                    ft.Text("Coming Soon!", size=14, color=TEXT_MUTED)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.Alignment.CENTER, expand=True
            )
        ]),
        expand=True, bgcolor=BG_DEEP, padding=ft.Padding.symmetric(horizontal=24, vertical=0)
    )

# ─────────────────────────────────────────────
# ADMIN DASHBOARD
# ─────────────────────────────────────────────

def build_admin_dashboard(page: ft.Page, on_exit):
    
    # 1. MARK ATTENDANCE TAB
    current_students = [dict(s) for s in STUDENTS_LIST]
    checkboxes: dict = {}

    roster_ref  = ft.Ref[ft.Column]()
    success_ref = ft.Ref[ft.Text]()
    mark_err    = ft.Ref[ft.Text]()
    sync_spin   = ft.Ref[ft.Row]()
    course_ref  = ft.Ref[ft.Dropdown]()
    lab_ref     = ft.Ref[ft.Dropdown]()
    date_ref    = ft.Ref[ft.TextField]()

    def rebuild_roster():
        checkboxes.clear()
        rows = []
        for s in current_students:
            cb = ft.Checkbox(value=False, active_color=ACCENT, check_color=BG_DEEP)
            checkboxes[s["id"]] = cb
            rows.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(s["id"], size=10, color=ACCENT, font_family="monospace", weight=ft.FontWeight.BOLD),
                                    ft.Text(s["name"], size=12, color=TEXT_MAIN, weight=ft.FontWeight.BOLD),
                                ],
                                expand=True, spacing=2,
                            ),
                            cb,
                            ft.IconButton(
                                ft.Icons.DELETE_OUTLINE, icon_color=TEXT_DIM, icon_size=18,
                                on_click=lambda e, sid=s["id"]: exclude_student(sid),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    bgcolor=BG_DEEP, border=ft.Border.only(bottom=ft.BorderSide(1, BORDER)),
                    padding=ft.Padding.symmetric(horizontal=14, vertical=10),
                )
            )
        roster_ref.current.controls = rows
        if getattr(page, 'update', None): page.update()

    def exclude_student(sid):
        nonlocal current_students
        current_students = [s for s in current_students if s["id"] != sid]
        if sid in checkboxes: del checkboxes[sid]
        rebuild_roster()

    def select_all(e):
        for cb in checkboxes.values(): cb.value = True
        page.update()

    def deselect_all(e):
        for cb in checkboxes.values(): cb.value = False
        page.update()

    def on_course_select(e):
        sel = course_ref.current.value or ""
        opts = [ft.dropdown.Option("", "No Lab")]
        if sel in LAB_MAP:
            val, label = LAB_MAP[sel]
            opts.append(ft.dropdown.Option(val, label))
        lab_ref.current.options = opts
        lab_ref.current.value   = ""
        lab_ref.current.update()

    def show_snackbar(text, is_error=False):
        # A simple visual feedback inside the tab
        if is_error:
            mark_err.current.value = text
            mark_err.current.visible = True
            success_ref.current.visible = False
        else:
            success_ref.current.value = text
            success_ref.current.visible = True
            mark_err.current.visible = False
        page.update()

    def handle_admin_sync(e):
        success_ref.current.visible = False
        mark_err.current.visible    = False

        base_c = course_ref.current.value or ""
        if not base_c:
            show_snackbar("Please select a course first!", True)
            return

        lab_val  = lab_ref.current.value or ""
        course = lab_val if lab_val else base_c
        att_date = date_ref.current.value or str(date.today())

        records = []
        for s in current_students:
            cb = checkboxes.get(s["id"])
            if cb is not None:
                records.append({
                    "studentId":   s["id"],
                    "studentName": s["name"],
                    "status":      "Present" if cb.value else "Absent",
                })

        if not records:
            show_snackbar("Roster is empty!", True)
            return

        # 1. Save to SQLite
        try:
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute("INSERT INTO attendance_sessions (course, date, created_at) VALUES (?, ?, ?)", 
                      (course, att_date, str(datetime.now())))
            session_id = c.lastrowid
            
            for r in records:
                c.execute("INSERT INTO attendance_records (session_id, student_id, student_name, status) VALUES (?, ?, ?, ?)",
                          (session_id, r["studentId"], r["studentName"], r["status"]))
            conn.commit()
            conn.close()
        except Exception as ex:
            show_snackbar("Failed to save locally.", True)
            return

        sync_spin.current.visible = True
        page.update()

        # 2. Sync to GAS
        def do_sync():
            if not check_internet():
                show_snackbar("Saved offline. No internet.", True)
                sync_spin.current.visible = False
                page.update()
                return
            
            try:
                # Duplicate Check
                dup_res = requests.get(f"{WEB_APP_URL}?action=checkDuplicate&course={course}&date={att_date}", timeout=15).json()
                if dup_res.get("exists"):
                    show_snackbar("Saved offline. Duplicate found on server.", True)
                    sync_spin.current.visible = False
                    page.update()
                    return

                # Upload
                payload = {"course": course, "date": att_date, "records": records}
                resp = requests.post(WEB_APP_URL, json=payload, timeout=25).json()
                
                if resp.get("result") == "success":
                    # Mark Synced
                    conn = sqlite3.connect(DB_FILE)
                    c = conn.cursor()
                    c.execute("UPDATE attendance_sessions SET synced=1 WHERE id=?", (session_id,))
                    conn.commit()
                    conn.close()
                    show_snackbar("✓ Saved and synced successfully!")
                    deselect_all(None)
                else:
                    show_snackbar(f"Saved offline. Server error: {resp.get('message')}", True)
            except:
                show_snackbar("Saved offline. Network error during sync.", True)
            finally:
                sync_spin.current.visible = False
                page.update()
                
        threading.Thread(target=do_sync, daemon=True).start()

    mark_tab = ft.Column(
        [
            glass_card(
                ft.Column([
                    make_dropdown("Select Course", ADMIN_COURSES, ref=course_ref, on_select=on_course_select),
                    ft.Container(height=8),
                    ft.Dropdown(
                        ref=lab_ref, hint_text="Select Lab (Optional)", bgcolor=BG_INPUT, border_color=BORDER_GOLD, focused_border_color=ACCENT,
                        color=TEXT_MAIN, hint_style=ft.TextStyle(color=TEXT_DIM), border_radius=10, options=[ft.dropdown.Option("", "No Lab")],
                        content_padding=ft.Padding.symmetric(horizontal=14, vertical=10), text_style=ft.TextStyle(size=12, color=TEXT_MAIN),
                    ),
                    ft.Container(height=8),
                    make_textfield("YYYY-MM-DD", ref=date_ref, label="Attendance Date", value=str(date.today())),
                ], spacing=0)
            ),
            ft.Container(height=10),
            ft.Row([
                ft.Text("STUDENT ROSTER", size=13, weight=ft.FontWeight.BOLD, color=TEXT_MAIN, font_family="monospace", expand=True),
                ScaleButton("ALL", on_click=select_all, bgcolor=ACCENT+"1a", color=ACCENT, padding=ft.Padding.symmetric(horizontal=12, vertical=6)),
                ft.Container(width=6),
                ScaleButton("CLEAR", on_click=deselect_all, bgcolor=BORDER, color=TEXT_DIM, padding=ft.Padding.symmetric(horizontal=12, vertical=6)),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(
                content=ft.Column(ref=roster_ref, spacing=0, scroll=ft.ScrollMode.AUTO),
                bgcolor=BG_CARD, border=ft.Border.all(1, BORDER_GOLD), border_radius=12, height=300, clip_behavior=ft.ClipBehavior.HARD_EDGE,
            ),
            ft.Container(height=10),
            ScaleButton("SYNC TO SHEETS", on_click=handle_admin_sync, icon=ft.Icons.CLOUD_UPLOAD, expand=True, bgcolor=ACCENT, color=BG_DEEP),
            spinner_row("Syncing...", ref=sync_spin),
            ft.Text("", ref=success_ref, color=SUCCESS, size=12, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, visible=False),
            ft.Text("", ref=mark_err, color=ERROR_C, size=12, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, visible=False),
        ], spacing=6, scroll=ft.ScrollMode.AUTO, expand=True
    )

    # 2. ANALYTICS TAB
    rep_course  = ft.Ref[ft.Dropdown]()
    rep_spin    = ft.Ref[ft.Row]()
    rep_err     = ft.Ref[ft.Text]()
    rep_content = ft.Ref[ft.Column]()
    rep_total   = ft.Ref[ft.Text]()
    rep_tbody   = ft.Ref[ft.Column]()

    def fetch_report(e):
        course = rep_course.current.value or ""
        rep_err.current.visible     = False
        rep_content.current.visible = False

        if not course:
            rep_err.current.value   = "Please select a module."
            rep_err.current.visible = True
            page.update()
            return

        rep_spin.current.visible = True
        page.update()

        def do_fetch():
            try:
                url  = f"{WEB_APP_URL}?action=classReport&course={course}"
                resp = requests.get(url, timeout=25)
                data = resp.json()
                if data.get("error"):
                    rep_err.current.value   = data["error"]
                    rep_err.current.visible = True
                else:
                    rep_total.current.value = str(data.get("totalClasses", 0))
                    rows = []
                    for s in data.get("report", []):
                        pct = s.get("percentage", 0)
                        clr = SUCCESS if pct >= 75 else (WARNING_C if pct >= 50 else ERROR_C)
                        rows.append(
                            ft.Container(
                                content=ft.Row([
                                    ft.Column([
                                        ft.Text(s.get("id", ""), size=9, color=ACCENT, font_family="monospace"),
                                        ft.Text(s.get("name", ""), size=12, color=TEXT_MAIN, weight=ft.FontWeight.BOLD),
                                    ], expand=True, spacing=2),
                                    ft.Column([
                                        ft.Text(f"{s.get('present',0)}/{s.get('total',0)}", size=11, color=TEXT_MUTED, font_family="monospace", text_align=ft.TextAlign.RIGHT),
                                        ft.Text(f"{pct}%", size=14, weight=ft.FontWeight.BOLD, color=clr, font_family="monospace", text_align=ft.TextAlign.RIGHT),
                                    ], horizontal_alignment=ft.CrossAxisAlignment.END, spacing=2),
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                bgcolor=BG_DEEP, border=ft.Border.only(bottom=ft.BorderSide(1, BORDER)),
                                padding=ft.Padding.symmetric(horizontal=14, vertical=10),
                            )
                        )
                    rep_tbody.current.controls = rows
                    rep_content.current.visible = True
            except Exception as ex:
                rep_err.current.value   = f"Failed to connect."
                rep_err.current.visible = True
            finally:
                rep_spin.current.visible = False
                page.update()

        threading.Thread(target=do_fetch, daemon=True).start()

    analytics_tab = ft.Column([
        glass_card(ft.Column([
            make_dropdown("Select Module...", COURSES, ref=rep_course),
            ft.Container(height=10),
            ScaleButton("GENERATE REPORT", on_click=fetch_report, icon=ft.Icons.BAR_CHART, expand=True)
        ], spacing=0)),
        ft.Container(height=10),
        spinner_row("Analyzing data...", ref=rep_spin),
        ft.Text("", ref=rep_err, color=ERROR_C, size=12, weight=ft.FontWeight.BOLD, visible=False),
        ft.Column([
            ft.Container(
                content=ft.Row([
                    ft.Text("TOTAL SESSIONS HELD", size=10, color=TEXT_MUTED, font_family="monospace", weight=ft.FontWeight.BOLD, expand=True),
                    ft.Text("0", ref=rep_total, size=22, weight=ft.FontWeight.BOLD, color=ACCENT, font_family="monospace"),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                bgcolor=BG_CARD, border=ft.Border.all(1, BORDER_GOLD), border_radius=12, padding=ft.Padding.symmetric(horizontal=16, vertical=12),
            ),
            ft.Container(
                content=ft.Column(ref=rep_tbody, spacing=0, scroll=ft.ScrollMode.AUTO),
                bgcolor=BG_CARD, border=ft.Border.all(1, BORDER_GOLD), border_radius=12, height=350, clip_behavior=ft.ClipBehavior.HARD_EDGE,
            ),
        ], ref=rep_content, visible=False, spacing=10, scroll=ft.ScrollMode.AUTO),
    ], spacing=6, scroll=ft.ScrollMode.AUTO, expand=True)

    # 3. LOCAL DB TAB
    db_list_ref = ft.Ref[ft.Column]()
    db_spin = ft.Ref[ft.Row]()
    
    def fetch_db():
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT id, course, date, synced FROM attendance_sessions ORDER BY id DESC")
        rows = c.fetchall()
        
        ui_rows = []
        for r in rows:
            sid, crs, dt, sync = r
            icon = ft.Icons.CHECK_CIRCLE if sync else ft.Icons.PENDING
            color = SUCCESS if sync else WARNING_C
            
            ui_rows.append(
                ft.Container(
                    content=ft.Row([
                        ft.Column([
                            ft.Text(crs, size=13, color=TEXT_MAIN, weight=ft.FontWeight.BOLD),
                            ft.Text(dt, size=11, color=TEXT_MUTED, font_family="monospace")
                        ], expand=True),
                        ft.Icon(icon, color=color, size=20),
                        ft.IconButton(ft.Icons.DELETE, icon_color=ERROR_C, on_click=lambda e, del_id=sid: delete_record(del_id))
                    ]),
                    bgcolor=BG_CARD, border=ft.Border.all(1, BORDER_GOLD), border_radius=8,
                    padding=ft.Padding.symmetric(horizontal=12, vertical=8)
                )
            )
        db_list_ref.current.controls = ui_rows
        conn.close()
        if getattr(page, 'update', None): page.update()

    def delete_record(sid):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("DELETE FROM attendance_records WHERE session_id=?", (sid,))
        c.execute("DELETE FROM attendance_sessions WHERE id=?", (sid,))
        conn.commit()
        conn.close()
        fetch_db()

    def sync_pending(e):
        db_spin.current.visible = True
        page.update()
        
        def background_sync():
            if not check_internet():
                db_spin.current.visible = False
                page.update()
                return
                
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute("SELECT id, course, date FROM attendance_sessions WHERE synced=0")
            pending = c.fetchall()
            
            for sid, crs, dt in pending:
                c.execute("SELECT student_id, student_name, status FROM attendance_records WHERE session_id=?", (sid,))
                recs = c.fetchall()
                records = [{"studentId": r[0], "studentName": r[1], "status": r[2]} for r in recs]
                
                try:
                    dup_res = requests.get(f"{WEB_APP_URL}?action=checkDuplicate&course={crs}&date={dt}", timeout=15).json()
                    if dup_res.get("exists"):
                        c.execute("UPDATE attendance_sessions SET synced=1 WHERE id=?", (sid,))
                        conn.commit()
                        continue
                    
                    payload = {"course": crs, "date": dt, "records": records}
                    resp = requests.post(WEB_APP_URL, json=payload, timeout=25).json()
                    if resp.get("result") == "success":
                        c.execute("UPDATE attendance_sessions SET synced=1 WHERE id=?", (sid,))
                        conn.commit()
                except:
                    pass
            
            conn.close()
            db_spin.current.visible = False
            fetch_db()

        threading.Thread(target=background_sync, daemon=True).start()

    local_db_tab = ft.Column([
        section_title("Offline Records"),
        ScaleButton("SYNC PENDING", on_click=sync_pending, icon=ft.Icons.SYNC, expand=True),
        spinner_row("Syncing all pending...", ref=db_spin),
        ft.Container(height=10),
        ft.Column(ref=db_list_ref, spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)
    ], expand=True)

    # Controller
    tabs = {"mark": mark_tab, "analytics": analytics_tab, "localdb": local_db_tab}
    for k, v in tabs.items(): v.visible = False
    tabs["mark"].visible = True

    content_area = ft.Container(content=ft.Column(list(tabs.values()), expand=True), expand=True)

    def switch_tab(tab_name):
        for k, v in tabs.items():
            v.visible = (k == tab_name)
        if tab_name == "localdb":
            fetch_db()
        page.update()

    def bottom_nav_item(icon, label, target_tab):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, size=24, color=TEXT_MAIN),
                ft.Text(label, size=10, color=TEXT_MAIN, weight=ft.FontWeight.BOLD)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=2),
            expand=True, ink=True,
            on_click=lambda e: switch_tab(target_tab),
            padding=ft.Padding.symmetric(vertical=8, horizontal=0)
        )

    bottom_nav = ft.Container(
        content=ft.Row([
            bottom_nav_item(ft.Icons.EDIT_DOCUMENT, "Mark", "mark"),
            bottom_nav_item(ft.Icons.ANALYTICS, "Analytics", "analytics"),
            bottom_nav_item(ft.Icons.STORAGE, "Local DB", "localdb"),
        ]),
        bgcolor=BG_CARD, border=ft.Border.only(top=ft.BorderSide(1, BORDER_GOLD)),
        padding=ft.Padding.symmetric(vertical=4, horizontal=8)
    )

    top_bar = ft.Container(
        content=ft.Row([
            ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.ADMIN_PANEL_SETTINGS, color=BG_DEEP, size=16),
                    width=36, height=36, bgcolor=ACCENT, border_radius=10, alignment=ft.Alignment.CENTER,
                ),
                ft.Text("ADMIN PORTAL", size=15, weight=ft.FontWeight.BOLD, color=ACCENT, font_family="monospace"),
            ], spacing=10, expand=True),
            ScaleButton("EXIT", on_click=lambda e: (clear_session(), on_exit(e)), bgcolor=ERROR_C+"1a", color=ERROR_C)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        bgcolor=BG_DEEP, border=ft.Border.only(bottom=ft.BorderSide(1, BORDER_GOLD)),
        padding=ft.Padding.symmetric(horizontal=16, vertical=10),
    )

    # Auto Sync on load
    threading.Thread(target=lambda: sync_pending(None), daemon=True).start()

    return ft.Container(
        content=ft.Column([
            top_bar,
            ft.Container(content=content_area, expand=True, padding=ft.Padding.symmetric(horizontal=16, vertical=12)),
            bottom_nav
        ], spacing=0, expand=True),
        expand=True, bgcolor=BG_DEEP, data=rebuild_roster,
    )


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main(page: ft.Page):
    page.title      = "SMS Portal | BS-AI"
    page.bgcolor    = BG_DEEP
    page.theme_mode = ft.ThemeMode.DARK
    page.padding    = 0

    def view_pop(e):
        if len(page.views) > 1:
            page.views.pop()
            page.update()

    page.on_view_pop = view_pop

    def add_view(route, widget):
        page.views.append(
            ft.View(
                route=route,
                controls=[ft.SafeArea(content=widget, expand=True)],
                bgcolor=BG_DEEP,
                padding=0
            )
        )
        page.update()
        if hasattr(widget, "data") and callable(widget.data):
            widget.data()

    def go_role():
        page.views.clear()
        add_view("/", build_role_selection(
            on_student=lambda e: go_student_login(),
            on_admin=lambda e: go_admin_login(),
        ))

    def go_student_login():
        add_view("/student_login", build_student_login(
            on_login=lambda e: go_student_dashboard(),
            on_back=lambda e: view_pop(None),
        ))

    def go_admin_login():
        add_view("/admin_login", build_admin_login(
            on_login=lambda e: go_admin_dashboard(),
            on_back=lambda e: view_pop(None),
        ))

    def go_student_dashboard():
        page.views.clear()
        add_view("/student", build_student_dashboard(
            page=page,
            on_exit=lambda e: go_role(),
            on_calc=lambda e: go_gpa_calc()
        ))

    def go_admin_dashboard():
        page.views.clear()
        add_view("/admin", build_admin_dashboard(
            page=page,
            on_exit=lambda e: go_role(),
        ))

    def go_gpa_calc():
        add_view("/gpa", build_gpa_calculator(on_back=lambda e: view_pop(None)))

    # Initial Routing Logic
    session = get_session()
    if session:
        if session.get("role") == "admin":
            go_admin_dashboard()
        elif session.get("role") == "student":
            go_student_dashboard()
        else:
            go_role()
    else:
        go_role()

ft.run(main)
