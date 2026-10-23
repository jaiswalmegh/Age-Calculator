
import tkinter as tk
from tkinter import messagebox
from datetime import date
import calendar

import customtkinter as ctk
from tkcalendar import DateEntry

# ==================== THEME ====================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG = "#0B1020"
PANEL = "#121A2D"
BORDER = "#263653"
TEXT = "#F4F7FF"
MUTED = "#9AAAC5"
CYAN = "#41D9FF"
PURPLE = "#9B8CFF"
GREEN = "#4DE0B0"
ORANGE = "#FFBE6B"


# ==================== AGE ENGINE ====================
def calculate_age(dob, today):
    if dob > today:
        raise ValueError("Date of birth cannot be in the future.")

    years = today.year - dob.year
    months = today.month - dob.month
    days = today.day - dob.day

    if days < 0:
        previous_month = today.month - 1 or 12
        previous_year = today.year if today.month > 1 else today.year - 1

        days += calendar.monthrange(
            previous_year, previous_month
        )[1]
        months -= 1

    if months < 0:
        months += 12
        years -= 1

    return years, months, days


def next_birthday(dob, today):
    year = today.year

    while True:
        try:
            birthday = date(year, dob.month, dob.day)
        except ValueError:
            # February 29 birthdays use February 28
            # in non-leap years.
            birthday = date(year, 2, 28)

        if birthday >= today:
            return birthday

        year += 1


def zodiac_sign(dob):
    month_day = (dob.month, dob.day)

    if month_day >= (12, 22) or month_day < (1, 20):
        return "Capricorn"

    boundaries = [
        ((1, 20), "Aquarius"),
        ((2, 19), "Pisces"),
        ((3, 21), "Aries"),
        ((4, 20), "Taurus"),
        ((5, 21), "Gemini"),
        ((6, 21), "Cancer"),
        ((7, 23), "Leo"),
        ((8, 23), "Virgo"),
        ((9, 23), "Libra"),
        ((10, 23), "Scorpio"),
        ((11, 22), "Sagittarius"),
        ((12, 22), "Capricorn"),
    ]

    result = "Capricorn"

    for boundary, sign in boundaries:
        if month_day < boundary:
            return result
        result = sign

    return result


