import flet as ft
import requests
import threading
from datetime import date

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
WEB_APP_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbwWwH57yGAGEu-79p12898wCLPO2WGDER44Otm9cV6P1sugL25__4uyHDZ4kIU2Tv7x/exec"
)

# ─────────────────────────────────────────────
# THEME TOKENS
# ─────────────────────────────────────────────
BG_DEEP     = "#0f172a"
BG_CARD     = "#1e293b"
BG_INPUT    = "#0f172a"
ACCENT      = "#22d3ee"
ACCENT_DARK = "#0891b2"
ACCENT_BLUE = "#1e3a8a"
TEXT_MAIN   = "#f8fafc"
TEXT_MUTED  = "#94a3b8"
TEXT_DIM    = "#64748b"
BORDER      = "#ffffff0d"
BORDER_CYAN = "#22d3ee33"
SUCCESS     = "#4ade80"
ERROR_C     = "#f87171"
WARNING_C   = "#facc15"

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
    ("ANN",     "ANN & Deep Learning"),
    ("ANN-LAB", "ANN & Deep Learning - Lab"),
    ("ABM",     "Agent Based Modelling"),
    ("ABM-LAB", "ABM - Lab"),
    ("OS",      "Operating System"),
    ("OS-LAB",  "OS - Lab"),
    ("KRR",     "Knowledge Rep. & Reasoning"),
    ("ToA",     "Theory of Automata"),
    ("ITM",     "Intro to Management"),
]

ADMIN_COURSES = [
    ("ANN", "ANN & Deep Learning"),
    ("ABM", "Agent Based Modelling"),
    ("OS",  "Operating System"),
    ("KRR", "Knowledge Rep. & Reasoning"),
    ("ToA", "Theory of Automata"),
    ("ITM", "Intro to Management"),
]

LAB_MAP = {
    "ANN": ("ANN_LAB", "ANN Lab"),
    "ABM": ("ABM_LAB", "ABM Lab"),
    "OS":  ("OS_LAB",  "OS Lab"),
}

CALENDAR_EVENTS = [
    ("Commencement of Classes", "Mon, 9th Feb 2026",  "Sun, 7th Jun 2026",  SUCCESS),
    ("Mid-Term Examinations",   "Mon, 6th Apr 2026",  "Sun, 12th Apr 2026", WARNING_C),
    ("Final Term Examinations", "Mon, 8th Jun 2026",  "Sun, 14th Jun 2026", ERROR_C),
]

# ─────────────────────────────────────────────
# SHARED UI HELPERS
# ─────────────────────────────────────────────

def arctic_divider():
    return ft.Container(height=1, bgcolor=BORDER, margin=ft.Margin.symmetric(vertical=6))

def section_title(text: str):
    return ft.Text(
        text.upper(), size=17,
        weight=ft.FontWeight.BOLD,
        color=ACCENT, font_family="monospace",
    )

def make_textfield(hint: str, password=False, ref=None, keyboard_type=None, label=None, value=None):
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
        border_color=BORDER_CYAN,
        focused_border_color=ACCENT,
        color=TEXT_MAIN,
        hint_style=ft.TextStyle(color=TEXT_DIM),
        border_radius=10,
        content_padding=ft.Padding.symmetric(horizontal=14, vertical=12),
        text_style=ft.TextStyle(size=13, color=TEXT_MAIN),
    )

def make_dropdown(hint: str, options_list, ref=None, on_select=None, expand=False):
    return ft.Dropdown(
        ref=ref,
        hint_text=hint,
        bgcolor=BG_INPUT,
        border_color=BORDER_CYAN,
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

def arctic_btn(text: str, on_click=None, icon=None, expand=False, width=None):
    row_items = []
    if icon:
        row_items.append(ft.Icon(icon, size=15, color=TEXT_MAIN))
    row_items.append(
        ft.Text(text.upper(), size=12, weight=ft.FontWeight.BOLD, color=TEXT_MAIN)
    )
    return ft.ElevatedButton(
        content=ft.Row(row_items, alignment=ft.MainAxisAlignment.CENTER, spacing=8),
        on_click=on_click,
        expand=expand,
        width=width,
        bgcolor=ACCENT_DARK,
        color=TEXT_MAIN,
        elevation=4,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.Padding.symmetric(horizontal=20, vertical=12),
        ),
    )

def glass_card(content, padding=16, border_top_color=None):
    if border_top_color:
        border = ft.Border.only(
            top=ft.BorderSide(3, border_top_color),
            left=ft.BorderSide(1, BORDER_CYAN),
            right=ft.BorderSide(1, BORDER_CYAN),
            bottom=ft.BorderSide(1, BORDER_CYAN),
        )
    else:
        border = ft.Border.all(1, BORDER_CYAN)
    return ft.Container(
        content=content,
        bgcolor=BG_CARD,
        border_radius=16,
        border=border,
        padding=padding,
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

# ─────────────────────────────────────────────
# SPLASH SCREEN
# ─────────────────────────────────────────────

def build_splash():
    return ft.Container(
        content=ft.Column(
            [
                ft.ProgressRing(color=ACCENT, width=54, height=54, stroke_width=4),
                ft.Container(height=20),
                ft.Text(
                    "INITIALIZING PORTAL...",
                    size=12, weight=ft.FontWeight.BOLD,
                    color=ACCENT, font_family="monospace",
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        expand=True,
        bgcolor=BG_DEEP,
        alignment=ft.Alignment.CENTER,
    )

# ─────────────────────────────────────────────
# ROLE SELECTION
# ─────────────────────────────────────────────

def build_role_selection(on_student, on_admin):
    header = ft.Column(
        [
            ft.Row(
                [
                    ft.Container(
                        content=ft.Icon(ft.Icons.HEXAGON, color=TEXT_MAIN, size=22),
                        width=50, height=50,
                        bgcolor=ACCENT_DARK,
                        border_radius=14,
                        alignment=ft.Alignment.CENTER,
                    ),
                    ft.Column(
                        [
                            ft.Text("POWERED BY", size=9, color=ACCENT,
                                    weight=ft.FontWeight.BOLD, font_family="monospace"),
                            ft.Text("HEXALABS", size=22, color=TEXT_MAIN,
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
                padding=ft.Padding.only(left=12, top=4, bottom=4),
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
                        ft.Text("View Schedule & Attendance", size=12, color=TEXT_MUTED),
                    ],
                    expand=True, spacing=4,
                ),
                ft.Container(
                    content=ft.Icon(ft.Icons.ARROW_FORWARD, color=TEXT_MAIN, size=18),
                    width=42, height=42,
                    bgcolor=ACCENT_DARK,
                    border_radius=21,
                    alignment=ft.Alignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor=BG_CARD,
        border=ft.Border.all(1, BORDER_CYAN),
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
                ft.Container(height=50),
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
        padding=ft.Padding.symmetric(horizontal=24),
    )

# ─────────────────────────────────────────────
# LOGIN PAGE
# ─────────────────────────────────────────────

def build_login_page(on_login, on_back):
    username_ref = ft.Ref[ft.TextField]()
    password_ref = ft.Ref[ft.TextField]()
    error_ref    = ft.Ref[ft.Text]()

    def handle_login(e):
        u = (username_ref.current.value or "").strip().upper()
        p = (password_ref.current.value or "")
        if u == "SA" and p == "123":
            error_ref.current.visible = False
            error_ref.current.update()
            on_login()
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
            arctic_btn("ACCESS", on_click=handle_login,
                       icon=ft.Icons.LOCK_OPEN, expand=True),
        ],
        spacing=6,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
    )

    return ft.Container(
        content=ft.Column(
            [
                ft.Container(height=48),
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
        padding=ft.Padding.symmetric(horizontal=24),
    )

# ─────────────────────────────────────────────
# STUDENT DASHBOARD
# ─────────────────────────────────────────────

def build_student_dashboard(page: ft.Page, on_exit):
    active_tab = {"val": "calendar"}
    tab_refs   = {}
    sec_refs   = {}

    # ── Calendar ──
    def cal_row(event, start, end, color):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(event, size=13, weight=ft.FontWeight.BOLD, color=color),
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text("START", size=9, color=TEXT_DIM,
                                            font_family="monospace"),
                                    ft.Text(start, size=11, color=TEXT_MAIN,
                                            weight=ft.FontWeight.BOLD),
                                ],
                                spacing=2,
                            ),
                            ft.VerticalDivider(color=BORDER_CYAN, width=1),
                            ft.Column(
                                [
                                    ft.Text("END", size=9, color=TEXT_DIM,
                                            font_family="monospace"),
                                    ft.Text(end, size=11, color=TEXT_MAIN,
                                            weight=ft.FontWeight.BOLD),
                                ],
                                spacing=2,
                            ),
                        ],
                        spacing=16,
                    ),
                ],
                spacing=8,
            ),
            bgcolor=color + "15",
            border=ft.Border.all(1, color + "44"),
            border_radius=12,
            padding=14,
        )

    calendar_sec = ft.Column(
        [section_title("Academic Calendar — Spring 2026")]
        + [cal_row(*ev) for ev in CALENDAR_EVENTS],
        spacing=10,
    )

    # ── Schedule ──
    schedule_sec = ft.Column(
        [
            section_title("Weekly Timeline (5th Sem)"),
            glass_card(
                ft.Text(
                    "Schedule not configured yet.\nAsk your class rep for the timetable.",
                    size=13, color=TEXT_MUTED,
                    text_align=ft.TextAlign.CENTER,
                ),
                padding=ft.Padding.symmetric(vertical=40, horizontal=20),
            ),
        ],
        spacing=10,
    )

    # ── Attendance ──
    roll_ref     = ft.Ref[ft.TextField]()
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
        roll   = (roll_ref.current.value or "").strip().upper()
        course = course_ref.current.value or ""

        att_err_ref.current.visible = False
        result_ref.current.visible  = False
        att_err_ref.current.update()
        result_ref.current.update()

        if not roll or not course:
            att_err_ref.current.value   = "Please enter Roll No and select a Course."
            att_err_ref.current.visible = True
            att_err_ref.current.update()
            return

        loader_ref.current.visible = True
        loader_ref.current.update()

        def fetch():
            try:
                url  = f"{WEB_APP_URL}?action=studentReport&studentId={roll}&course={course}"
                resp = requests.get(url, timeout=15)
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
                    for d in data.get("details", []):
                        clr = SUCCESS if d.get("status") == "Present" else ERROR_C
                        detail_rows.append(
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Text(
                                            d.get("date", ""),
                                            size=11, color=TEXT_MUTED,
                                            font_family="monospace", expand=True,
                                        ),
                                        status_pill(d.get("status", ""), clr),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                bgcolor="#1e293b",
                                border=ft.Border.all(1, BORDER),
                                border_radius=8,
                                padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                            )
                        )
                    if not detail_rows:
                        detail_rows.append(
                            ft.Text("No session records found.", size=11, color=TEXT_DIM)
                        )
                    res_details.current.controls = detail_rows
                    result_ref.current.visible   = True
            except Exception as ex:
                att_err_ref.current.value   = f"Connection failed: {ex}"
                att_err_ref.current.visible = True
            finally:
                loader_ref.current.visible = False
                page.update()

        threading.Thread(target=fetch, daemon=True).start()

    result_panel = ft.Column(
        [
            ft.Row(
                [
                    ft.Text("Total Classes:", size=12, color=TEXT_MUTED, expand=True),
                    ft.Text("0", ref=res_total, size=16,
                            weight=ft.FontWeight.BOLD, color=TEXT_MAIN,
                            font_family="monospace"),
                ]
            ),
            ft.Row(
                [
                    ft.Text("Attended:", size=12, color=TEXT_MUTED, expand=True),
                    ft.Text("0", ref=res_present, size=16,
                            weight=ft.FontWeight.BOLD, color=TEXT_MAIN,
                            font_family="monospace"),
                ]
            ),
            arctic_divider(),
            ft.Text("ATTENDANCE %", size=9, color=TEXT_DIM,
                    font_family="monospace", weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Stack(
                    [
                        ft.Container(bgcolor=BG_INPUT, border_radius=8, expand=True),
                        ft.Container(
                            ref=res_bar,
                            bgcolor=SUCCESS,
                            border_radius=8,
                            height=14,
                            width=0,
                        ),
                    ]
                ),
                height=14,
                border_radius=8,
                border=ft.Border.all(1, BORDER),
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
            ),
            ft.Text(
                "0%", ref=res_pct, size=20,
                weight=ft.FontWeight.BOLD, color=SUCCESS,
                font_family="monospace",
                text_align=ft.TextAlign.RIGHT,
            ),
            arctic_divider(),
            ft.Text("SESSION DETAILS", size=9, color=TEXT_DIM,
                    font_family="monospace", weight=ft.FontWeight.BOLD),
            ft.Column(
                ref=res_details,
                spacing=6,
                scroll=ft.ScrollMode.AUTO,
                height=200,
            ),
        ],
        ref=result_ref,
        visible=False,
        spacing=8,
    )

    attendance_sec = ft.Column(
        [
            section_title("Check Attendance"),
            glass_card(
                ft.Column(
                    [
                        make_textfield(
                            "Roll No (e.g. BAI-24F-617)",
                            ref=roll_ref,
                            keyboard_type=ft.KeyboardType.TEXT,
                        ),
                        ft.Container(height=8),
                        make_dropdown(
                            "Select Module...", COURSES, ref=course_ref
                        ),
                        ft.Container(height=10),
                        arctic_btn(
                            "CHECK", on_click=do_check,
                            icon=ft.Icons.SEARCH, expand=True,
                        ),
                        ft.Container(height=8),
                        spinner_row("Fetching data...", ref=loader_ref),
                        ft.Text(
                            "", ref=att_err_ref, color=ERROR_C, size=12,
                            weight=ft.FontWeight.BOLD, visible=False,
                        ),
                        result_panel,
                    ],
                    spacing=0,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                )
            ),
        ],
        spacing=10,
    )

    sec_refs["calendar"]   = calendar_sec
    sec_refs["schedule"]   = schedule_sec
    sec_refs["attendance"] = attendance_sec

    calendar_sec.visible   = True
    schedule_sec.visible   = False
    attendance_sec.visible = False

    # ── Tab switcher ──
    def switch_tab(key):
        active_tab["val"] = key
        for k, sec in sec_refs.items():
            sec.visible = (k == key)
            sec.update()
        for k, btn in tab_refs.items():
            btn.bgcolor = ACCENT_DARK if k == key else "transparent"
            btn.update()

    def make_nav_btn(key, icon, label):
        btn = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icon, size=18, color=TEXT_MAIN),
                    ft.Text(label, size=9, weight=ft.FontWeight.BOLD,
                            color=TEXT_MAIN, font_family="monospace"),
                ],
                spacing=2,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=ACCENT_DARK if key == "calendar" else "transparent",
            border_radius=10,
            padding=ft.Padding.symmetric(horizontal=12, vertical=8),
            ink=True,
            on_click=lambda e, k=key: switch_tab(k),
            expand=True,
        )
        tab_refs[key] = btn
        return btn

    nav_bar = ft.Container(
        content=ft.Row(
            [
                make_nav_btn("calendar",   ft.Icons.CALENDAR_MONTH, "Calendar"),
                make_nav_btn("schedule",   ft.Icons.ACCESS_TIME,    "Schedule"),
                make_nav_btn("attendance", ft.Icons.PIE_CHART,      "Attendance"),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            spacing=4,
        ),
        bgcolor=BG_CARD + "cc",
        border=ft.Border.only(bottom=ft.BorderSide(1, BORDER_CYAN)),
        padding=ft.Padding.symmetric(horizontal=8, vertical=6),
    )

    ticker_text = (
        "Welcome to Spring 2026 Semester!  •  "
        "System Architect: Hammad Ul Hasnain  •  "
        "BS Artificial Intelligence  •  "
    )
    ticker = ft.Container(
        content=ft.Text(ticker_text, size=10, color=ACCENT, no_wrap=True),
        bgcolor=ACCENT + "18",
        border=ft.Border.only(bottom=ft.BorderSide(1, ACCENT + "33")),
        padding=ft.Padding.symmetric(horizontal=16, vertical=5),
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
    )

    top_bar = ft.Container(
        content=ft.Row(
            [
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(ft.Icons.GRID_VIEW, color=TEXT_MAIN, size=16),
                            width=36, height=36,
                            bgcolor=ACCENT_DARK,
                            border_radius=10,
                            alignment=ft.Alignment.CENTER,
                        ),
                        ft.Text("SMS-AI5B", size=16, weight=ft.FontWeight.BOLD,
                                color=TEXT_MAIN, font_family="monospace"),
                    ],
                    spacing=10, expand=True,
                ),
                ft.Container(
                    content=ft.Text(
                        "EXIT", size=11,
                        weight=ft.FontWeight.BOLD, color=ERROR_C,
                    ),
                    bgcolor=ERROR_C + "1a",
                    border=ft.Border.all(1, ERROR_C + "44"),
                    border_radius=8,
                    padding=ft.Padding.symmetric(horizontal=14, vertical=6),
                    ink=True,
                    on_click=on_exit,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor=BG_DEEP,
        border=ft.Border.only(bottom=ft.BorderSide(1, BORDER_CYAN)),
        padding=ft.Padding.symmetric(horizontal=16, vertical=10),
    )

    scroll_body = ft.Column(
        [calendar_sec, schedule_sec, attendance_sec],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=0,
    )

    return ft.Container(
        content=ft.Column(
            [
                top_bar,
                nav_bar,
                ticker,
                ft.Container(
                    content=scroll_body,
                    expand=True,
                    padding=ft.Padding.symmetric(horizontal=16, vertical=12),
                ),
            ],
            spacing=0,
            expand=True,
        ),
        expand=True,
        bgcolor=BG_DEEP,
    )

# ─────────────────────────────────────────────
# ADMIN DASHBOARD
# ─────────────────────────────────────────────

def build_admin_dashboard(page: ft.Page, on_exit):
    active_tab = {"val": "mark"}

    # ── Mark Attendance state ──
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
                                    ft.Text(s["id"], size=10, color=ACCENT,
                                            font_family="monospace",
                                            weight=ft.FontWeight.BOLD),
                                    ft.Text(s["name"], size=12, color=TEXT_MAIN,
                                            weight=ft.FontWeight.BOLD),
                                ],
                                expand=True, spacing=2,
                            ),
                            cb,
                            ft.IconButton(
                                ft.Icons.DELETE_OUTLINE,
                                icon_color=TEXT_DIM,
                                icon_size=18,
                                tooltip="Remove from list",
                                on_click=lambda e, sid=s["id"]: exclude_student(sid),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    bgcolor=BG_DEEP,
                    border=ft.Border.only(bottom=ft.BorderSide(1, BORDER)),
                    padding=ft.Padding.symmetric(horizontal=14, vertical=10),
                )
            )
        roster_ref.current.controls = rows
        page.update()

    def exclude_student(sid):
        nonlocal current_students
        current_students = [s for s in current_students if s["id"] != sid]
        if sid in checkboxes:
            del checkboxes[sid]
        rebuild_roster()

    def select_all(e):
        for cb in checkboxes.values():
            cb.value = True
        page.update()

    def deselect_all(e):
        for cb in checkboxes.values():
            cb.value = False
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

    def sync_attendance(e):
        success_ref.current.visible = False
        mark_err.current.visible    = False
        success_ref.current.update()
        mark_err.current.update()

        course = course_ref.current.value or ""
        if not course:
            mark_err.current.value   = "Please select a course first!"
            mark_err.current.visible = True
            mark_err.current.update()
            return

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
            mark_err.current.value   = "Roster is empty!"
            mark_err.current.visible = True
            mark_err.current.update()
            return

        lab_val  = lab_ref.current.value or ""
        att_date = date_ref.current.value or str(date.today())
        payload  = {
            "course":  lab_val if lab_val else course,
            "date":    att_date,
            "records": records,
        }

        sync_spin.current.visible = True
        sync_spin.current.update()

        def do_post():
            try:
                resp   = requests.post(WEB_APP_URL, json=payload, timeout=20)
                result = resp.json()
                if result.get("result") == "success":
                    success_ref.current.value   = "✓  Attendance synced successfully!"
                    success_ref.current.visible = True
                    deselect_all(None)
                else:
                    mark_err.current.value   = "Error: " + result.get("message", "Unknown")
                    mark_err.current.visible = True
            except Exception as ex:
                mark_err.current.value   = f"Network error: {ex}"
                mark_err.current.visible = True
            finally:
                sync_spin.current.visible = False
                page.update()

        threading.Thread(target=do_post, daemon=True).start()

    mark_tab_content = ft.Column(
        [
            glass_card(
                ft.Column(
                    [
                        make_dropdown(
                            "Select Course", ADMIN_COURSES,
                            ref=course_ref, on_select=on_course_select,
                        ),
                        ft.Container(height=8),
                        ft.Dropdown(
                            ref=lab_ref,
                            hint_text="Select Lab (Optional)",
                            bgcolor=BG_INPUT,
                            border_color=BORDER_CYAN,
                            focused_border_color=ACCENT,
                            color=TEXT_MAIN,
                            hint_style=ft.TextStyle(color=TEXT_DIM),
                            border_radius=10,
                            options=[ft.dropdown.Option("", "No Lab")],
                            content_padding=ft.Padding.symmetric(horizontal=14, vertical=10),
                            text_style=ft.TextStyle(size=12, color=TEXT_MAIN),
                        ),
                        ft.Container(height=8),
                        make_textfield(
                            "YYYY-MM-DD", ref=date_ref,
                            label="Attendance Date",
                            value=str(date.today()),
                        ),
                    ],
                    spacing=0,
                )
            ),
            ft.Container(height=10),
            ft.Row(
                [
                    ft.Text("STUDENT ROSTER", size=13,
                            weight=ft.FontWeight.BOLD,
                            color=TEXT_MAIN, font_family="monospace", expand=True),
                    ft.Container(
                        content=ft.Text("ALL", size=10,
                                        weight=ft.FontWeight.BOLD, color=ACCENT),
                        bgcolor=ACCENT + "1a",
                        border=ft.Border.all(1, ACCENT + "44"),
                        border_radius=8,
                        padding=ft.Padding.symmetric(horizontal=12, vertical=6),
                        ink=True, on_click=select_all,
                    ),
                    ft.Container(width=6),
                    ft.Container(
                        content=ft.Text("CLEAR", size=10,
                                        weight=ft.FontWeight.BOLD, color=TEXT_DIM),
                        bgcolor=BORDER,
                        border=ft.Border.all(1, TEXT_DIM + "44"),
                        border_radius=8,
                        padding=ft.Padding.symmetric(horizontal=12, vertical=6),
                        ink=True, on_click=deselect_all,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Container(
                content=ft.Column(
                    ref=roster_ref,
                    spacing=0,
                    scroll=ft.ScrollMode.AUTO,
                ),
                bgcolor=BG_CARD,
                border=ft.Border.all(1, BORDER_CYAN),
                border_radius=12,
                height=360,
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
            ),
            ft.Container(height=10),
            arctic_btn("SYNC TO SHEETS", on_click=sync_attendance,
                       icon=ft.Icons.CLOUD_UPLOAD, expand=True),
            spinner_row("Syncing...", ref=sync_spin),
            ft.Text("", ref=success_ref, color=SUCCESS, size=12,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER, visible=False),
            ft.Text("", ref=mark_err, color=ERROR_C, size=12,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER, visible=False),
        ],
        spacing=6,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    # ── Class Analytics ──
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
        rep_err.current.update()
        rep_content.current.update()

        if not course:
            rep_err.current.value   = "Please select a module."
            rep_err.current.visible = True
            rep_err.current.update()
            return

        rep_spin.current.visible = True
        rep_spin.current.update()

        def do_fetch():
            try:
                url  = f"{WEB_APP_URL}?action=classReport&course={course}"
                resp = requests.get(url, timeout=20)
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
                                content=ft.Row(
                                    [
                                        ft.Column(
                                            [
                                                ft.Text(s.get("id", ""), size=9,
                                                        color=ACCENT, font_family="monospace"),
                                                ft.Text(s.get("name", ""), size=12,
                                                        color=TEXT_MAIN,
                                                        weight=ft.FontWeight.BOLD),
                                            ],
                                            expand=True, spacing=2,
                                        ),
                                        ft.Column(
                                            [
                                                ft.Text(
                                                    f"{s.get('present',0)}/{s.get('total',0)}",
                                                    size=11, color=TEXT_MUTED,
                                                    font_family="monospace",
                                                    text_align=ft.TextAlign.RIGHT,
                                                ),
                                                ft.Text(
                                                    f"{pct}%",
                                                    size=14, weight=ft.FontWeight.BOLD,
                                                    color=clr, font_family="monospace",
                                                    text_align=ft.TextAlign.RIGHT,
                                                ),
                                            ],
                                            horizontal_alignment=ft.CrossAxisAlignment.END,
                                            spacing=2,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                bgcolor=BG_DEEP,
                                border=ft.Border.only(bottom=ft.BorderSide(1, BORDER)),
                                padding=ft.Padding.symmetric(horizontal=14, vertical=10),
                            )
                        )
                    rep_tbody.current.controls = rows
                    rep_content.current.visible = True
            except Exception as ex:
                rep_err.current.value   = f"Failed: {ex}"
                rep_err.current.visible = True
            finally:
                rep_spin.current.visible = False
                page.update()

        threading.Thread(target=do_fetch, daemon=True).start()

    report_tab_content = ft.Column(
        [
            glass_card(
                ft.Column(
                    [
                        make_dropdown(
                            "Select Module for Class Report...",
                            COURSES, ref=rep_course,
                        ),
                        ft.Container(height=10),
                        arctic_btn("GENERATE REPORT", on_click=fetch_report,
                                   icon=ft.Icons.BAR_CHART, expand=True),
                    ],
                    spacing=0,
                )
            ),
            ft.Container(height=10),
            spinner_row("Analyzing class data...", ref=rep_spin),
            ft.Text("", ref=rep_err, color=ERROR_C, size=12,
                    weight=ft.FontWeight.BOLD, visible=False),
            ft.Column(
                [
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Text("TOTAL SESSIONS HELD", size=10,
                                        color=TEXT_MUTED, font_family="monospace",
                                        weight=ft.FontWeight.BOLD, expand=True),
                                ft.Text("0", ref=rep_total, size=22,
                                        weight=ft.FontWeight.BOLD,
                                        color=ACCENT, font_family="monospace"),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        bgcolor=BG_CARD,
                        border=ft.Border.all(1, BORDER_CYAN),
                        border_radius=12,
                        padding=ft.Padding.symmetric(horizontal=16, vertical=12),
                    ),
                    ft.Container(
                        content=ft.Column(
                            ref=rep_tbody,
                            spacing=0,
                            scroll=ft.ScrollMode.AUTO,
                        ),
                        bgcolor=BG_CARD,
                        border=ft.Border.all(1, BORDER_CYAN),
                        border_radius=12,
                        height=400,
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                    ),
                ],
                ref=rep_content,
                visible=False,
                spacing=10,
                scroll=ft.ScrollMode.AUTO,
            ),
        ],
        spacing=6,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    # ── Tab switching ──
    mark_cont = ft.Ref[ft.Container]()
    rep_cont  = ft.Ref[ft.Container]()

    def switch_admin_tab(key):
        active_tab["val"] = key
        mark_tab_content.visible   = (key == "mark")
        report_tab_content.visible = (key == "report")
        mark_cont.current.bgcolor  = ACCENT_DARK if key == "mark"   else "transparent"
        rep_cont.current.bgcolor   = ACCENT_DARK if key == "report" else "transparent"
        mark_cont.current.update()
        rep_cont.current.update()
        page.update()

    tab_bar = ft.Container(
        content=ft.Row(
            [
                ft.Container(
                    ref=mark_cont,
                    content=ft.Text("MARK ATTENDANCE", size=11,
                                    weight=ft.FontWeight.BOLD, color=TEXT_MAIN,
                                    font_family="monospace"),
                    bgcolor=ACCENT_DARK,
                    border_radius=8,
                    padding=ft.Padding.symmetric(horizontal=14, vertical=8),
                    ink=True,
                    on_click=lambda e: switch_admin_tab("mark"),
                ),
                ft.Container(
                    ref=rep_cont,
                    content=ft.Text("CLASS ANALYTICS", size=11,
                                    weight=ft.FontWeight.BOLD, color=TEXT_MUTED,
                                    font_family="monospace"),
                    bgcolor="transparent",
                    border_radius=8,
                    padding=ft.Padding.symmetric(horizontal=14, vertical=8),
                    ink=True,
                    on_click=lambda e: switch_admin_tab("report"),
                ),
            ],
            spacing=6,
        ),
        border=ft.Border.only(bottom=ft.BorderSide(1, BORDER)),
        padding=ft.Padding.only(bottom=6),
    )

    top_bar = ft.Container(
        content=ft.Row(
            [
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(ft.Icons.ADMIN_PANEL_SETTINGS,
                                            color=TEXT_MAIN, size=16),
                            width=36, height=36,
                            bgcolor=ACCENT_DARK,
                            border_radius=10,
                            alignment=ft.Alignment.CENTER,
                        ),
                        ft.Text("ADMIN PORTAL", size=15,
                                weight=ft.FontWeight.BOLD,
                                color=ACCENT, font_family="monospace"),
                    ],
                    spacing=10, expand=True,
                ),
                ft.Container(
                    content=ft.Text("EXIT", size=11,
                                    weight=ft.FontWeight.BOLD, color=ERROR_C),
                    bgcolor=ERROR_C + "1a",
                    border=ft.Border.all(1, ERROR_C + "44"),
                    border_radius=8,
                    padding=ft.Padding.symmetric(horizontal=14, vertical=6),
                    ink=True,
                    on_click=on_exit,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor=BG_DEEP,
        border=ft.Border.only(bottom=ft.BorderSide(1, ACCENT + "55")),
        padding=ft.Padding.symmetric(horizontal=16, vertical=10),
    )

    mark_tab_content.visible   = True
    report_tab_content.visible = False

    return ft.Container(
        content=ft.Column(
            [
                top_bar,
                ft.Container(
                    content=ft.Column(
                        [
                            tab_bar,
                            ft.Container(height=10),
                            mark_tab_content,
                            report_tab_content,
                        ],
                        spacing=0,
                        expand=True,
                    ),
                    expand=True,
                    padding=ft.Padding.symmetric(horizontal=16, vertical=8),
                ),
            ],
            spacing=0,
            expand=True,
        ),
        expand=True,
        bgcolor=BG_DEEP,
        data=rebuild_roster,   # called after widget added to page
    )

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main(page: ft.Page):
    page.title      = "SMS Portal | BS-AI"
    page.bgcolor    = BG_DEEP
    page.theme_mode = ft.ThemeMode.DARK
    page.padding    = 0
    page.window.width  = 390
    page.window.height = 844

    def set_view(widget):
        page.controls.clear()
        page.controls.append(widget)
        page.update()
        if hasattr(widget, "data") and callable(widget.data):
            widget.data()

    def go_role():
        set_view(build_role_selection(
            on_student=lambda e: go_student(),
            on_admin=lambda e: go_login(),
        ))

    def go_login():
        set_view(build_login_page(
            on_login=go_admin,
            on_back=lambda e: go_role(),
        ))

    def go_student():
        set_view(build_student_dashboard(
            page=page,
            on_exit=lambda e: go_role(),
        ))

    def go_admin():
        set_view(build_admin_dashboard(
            page=page,
            on_exit=lambda e: go_role(),
        ))

    set_view(build_splash())

    def after_splash():
        import time
        time.sleep(1.2)
        go_role()

    threading.Thread(target=after_splash, daemon=True).start()


ft.run(main)