# ==================== APPLICATION ====================
class AuroraAgeCalculator(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("AURORA | Age Intelligence")
        self.geometry("1100x760")
        self.minsize(900, 650)
        self.configure(fg_color=BG)

        self.build_ui()
        self.calculate()

    def make_card(self, parent, accent=BORDER):
        return ctk.CTkFrame(
            parent,
            fg_color=PANEL,
            corner_radius=18,
            border_width=1,
            border_color=accent
        )

    def label(self, parent, text, size=13,
              color=TEXT, bold=False):
        return ctk.CTkLabel(
            parent,
            text=text,
            text_color=color,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=size,
                weight="bold" if bold else "normal"
            )
        )

    def build_ui(self):

        # Scrollable main screen
        self.main = ctk.CTkScrollableFrame(
            self,
            fg_color=BG,
            scrollbar_button_color=BORDER,
            scrollbar_button_hover_color=CYAN
        )
        self.main.pack(fill="both", expand=True)

        # ==================== HEADER ====================
        header = ctk.CTkFrame(
            self.main, fg_color="transparent"
        )
        header.pack(fill="x", padx=32, pady=(26, 22))

        left = ctk.CTkFrame(
            header, fg_color="transparent"
        )
        left.pack(side="left", fill="x", expand=True)

        self.label(
            left, "✦  A U R O R A",
            13, CYAN, True
        ).pack(anchor="w")

        self.label(
            left, "Age Intelligence",
            30, TEXT, True
        ).pack(anchor="w", pady=(6, 0))

        self.label(
            left,
            "Your timeline, precisely calculated.",
            13, MUTED
        ).pack(anchor="w", pady=(3, 0))

        self.today_label = self.label(
            header, "", 12, MUTED
        )
        self.today_label.pack(
            side="right", anchor="ne", pady=12
        )

        # ==================== INPUT PANEL ====================
        input_card = self.make_card(self.main)
        input_card.pack(
            fill="x", padx=32, pady=(0, 18)
        )

        top = ctk.CTkFrame(
            input_card, fg_color="transparent"
        )
        top.pack(fill="x", padx=22, pady=(20, 12))

        self.label(
            top, "01  /  YOUR DETAILS",
            11, CYAN, True
        ).pack(side="left")

        self.label(
            top, "PRIVATE BY DESIGN",
            10, MUTED, True
        ).pack(side="right")

        form = ctk.CTkFrame(
            input_card, fg_color="transparent"
        )
        form.pack(fill="x", padx=22, pady=(0, 22))

        self.label(
            form, "Date of birth", 13, TEXT, True
        ).pack(anchor="w", pady=(0, 8))

        self.dob_picker = DateEntry(
            form,
            width=22,
            date_pattern="dd/mm/yyyy",
            maxdate=date.today(),
            background="#1E2B45",
            foreground="white",
            bordercolor=BORDER,
            headersbackground="#1E2B45",
            headersforeground=CYAN,
            selectbackground="#087E9B",
            selectforeground="white",
            normalbackground=PANEL,
            normalforeground="white",
            weekendbackground="#172239",
            weekendforeground="white",
            font=("Segoe UI", 12)
        )
        self.dob_picker.pack(
            side="left", ipady=7, padx=(0, 15)
        )

        ctk.CTkButton(
            form,
            text="CALCULATE MY AGE   ↗",
            command=self.calculate,
            height=42,
            width=220,
            corner_radius=12,
            fg_color=CYAN,
            hover_color="#22BFE8",
            text_color="#07111F",
            font=ctk.CTkFont(
                "Segoe UI", 12, "bold"
            )
        ).pack(side="right")

        # ==================== MAIN RESULT ====================
        result = self.make_card(self.main, CYAN)
        result.pack(
            fill="x", padx=32, pady=(0, 18)
        )

        result_header = ctk.CTkFrame(
            result, fg_color="transparent"
        )
        result_header.pack(
            fill="x", padx=22, pady=(20, 0)
        )

        self.label(
            result_header,
            "02  /  YOUR EXACT AGE",
            11, CYAN, True
        ).pack(side="left")

        self.status = self.label(
            result_header,
            "● READY",
            10, GREEN, True
        )
        self.status.pack(side="right")

        self.age_display = self.label(
            result,
            "Choose your date of birth",
            26, TEXT, True
        )
        self.age_display.pack(
            anchor="w", padx=22, pady=(18, 5)
        )

        self.age_details = self.label(
            result,
            "Your age breakdown will appear here.",
            12, MUTED
        )
        self.age_details.pack(
            anchor="w", padx=22, pady=(0, 22)
        )

        # ==================== STATISTICS ====================
        stats_frame = ctk.CTkFrame(
            self.main, fg_color="transparent"
        )
        stats_frame.pack(
            fill="x", padx=32, pady=(0, 18)
        )

        stats_frame.grid_columnconfigure(
            (0, 1, 2, 3), weight=1, uniform="stats"
        )

        stats = [
            ("TOTAL MONTHS", "months", PURPLE),
            ("TOTAL WEEKS", "weeks", CYAN),
            ("TOTAL DAYS", "days", GREEN),
            ("TOTAL HOURS", "hours", ORANGE)
        ]

        self.stat_values = {}

        for column, (title, key, color) in enumerate(stats):
            tile = self.make_card(stats_frame)
            tile.grid(
                row=0, column=column,
                sticky="nsew",
                padx=(0 if column == 0 else 6,
                      0 if column == 3 else 6)
            )

            self.label(
                tile, title, 10, MUTED, True
            ).pack(
                anchor="w", padx=14, pady=(17, 9)
            )

            value = self.label(
                tile, "--", 23, color, True
            )
            value.pack(
                anchor="w", padx=14, pady=(0, 5)
            )

            self.label(
                tile, "Calculated total", 10, MUTED
            ).pack(
                anchor="w", padx=14, pady=(0, 17)
            )

            self.stat_values[key] = value

        # ==================== INSIGHTS ====================
        insights = ctk.CTkFrame(
            self.main, fg_color="transparent"
        )
        insights.pack(
            fill="x", padx=32, pady=(0, 20)
        )

        insights.grid_columnconfigure(
            (0, 1), weight=1, uniform="insights"
        )

        birthday_card = self.make_card(insights)
        birthday_card.grid(
            row=0, column=0, sticky="nsew",
            padx=(0, 8)
        )

        zodiac_card = self.make_card(insights)
        zodiac_card.grid(
            row=0, column=1, sticky="nsew",
            padx=(8, 0)
        )

        self.label(
            birthday_card, "✧  NEXT BIRTHDAY",
            11, ORANGE, True
        ).pack(
            anchor="w", padx=18, pady=(18, 10)
        )

        self.birthday_value = self.label(
            birthday_card, "-- days to go",
            21, TEXT, True
        )
        self.birthday_value.pack(
            anchor="w", padx=18
        )

        self.birthday_date = self.label(
            birthday_card, "Your next milestone.",
            12, MUTED
        )
        self.birthday_date.pack(
            anchor="w", padx=18, pady=(5, 18)
        )

        self.label(
            zodiac_card, "✧  BIRTHDAY PROFILE",
            11, PURPLE, True
        ).pack(
            anchor="w", padx=18, pady=(18, 10)
        )

        self.zodiac_value = self.label(
            zodiac_card, "--",
            21, TEXT, True
        )
        self.zodiac_value.pack(
            anchor="w", padx=18
        )

        self.zodiac_date = self.label(
            zodiac_card, "Your birthday profile.",
            12, MUTED
        )
        self.zodiac_date.pack(
            anchor="w", padx=18, pady=(5, 18)
        )

        # ==================== FOOTER ====================
        self.label(
            self.main,
            "AURORA AGE INTELLIGENCE  •  POWERED BY PYTHON",
            10, "#52617C", True
        ).pack(pady=(0, 22))

    # ==================== CALCULATION ====================
    def calculate(self):
        today = date.today()

        self.today_label.configure(
            text=today.strftime("%d %b %Y").upper()
        )

        try:
            dob = self.dob_picker.get_date()

            if dob > today:
                raise ValueError(
                    "Date of birth cannot be in the future."
                )

            years, months, days = calculate_age(
                dob, today
            )

            total_days = (today - dob).days
            total_months = years * 12 + months
            total_weeks = total_days // 7
            total_hours = total_days * 24

            birthday = next_birthday(dob, today)
            days_left = (birthday - today).days

            self.age_display.configure(
                text=(
                    f"{years} YEARS   "
                    f"{months} MONTHS   "
                    f"{days} DAYS"
                )
            )

            self.age_details.configure(
                text=(
                    f"Born {dob.strftime('%A, %d %B %Y')}  "
                    f"•  {total_days:,} days lived"
                )
            )

            self.stat_values["months"].configure(
                text=f"{total_months:,}"
            )
            self.stat_values["weeks"].configure(
                text=f"{total_weeks:,}"
            )
            self.stat_values["days"].configure(
                text=f"{total_days:,}"
            )
            self.stat_values["hours"].configure(
                text=f"{total_hours:,}"
            )

            if days_left == 0:
                birthday_text = "It's your birthday! 🎉"
            else:
                birthday_text = f"{days_left} days to go"

            self.birthday_value.configure(
                text=birthday_text
            )

            self.birthday_date.configure(
                text=(
                    f"{birthday.strftime('%d %B %Y')}  "
                    f"•  {birthday.strftime('%A')}"
                )
            )

            self.zodiac_value.configure(
                text=zodiac_sign(dob)
            )

            self.zodiac_date.configure(
                text=dob.strftime("Born on %d %B")
            )

            self.status.configure(
                text="● CALCULATED",
                text_color=GREEN
            )

        except (ValueError, TypeError) as error:
            self.status.configure(
                text="● INVALID DATE",
                text_color="#FF6B81"
            )
            messagebox.showerror(
                "Invalid date", str(error)
            )


if __name__ == "__main__":
    app = AuroraAgeCalculator()
    app.mainloop()
