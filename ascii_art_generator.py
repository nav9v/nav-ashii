import sys

import pyfiglet
from ttkthemes import ThemedTk
import tkinter as tk
from tkinter import ttk, messagebox, colorchooser, font, filedialog
from tkinter.font import Font
import os
import threading
import time
import webbrowser

RUNNING_AS_EXE = getattr(sys, 'frozen', True)

class ASCIIArtStudio:
    
    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    
    def __init__(self, root):
        self.root = root
        self.root.title("ASCII txt by nav9v")
        self.root.geometry("1380x800")  # 16:10 aspect ratio
        self.root.minsize(1024, 600)  # Minimum usable size

        # Initialize variables before UI components
        self.initialize_variables()  # MUST come before UI components
        self.initialize_style()
        self.create_main_layout()
        self.initialize_fonts()
        self.load_favorites()
        self.create_ui_components()
        self.create_footer()
        self.setup_keybindings()
        self.apply_initial_theme()
        self.setup_theme_cycling()
        
        icon_path = self.resource_path("icon.png")
        self.icon = tk.PhotoImage(file=icon_path)
        self.root.iconphoto(False, self.icon)


    def initialize_style(self):
        # Define themes - moved from initialize_variables for better organization
        self.themes = [
            (
                "🌃 PinkNight",  # Theme Name
                "#f28fab",
                "#1f1926",
                "#261b30",
                "#2a1f39",
                "#f28fab",
                "#fce1eb",
                "#39274f",
                "#51336d",
            ),
            (
                "🎨 Material",
                "#eceff1",
                "#263238",
                "#37474f",
                "#263238",
                "#90a4ae",
                "#eceff1",
                "#455a64",
                "#1c262b",
            ),
            (
                "☕ Coffee",  # Theme Name
                "#d7ccc8",  # Text Color
                "#4e342e",  # Background Color
                "#3e2723",  # Secondary Background
                "#6d4c41",  # Primary Background
                "#a1887f",  # Accent Color
                "#bcaaa4",  # UI Text Color
                "#8d6e63",  # Selection Background
                ),
                (
                    "🌅 Sunset",
                    "#ff9e80",
                    "#4e342e",
                    "#5f4339",
                    "#4e342e",
                    "#ff9e80",
                    "#ff9e80",
                    "#6a4f48",
                    "#3d2a25",
                ),
                (
                    "🤖 Cyberpunk",
                    "#00ff9d",
                    "#0a0a2a",
                    "#1a1a3a",
                    "#0a0a2a",
                    "#00ff9d",
                    "#00ff9d",
                    "#252545",
                    "#05051a",
                ),
                (
                    "❄️ Nordic",
                    "#d8dee9",
                    "#2e3440",
                    "#3b4252",
                    "#2e3440",
                    "#88c0d0",
                    "#d8dee9",
                    "#4c566a",
                    "#21252e",
                ),
                (
                    "🧛 Dracula",
                    "#f8f8f2",
                    "#282a36",
                    "#383a4e",
                    "#282a36",
                    "#bd93f9",
                    "#f8f8f2",
                    "#44475a",
                    "#1d1e27",
                ),
                (
                    "🌊 Ocean",
                    "#e0f7fa",
                    "#006064",
                    "#007174",
                    "#006064",
                    "#80deea",
                    "#e0f7fa",
                    "#00838f",
                    "#004042",
                ),
                (
                    "🌳 Forest",
                    "#c8e6c9",
                    "#1b5e20",
                    "#2b6e30",
                    "#1b5e20",
                    "#81c784",
                    "#c8e6c9",
                    "#388e3c",
                    "#104014",
                ),
                (
                    "🌌 Midnight",
                    "#ffffff",
                    "#000033",
                    "#000066",
                    "#000033",
                    "#4444ff",
                    "#ffffff",
                    "#0000aa",
                    "#000022",
                ),
                (
                    "📺 Retro",
                    "#39ff14",
                    "#000000",
                    "#222222",
                    "#000000",
                    "#39ff14",
                    "#dddddd",
                    "#444444",
                    "#111111",
                ),
                (
                    "🩸 Crimson",
                    "#fafafa",
                    "#8b0000",
                    "#a00000",
                    "#8b0000",
                    "#ff5555",
                    "#fafafa",
                    "#cc0000",
                    "#6b0000",
                ),
                (
                    "🌻 Sunshine",
                    "#3E2723",
                    "#FFF8E1",
                    "#FFECB3",
                    "#FFE082",
                    "#FFC107",
                    "#3E2723",
                    "#FFCA28",
                    "#FFA000",
                ),
                (
                    "🌲 Pine",
                    "#c5e1a5",
                    "#1b5e20",
                    "#2e7d32",
                    "#388e3c",
                    "#4caf50",
                    "#ffffff",
                    "#66bb6a",
                    "#43a047",
                ),
                (
                    "🍃 Mint",
                    "#00ffcc",
                    "#004d40",
                    "#00796b",
                    "#00695c",
                    "#00bfa5",
                    "#e0f2f1",
                    "#00897b",
                    "#004d40",
                ),
                (
                    "🎭 Neon",
                    "#00FFFF",
                    "#000000",
                    "#0A0A0A",
                    "#000000",
                    "#FF00FF",
                    "#00FFFF",
                    "#FF00FF",
                    "#300030",
                ),
                (
                    "🍊 Citrus",
                    "#FFFFFF",
                    "#FF6600",
                    "#FF8533",
                    "#FF6600",
                    "#FFCC00",
                    "#FFFFFF",
                    "#FFAA33",
                    "#CC5200",
                ),
                (
                    "🌌 Galaxy",
                    "#E0E0FF",
                    "#0F0F3D",
                    "#1F1F4D",
                    "#0F0F3D",
                    "#8A2BE2",
                    "#E0E0FF",
                    "#4B0082",
                    "#191970",
            ),
        ]


        # Load current theme colors - defaults to first theme
        (
            name,
            text_color,
            bg_color,
            secondary_bg,
            primary_bg,
            accent_color,
            text_color_ui,
            selection_bg,
            hover_bg,
        ) = self.themes[0]

        # Base colors - now derived from theme
        self.primary_bg = primary_bg
        self.secondary_bg = secondary_bg
        self.accent_color = accent_color
        self.text_color_ui = text_color_ui
        self.highlight_color = accent_color  # Use accent color as highlight
        self.selection_bg = selection_bg
        self.entry_bg = primary_bg
        self.entry_fg = text_color_ui
        self.hover_bg = hover_bg

        # ASCII art colors (now linked to the theme system)
        self.text_color = text_color
        self.bg_color = bg_color

        self.style = ttk.Style()
        # Check if "clam" theme is available, otherwise use default
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass  # Use default theme if "clam" is not available

        # Apply the styles with the theme colors
        self.apply_styles()

        self.style.configure(
            "Footer.TLabel",
            background=self.primary_bg,
            foreground=self.text_color_ui,
            font=("Segoe UI", 8, "italic"),  # Smaller, italic text
        )

    def apply_styles(self):
        """Apply all styles with current theme colors"""
        # Base style configurations
        self.style.configure(
            ".",
            background=self.primary_bg,
            foreground=self.text_color_ui,
            font=("Segoe UI", 10),
            borderwidth=1,
        )

        # Frame styles
        self.style.configure("TFrame", background=self.secondary_bg)
        self.style.configure("Primary.TFrame", background=self.primary_bg)

        # Button styles with improved visual feedback
        self.style.configure(
            "TButton",
            background=self.accent_color,
            foreground=self.primary_bg,
            borderwidth=2,
            relief="raised",
            padding=8,
            focuscolor=self.highlight_color,
        )
        self.style.map(
            "TButton",
            background=[("active", self.accent_color), ("pressed", self.selection_bg)],
            relief=[("pressed", "sunken"), ("!pressed", "raised")],
            bordercolor=[("focus", self.highlight_color)],
        )

        # Label styles
        self.style.configure(
            "TLabel", background=self.secondary_bg, foreground=self.text_color_ui
        )
        self.style.configure(
            "Primary.TLabel", background=self.primary_bg, foreground=self.accent_color
        )

        # Notebook styles
        self.style.configure("TNotebook", background=self.primary_bg)
        self.style.configure(
            "TNotebook.Tab",
            background=self.primary_bg,
            foreground=self.text_color_ui,
            padding=(20, 8),
        )
        self.style.map(
            "TNotebook.Tab",
            background=[("selected", self.accent_color)],
            foreground=[("selected", self.primary_bg)],
        )

        # Enhanced scrollbar styling
        self.style.configure(
            "TScrollbar",
            gripcount=0,
            background=self.selection_bg,
            arrowcolor=self.text_color_ui,
            bordercolor=self.primary_bg,
            troughcolor=self.primary_bg,
            width=14,
        )
        self.style.map(
            "TScrollbar",
            background=[("active", self.hover_bg)],
            arrowcolor=[("active", self.accent_color)],
        )

        # Enhanced checkbox styling
        self.style.configure(
            "TCheckbutton",
            background=self.secondary_bg,
            foreground=self.text_color_ui,
            indicatorbackground=self.primary_bg,
            indicatorforeground=self.accent_color,
            padding=4,
        )
        self.style.map(
            "TCheckbutton",
            background=[("active", self.secondary_bg)],
            foreground=[("active", self.accent_color)],
            indicatorbackground=[
                ("active", self.hover_bg),
                ("selected", self.accent_color),
            ],
            indicatorforeground=[("selected", self.primary_bg)],
        )

        # Combobox styling
        self.style.configure(
            "TCombobox",
            fieldbackground=self.entry_bg,
            foreground=self.entry_fg,
            background=self.secondary_bg,
            arrowcolor=self.accent_color,
            padding=6,
        )
        self.style.map(
            "TCombobox",
            fieldbackground=[("readonly", self.entry_bg)],
            foreground=[("readonly", self.entry_fg)],
            selectbackground=[("readonly", self.selection_bg)],
            selectforeground=[("readonly", self.entry_fg)],
        )

        # Scale slider styling
        self.style.configure(
            "TScale",
            background=self.secondary_bg,
            troughcolor=self.primary_bg,
            sliderrelief="raised",
            sliderthickness=20,
        )
        self.style.map(
            "TScale",
            background=[("active", self.secondary_bg)],
            troughcolor=[("active", self.primary_bg)],
        )

        # Entry styling
        self.style.configure(
            "TEntry",
            fieldbackground=self.entry_bg,
            foreground=self.entry_fg,
            bordercolor=self.selection_bg,
            lightcolor=self.selection_bg,
            darkcolor=self.selection_bg,
            padding=6,
        )
        self.style.map(
            "TEntry",
            fieldbackground=[("focus", self.entry_bg)],
            bordercolor=[("focus", self.accent_color)],
        )

        # Create Action button style
        self.style.configure(
            "Action.TButton",
            background=self.accent_color,
            foreground=self.primary_bg,
            font=("Segoe UI", 10, "bold"),
        )

        # Create Star button style
        self.style.configure(
            "Star.TButton",
            background="#FFCC00",
            foreground="#2E3440",
            font=("Segoe UI", 10, "bold"),
        )

        # Create Animation button style
        self.style.configure(
            "Anim.TButton",
            background=self.accent_color,
            foreground=self.primary_bg,
            font=("Segoe UI", 10, "bold"),
        )

        # Create LabelFrame style
        self.style.configure(
            "TLabelframe", background=self.secondary_bg, foreground=self.text_color_ui
        )
        self.style.configure(
            "TLabelframe.Label",
            background=self.primary_bg,
            foreground=self.accent_color,
            font=("Segoe UI", 10, "bold"),
        )

        # Create Separator style
        self.style.configure("TSeparator", background=self.selection_bg)

        # Status bar style
        self.style.configure(
            "Status.TLabel",
            background=self.primary_bg,
            foreground=self.accent_color,
            font=("Segoe UI", 9, "italic"),
            padding=(12, 4),
        )

        # Update root window background
        self.root.config(background=self.primary_bg)

    def create_main_layout(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=18, pady=18)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.paned_window = ttk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
        self.paned_window.grid(row=0, column=0, sticky="nsew")

        # Configure main_frame to expand
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Control Panel (left side)
        self.control_frame = ttk.Frame(self.paned_window, width=400)

        # Output Panel (right side)
        self.output_frame = ttk.LabelFrame(self.paned_window)

        # Add frames to paned window
        self.paned_window.add(self.control_frame, weight=0)  # Fixed width
        self.paned_window.add(self.output_frame, weight=1)  # Takes remaining space

        # Configure output frame to expand
        self.output_frame.grid_rowconfigure(0, weight=1)
        self.output_frame.grid_columnconfigure(0, weight=1)

    def initialize_variables(self):
        # Core variables
        self.font_width = tk.DoubleVar(value=1.0)
        self.font_size = tk.IntVar(value=8)
        self.display_font = tk.StringVar(value="MS Gothic")
        self.updating_banner = False
        self.current_theme_index = 0

        # Animation variables
        self.animation_speed = tk.DoubleVar(value=0.5)
        self.animating = False
        self.animation_thread = None

        # Status variable
        self.status_var = tk.StringVar(value="Ready")

        # Favorites system
        self.favorite_fonts = []

        # Text history system
        self.text_history = []
        self.max_history = 10

    def initialize_fonts(self):
        try:
            self.figlet_fonts = pyfiglet.FigletFont.getFonts()
            if not self.figlet_fonts:
                raise ValueError("No Figlet fonts found")

            # Get system monospace fonts
            self.system_fonts = []
            for f in font.families():
                try:
                    if Font(family=f, size=10).metrics("fixed"):
                        self.system_fonts.append(f)
                except:
                    continue

            if "MS Gothic" not in self.system_fonts:
                self.system_fonts.append("MS Gothic")

            self.system_fonts = (
                sorted(self.system_fonts)
                if self.system_fonts
                else ["MS Gothic", "Courier", "Courier New", "Consolas"]
            )

            # Now that we have system fonts, set the display_font variable
            if self.display_font.get() not in self.system_fonts:
                self.display_font.set(
                    "MS Gothic"
                    if "MS Gothic" in self.system_fonts
                    else self.system_fonts[0]
                )

        except Exception as e:
            print(f"Font error: {e}")
            self.figlet_fonts = ["standard"]
            self.system_fonts = ["MS Gothic", "Courier New"]
            self.display_font.set("MS Gothic")

    def create_ui_components(self):
        self.create_notebook()
        self.create_text_tab()
        self.create_style_tab()
        self.create_output_area()
        self.create_action_buttons()
        self.create_status_bar()

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.control_frame)
        self.notebook.config(padding=(12, 8, 12, 12))  # T R B L
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        self.text_tab = ttk.Frame(self.notebook, padding=16, style="TFrame")
        self.style_tab = ttk.Frame(self.notebook, padding=16, style="TFrame")
        self.notebook.add(self.text_tab, text="✏️ Text & Font")
        self.notebook.add(self.style_tab, text="🎨 Style & Themes")

    def create_text_tab(self):
        # Input Section
        ttk.Label(self.text_tab, text="Input Text:").grid(
            row=0, column=0, padx=14, pady=12, sticky=tk.W
        )
        self.text_var = tk.StringVar(value="Helow")

        # Use ttk.Entry with the configured style
        self.text_entry = ttk.Entry(
            self.text_tab,
            textvariable=self.text_var,
            font=("Segoe UI", 11),
            style="TEntry",
        )
        self.text_entry.grid(row=0, column=1, padx=14, pady=12, sticky=tk.EW)
        self.text_entry.bind("<KeyRelease>", lambda e: self.update_banner())

        # Add preview checkbox with improved styling
        preview_frame = ttk.Frame(self.text_tab, style="TFrame")
        preview_frame.grid(row=0, column=2, padx=(0, 14), pady=12, sticky=tk.W)

        self.preview_var = tk.BooleanVar(value=True)
        self.preview_check = ttk.Checkbutton(
            preview_frame,
            text="Live Preview",
            variable=self.preview_var,
            command=self.toggle_preview,
            style="TCheckbutton",
        )
        self.preview_check.pack(side=tk.LEFT)

        # Create a shared button frame for both buttons
        button_frame = ttk.Frame(self.text_tab, style="TFrame")
        button_frame.grid(row=1, column=2, padx=(0, 14), pady=12, sticky=tk.W)

        # Add Favorites button to the shared frame
        self.fav_btn = ttk.Button(
            button_frame,
            text="★",
            width=3,
            command=self.toggle_favorite,
            style="Star.TButton",
        )
        self.fav_btn.pack(side=tk.LEFT, padx=(0, 5))

        # Add History button to the same shared frame
        self.history_btn = ttk.Menubutton(
            button_frame, text="📜 History", style="Action.TButton"
        )
        self.history_btn.pack(side=tk.LEFT, padx=0)

        # Create history menu with improved styling
        self.history_menu = tk.Menu(
            self.history_btn,
            tearoff=0,
            bg=self.entry_bg,
            fg=self.entry_fg,
            activebackground=self.selection_bg,
            activeforeground=self.text_color_ui,
            relief="flat",
            bd=1,
        )
        self.history_btn["menu"] = self.history_menu
        self.update_history_menu()

        # Font Controls with improved styling
        ttk.Label(self.text_tab, text="Art Font:").grid(
            row=1, column=0, padx=14, pady=12, sticky=tk.W
        )
        default_art_font = (
            "dos_rebel" if "dos_rebel" in self.figlet_fonts else self.figlet_fonts[0]
        )
        self.figlet_font = tk.StringVar(value=default_art_font)
        self.font_combo = ttk.Combobox(
            self.text_tab,
            textvariable=self.figlet_font,
            values=self.figlet_fonts,
            state="readonly",
            style="TCombobox",
            height=15,  # Show more items in dropdown
        )
        self.font_combo.grid(row=1, column=1, padx=14, pady=12, sticky=tk.EW)
        self.font_combo.bind("<<ComboboxSelected>>", lambda e: self.update_banner())

        # Favorites dropdown with improved styling
        ttk.Label(self.text_tab, text="Favorites:").grid(
            row=7, column=0, padx=14, pady=12, sticky=tk.W
        )
        self.favorites_var = tk.StringVar()
        self.favorites_combo = ttk.Combobox(
            self.text_tab,
            textvariable=self.favorites_var,
            state="readonly",
            style="TCombobox",
            height=10,
        )
        self.favorites_combo.grid(row=7, column=1, padx=14, pady=12, sticky=tk.EW)
        self.favorites_combo.bind("<<ComboboxSelected>>", self.apply_favorite_font)
        self.update_favorites_menu()

        # Enhanced Font Slider with Label
        ttk.Label(self.text_tab, text="Font Browser:").grid(
            row=2, column=0, padx=14, pady=12, sticky=tk.W
        )
        self.font_slider = ttk.Scale(
            self.text_tab,
            from_=0,
            to=len(self.figlet_fonts) - 1,
            command=lambda v: self.update_font_from_slider(),
            style="TScale",
        )
        self.font_slider.grid(row=2, column=1, padx=14, pady=12, sticky=tk.EW)
        self.font_slider_label = ttk.Label(
            self.text_tab,
            text=self.figlet_fonts[0],
            style="Primary.TLabel",
            font=("Segoe UI", 9, "italic"),
        )
        self.font_slider_label.grid(row=3, column=1, padx=14, sticky=tk.W)
        default_index = self.figlet_fonts.index(self.figlet_font.get())
        self.font_slider.set(default_index)
        self.font_slider_label.config(text=self.figlet_fonts[default_index])

        # Display Font with improved styling
        ttk.Label(self.text_tab, text="Display Font:").grid(
            row=4, column=0, padx=14, pady=12, sticky=tk.W
        )
        self.display_combo = ttk.Combobox(
            self.text_tab,
            textvariable=self.display_font,
            values=self.system_fonts,
            state="readonly",
            style="TCombobox",
            height=15,
        )
        self.display_combo.grid(row=4, column=1, padx=14, pady=12, sticky=tk.EW)
        self.display_combo.bind("<<ComboboxSelected>>", lambda e: self.update_banner())

        # Size Controls
        self.size_slider, self.size_label = self.create_slider_group(
            self.text_tab, "Font Size:", 6, 48, self.font_size, "{} pt", 5
        )

        # Width Controls
        self.font_width_slider, self.width_label = self.create_slider_group(
            self.text_tab, "Width Scale:", 0.5, 3.0, self.font_width, "{:.1f}x", 6
        )

        # Ensure text_tab row 1 column 1 can expand
        self.text_tab.grid_columnconfigure(1, weight=1)

    def create_slider_group(
        self, parent, label_text, from_, to, variable, format_str, row
    ):
        frame = ttk.Frame(parent, style="TFrame")
        frame.grid(row=row, column=0, columnspan=2, padx=12, pady=8, sticky="ew")

        ttk.Label(frame, text=label_text, font=("Segoe UI", 10)).pack(
            side=tk.LEFT, anchor="w"
        )

        value_label = ttk.Label(
            frame,
            text=format_str.format(variable.get()),
            width=8,
            anchor="e",
            style="Primary.TLabel",
        )
        value_label.pack(side=tk.RIGHT, padx=8)

        slider = ttk.Scale(
            frame,
            from_=from_,
            to=to,
            variable=variable,
            command=lambda v: [
                value_label.config(text=format_str.format(float(v))),
                self.schedule_banner_update(),
            ],
            style="TScale",
        )
        slider.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=8)

        return slider, value_label

    def create_style_tab(self):
        # Color Pickers with improved styling
        ttk.Label(self.style_tab, text="Text Color:").grid(
            row=0, column=0, padx=14, pady=14, sticky=tk.W
        )
        self.text_color_frame = ttk.Frame(self.style_tab, style="TFrame")
        self.text_color_frame.grid(row=0, column=1, padx=14, pady=14, sticky=tk.EW)
        ttk.Button(
            self.text_color_frame,
            text="Choose",
            command=self.choose_text_color,
            style="Action.TButton",
        ).pack(side=tk.LEFT)
        self.text_preview = tk.Canvas(
            self.text_color_frame,
            width=40,
            height=28,
            highlightthickness=1,
            highlightbackground=self.selection_bg,
            bg=self.text_color,
            bd=0,
        )
        self.text_preview.pack(side=tk.LEFT, padx=8)

        ttk.Label(self.style_tab, text="Background:").grid(
            row=1, column=0, padx=14, pady=14, sticky=tk.W
        )
        self.bg_color_frame = ttk.Frame(self.style_tab, style="TFrame")
        self.bg_color_frame.grid(row=1, column=1, padx=14, pady=14, sticky=tk.EW)
        ttk.Button(
            self.bg_color_frame,
            text="Choose",
            command=self.choose_bg_color,
            style="Action.TButton",
        ).pack(side=tk.LEFT)
        self.bg_preview = tk.Canvas(
            self.bg_color_frame,
            width=40,
            height=28,
            highlightthickness=1,
            highlightbackground=self.selection_bg,
            bg=self.bg_color,
            bd=0,
        )
        self.bg_preview.pack(side=tk.LEFT, padx=8)

        # Theme Grid with improved styling
        ttk.Label(self.style_tab, text="Preset Themes:").grid(
            row=2, column=0, padx=14, pady=14, sticky=tk.NW
        )

        theme_outer_frame = ttk.Frame(self.style_tab, style="TFrame")
        theme_outer_frame.grid(row=2, column=1, padx=14, pady=14, sticky=tk.EW)

        self.theme_frame = ttk.Frame(theme_outer_frame, style="TFrame")
        self.theme_frame.pack(fill=tk.BOTH, expand=True)

        # Configure the theme grid
        for i in range(3):
            self.theme_frame.grid_columnconfigure(i, weight=1)

        # Update theme button configuration with active indicator
        self.theme_buttons = []
        for i, (name, fg, bg, *_) in enumerate(self.themes):
            theme_style = f"Theme{i}.TButton"
            self.style.configure(
                theme_style,
                background=bg,
                foreground=fg,
                borderwidth=2,
                font=("Segoe UI", 9, "bold"),
            )

            theme_frame = ttk.Frame(self.theme_frame, style="TFrame")
            theme_frame.grid(row=i // 3, column=i % 3, padx=4, pady=4, sticky=tk.EW)

            # Create a container to hold both the button and the checkmark
            inner_frame = ttk.Frame(theme_frame, style="TFrame")
            inner_frame.pack(fill=tk.X, expand=True)

            btn = ttk.Button(
                inner_frame,
                text=name,
                command=lambda f=fg, b=bg, idx=i: self.apply_theme(f, b, idx),
                style=theme_style,
                padding=(8, 4),
            )
            btn.pack(fill=tk.X, expand=True, side=tk.LEFT)

            # Add check indicator with high contrast
            indicator = ttk.Label(
                inner_frame,
                text="✓",
                style="Primary.TLabel",
                font=("Segoe UI", 12, "bold"),
            )
            indicator.pack(side=tk.RIGHT, padx=5)

            # Set initial visibility - only show for active theme
            if i == self.current_theme_index:
                indicator.config(foreground="#FFFFFF")  # Bright white for visibility
            else:
                indicator.config(foreground=bg)  # Same as button background to hide it

            self.theme_buttons.append((btn, indicator))
        # Animation Controls with improved styling
        ttk.Separator(self.style_tab, orient=tk.HORIZONTAL).grid(
            row=3, column=0, columnspan=2, sticky=tk.EW, padx=14, pady=16
        )

        animation_title = ttk.Label(
            self.style_tab,
            text="Animation Controls",
            style="Primary.TLabel",
            font=("Segoe UI", 10, "bold"),
        )
        animation_title.grid(
            row=4, column=0, columnspan=2, padx=14, pady=(16, 8), sticky=tk.W
        )

        ttk.Label(self.style_tab, text="Animation:").grid(
            row=5, column=0, padx=14, pady=12, sticky=tk.W
        )

        animation_frame = ttk.Frame(self.style_tab, style="TFrame")
        animation_frame.grid(row=5, column=1, padx=14, pady=12, sticky=tk.EW)

        ttk.Label(animation_frame, text="Speed:").pack(side=tk.LEFT, padx=(0, 8))
        speed_slider = ttk.Scale(
            animation_frame,
            from_=0.1,
            to=2.0,
            variable=self.animation_speed,
            length=120,
            style="TScale",
        )
        speed_slider.pack(side=tk.LEFT, padx=8)

        speed_value = ttk.Label(
            animation_frame,
            text=f"{self.animation_speed.get():.1f}x",
            width=4,
            style="Primary.TLabel",
        )
        speed_value.pack(side=tk.LEFT, padx=(0, 8))

        # Update speed value when slider changes
        speed_slider.configure(
            command=lambda v: [
                speed_value.config(text=f"{float(v):.1f}x"),
                self.animation_speed.set(float(v)),
            ]
        )

        self.anim_btn = ttk.Button(
            animation_frame,
            text="▶️ Animate",
            command=self.toggle_animation,
            style="Anim.TButton",
        )
        self.anim_btn.pack(side=tk.LEFT, padx=8)

    def create_output_area(self):
        # Create styled output area with improved visuals
        output_frame_inner = ttk.Frame(
            self.output_frame, style="Primary.TFrame", padding=2
        )
        output_frame_inner.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        output_frame_inner.grid_rowconfigure(0, weight=1)
        output_frame_inner.grid_columnconfigure(0, weight=1)

        self.output_text = tk.Text(
            output_frame_inner,
            font=("Consolas", 12),
            wrap=tk.NONE,
            bg=self.bg_color,
            fg=self.text_color,
            padx=16,
            pady=16,
            spacing3=4,  # Line spacing
            insertbackground=self.text_color,
            selectbackground=self.selection_bg,
            selectforeground=self.text_color_ui,
            borderwidth=0,
            relief=tk.FLAT,
            highlightthickness=0,
            cursor="arrow",  # Use arrow cursor since it's more display-focused
        )
        self.output_text.grid(row=0, column=0, sticky="nsew")

        # Modern Scrollbars
        self.v_scroll = ttk.Scrollbar(self.output_frame, command=self.output_text.yview)
        self.v_scroll.grid(row=0, column=1, sticky="ns")
        self.h_scroll = ttk.Scrollbar(
            self.output_frame, orient=tk.HORIZONTAL, command=self.output_text.xview
        )
        self.h_scroll.grid(row=1, column=0, sticky="ew")
        self.output_text.config(
            yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set
        )

    def create_action_buttons(self):
        self.action_frame = ttk.Frame(self.control_frame, style="TFrame", padding=6)
        self.action_frame.pack(fill=tk.X, padx=12, pady=12)

        action_btns = [
            ("🔄 Generate", self.update_banner),
            ("📋 Copy", self.copy_to_clipboard),
            ("💾 Export", self.save_to_file),
        ]

        for text, cmd in action_btns:
            btn = ttk.Button(
                self.action_frame, text=text, command=cmd, style="Action.TButton"
            )
            btn.pack(side=tk.LEFT, expand=True, padx=6, fill=tk.X)

    def create_status_bar(self):
        self.status_bar = ttk.Label(
            self.main_frame, textvariable=self.status_var, style="Status.TLabel"
        )
        self.status_bar.grid(row=1, column=0, sticky="ew", padx=18, pady=6)

    def setup_keybindings(self):
        # Comprehensive Keyboard Controls
        self.root.bind("<Control-n>", self.cycle_theme)
        self.root.bind("<Control-N>", self.cycle_theme)
        self.root.bind("<Control-Up>", lambda e: self.adjust_slider(1, "font"))
        self.root.bind("<Control-Down>", lambda e: self.adjust_slider(-1, "font"))
        self.root.bind("<Alt-Up>", lambda e: self.adjust_slider(1, "size"))
        self.root.bind("<Alt-Down>", lambda e: self.adjust_slider(-1, "size"))
        self.root.bind("<Control-Shift-Up>", lambda e: self.adjust_slider(0.1, "width"))
        self.root.bind(
            "<Control-Shift-Down>", lambda e: self.adjust_slider(-0.1, "width")
        )

    def handle_slider_wheel(self, event):
        widget = event.widget
        # Handle different platforms
        delta = -1 if event.delta < 0 else 1

        if widget == self.font_slider:
            self.adjust_slider(delta, "font")
        elif widget == self.size_slider:
            self.adjust_slider(delta, "size")
        elif widget == self.font_width_slider:
            self.adjust_slider(delta * 0.1, "width")

    def setup_theme_cycling(self):
        self.current_theme_index = 0

    def cycle_theme(self, event=None):
        self.current_theme_index = (self.current_theme_index + 1) % len(self.themes)
        self.apply_theme_by_index(self.current_theme_index)
        name, _, _, _, _, _, _, _, _ = self.themes[self.current_theme_index]
        self.status_var.set(f"Active Theme: {name}")

    def adjust_slider(self, delta, slider_type):
        if slider_type == "font":
            current = self.font_slider.get()
            new_val = max(0, min(current + delta, len(self.figlet_fonts) - 1))
            self.font_slider.set(new_val)
            self.update_font_from_slider()
        elif slider_type == "size":
            current = self.font_size.get()
            new_val = max(6, min(current + delta, 48))
            self.font_size.set(new_val)
            self.size_label.config(text=f"{new_val} pt")
        elif slider_type == "width":
            current = self.font_width.get()
            new_val = max(0.5, min(current + delta, 3.0))
            self.font_width.set(new_val)
            self.width_label.config(text=f"{new_val:.1f}x")
        self.update_banner()

    def apply_initial_theme(self):
        self.apply_theme_by_index(0)

        # Add this to the apply_theme_by_index method or update it if it already exists:

    def apply_theme_by_index(self, index):
        """Apply theme by index, updating both UI and ASCII art colors"""
        (
            name,
            text_color,
            bg_color,
            secondary_bg,
            primary_bg,
            accent_color,
            text_color_ui,
            selection_bg,
            hover_bg,
        ) = self.themes[index]

        # Update all theme colors
        self.text_color = text_color
        self.bg_color = bg_color
        self.primary_bg = primary_bg
        self.secondary_bg = secondary_bg
        self.accent_color = accent_color
        self.text_color_ui = text_color_ui
        self.highlight_color = accent_color
        self.selection_bg = selection_bg
        self.entry_bg = primary_bg
        self.entry_fg = text_color_ui
        self.hover_bg = hover_bg

        # Apply to UI
        self.apply_styles()

        # Update color previews
        if hasattr(self, "text_preview"):
            self.text_preview.config(bg=self.text_color)
        if hasattr(self, "bg_preview"):
            self.bg_preview.config(bg=self.bg_color)

        # Update output area
        if hasattr(self, "output_text"):
            self.output_text.config(bg=self.bg_color, fg=self.text_color)

        # Update theme indicators
        if hasattr(self, "theme_buttons"):
            for i, (_, indicator) in enumerate(self.theme_buttons):
                if i == index:
                    indicator.config(
                        foreground="#FFFFFF"
                    )  # Bright white for visibility
                else:
                    # Hide by making same color as button background
                    theme_bg = self.themes[i][2]  # Get background color for this theme
                    indicator.config(foreground=theme_bg)
        # # Update theme-specific button styles
        # for i, (_, fg, bg, _, _, _, _, _, _) in enumerate(self.themes):
        #     if hasattr(self, "style"):
        #         self.style.configure(
        #             f"Theme{i}.TButton",
        #             background=bg,
        #             foreground=fg,
        #             borderwidth=2,
        #             font=("Segoe UI", 9, "bold"),
        #         )

        # Set current theme index
        self.current_theme_index = index
        # Update banner with new colors
        self.update_banner()

    def update_font_from_slider(self):
        try:
            index = int(self.font_slider.get())
            self.figlet_font.set(self.figlet_fonts[index])
            self.font_slider_label.config(text=self.figlet_fonts[index])
            # Update the favorite button state
            current_font = self.figlet_fonts[index]
            if hasattr(self, "fav_btn"):
                self.fav_btn.configure(
                    text="★" if current_font in self.favorite_fonts else "☆"
                )
            self.update_banner()
        except (IndexError, ValueError) as e:
            self.status_var.set(f"Font error: {str(e)}")

    def update_banner(self, event=None):
        if not hasattr(self, "output_text"):
            return
        if self.updating_banner:
            return
        self.updating_banner = True
        self.output_text.config(state=tk.NORMAL)
        try:
            current_font = self.figlet_font.get()
            width = int(80 * self.font_width.get())

            # Update favorite button state when banner updates
            if hasattr(self, "fav_btn"):
                self.fav_btn.configure(
                    text="★" if current_font in self.favorite_fonts else "☆"
                )

            # Use a try-except block for renderText
            try:
                fig = pyfiglet.Figlet(font=current_font, width=width)
                banner = fig.renderText(self.text_var.get())
            except Exception as e:
                # If rendering fails, fall back to standard font
                self.status_var.set(f"Error with font {current_font}, using standard")
                fig = pyfiglet.Figlet(font="standard", width=width)
                banner = fig.renderText(self.text_var.get())

            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, banner)

            # Make sure font exists and is valid
            try:
                self.output_text.config(
                    font=(self.display_font.get(), self.font_size.get()),
                    fg=self.text_color,
                    bg=self.bg_color,
                )
            except tk.TclError:
                # Fall back to a reliable font
                self.output_text.config(
                    font=("Courier", self.font_size.get()),
                    fg=self.text_color,
                    bg=self.bg_color,
                )

            status_text = (
                f"Rendered: {current_font} | Size: {self.font_size.get()}pt | "
                f"Width: {self.font_width.get():.1f}x | Chars: {len(banner)}"
            )
            self.status_var.set(status_text)

            # After successful rendering, add to history
            self.add_to_history(self.text_var.get())

        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
        finally:
            self.output_text.config(state=tk.DISABLED)
            self.updating_banner = False
            if hasattr(self, "_update_job"):
                self.root.after_cancel(self._update_job)
                del self._update_job

    def schedule_banner_update(self):
        if hasattr(self, "_update_job"):
            self.root.after_cancel(self._update_job)
        self._update_job = self.root.after(300, self.update_banner)

    def choose_text_color(self):
        """Handle text color selection"""
        color = colorchooser.askcolor(
            title="Choose Text Color", initialcolor=self.text_color
        )
        if color[1]:
            self.text_color = color[1]
            self.text_preview.config(bg=self.text_color)
            self.update_banner()

            # Give feedback in status bar
            self.status_var.set(f"Text color updated to {self.text_color}")

    def choose_bg_color(self):
        """Handle background color selection"""
        color = colorchooser.askcolor(
            title="Choose Background Color", initialcolor=self.bg_color
        )
        if color[1]:
            self.bg_color = color[1]
            self.bg_preview.config(bg=self.bg_color)
            self.update_banner()

            # Give feedback in status bar
            self.status_var.set(f"Background color updated to {self.bg_color}")

    def apply_theme(self, text_color, bg_color, index=None):
        """Apply selected theme colors (legacy method - forwards to apply_theme_by_index)"""
        if index is not None:
            self.apply_theme_by_index(index)
        else:
            # Create a custom theme based on current settings but with new text/bg colors
            custom_theme = list(self.themes[self.current_theme_index])
            custom_theme[1] = text_color  # Update text color
            custom_theme[2] = bg_color  # Update bg color

            # Apply just the text/bg color changes
            self.text_color = text_color
            self.bg_color = bg_color

            # Update visual elements
            if hasattr(self, "text_preview"):
                self.text_preview.config(bg=text_color)
            if hasattr(self, "bg_preview"):
                self.bg_preview.config(bg=bg_color)
            if hasattr(self, "output_text"):
                self.output_text.config(bg=bg_color, fg=text_color)

    def copy_to_clipboard(self):
        """Copy ASCII art to clipboard"""
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.output_text.get(1.0, tk.END))
            self.status_var.set("Copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Clipboard Error", f"Failed to copy:\n{str(e)}")

    def save_to_file(self):
        """Save ASCII art to file"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            )
            if filename:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(self.output_text.get(1.0, tk.END))
                self.status_var.set(f"Saved to {filename}")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save:\n{str(e)}")

    def load_favorites(self):
        """Load favorite fonts from a config file"""
        try:
            if os.path.exists("ascii_favorites.txt"):
                with open("ascii_favorites.txt", "r") as f:
                    self.favorite_fonts = [
                        line.strip() for line in f if line.strip() in self.figlet_fonts
                    ]
        except Exception as e:
            print(f"Could not load favorites: {e}")
            self.favorite_fonts = []

    def save_favorites(self):
        """Save favorite fonts to a config file"""
        try:
            with open("ascii_favorites.txt", "w") as f:
                for font in self.favorite_fonts:
                    f.write(f"{font}\n")
        except Exception as e:
            print(f"Could not save favorites: {e}")
            messagebox.showerror("Save Error", f"Failed to save favorites:\n{str(e)}")

    def toggle_favorite(self):
        """Toggle current font as favorite"""
        current_font = self.figlet_font.get()
        if current_font in self.favorite_fonts:
            self.favorite_fonts.remove(current_font)
            self.status_var.set(f"Removed '{current_font}' from favorites")
            self.fav_btn.configure(text="☆")
        else:
            self.favorite_fonts.append(current_font)
            self.status_var.set(f"Added '{current_font}' to favorites")
            self.fav_btn.configure(text="★")
        self.save_favorites()
        self.update_favorites_menu()

    def update_favorites_menu(self):
        """Update the favorites dropdown menu"""
        if hasattr(self, "favorites_combo"):
            self.favorites_combo["values"] = (
                sorted(self.favorite_fonts)
                if self.favorite_fonts
                else ["No favorites yet"]
            )

            # Update star button state
            current_font = self.figlet_font.get()
            if hasattr(self, "fav_btn"):
                self.fav_btn.configure(
                    text="★" if current_font in self.favorite_fonts else "☆"
                )

    def apply_favorite_font(self, event=None):
        """Apply selected favorite font"""
        selected = self.favorites_var.get()
        if selected and selected != "No favorites yet":
            self.figlet_font.set(selected)
            # Find the index of the font and update the slider
            if selected in self.figlet_fonts:
                index = self.figlet_fonts.index(selected)
                self.font_slider.set(index)
                self.font_slider_label.config(text=selected)
            self.update_banner()

    def toggle_preview(self):
        """Toggle live preview feature"""
        if self.preview_var.get():
            self.text_entry.bind("<KeyRelease>", lambda e: self.update_banner())
            self.status_var.set("Live preview enabled")
        else:
            self.text_entry.unbind("<KeyRelease>")
            self.status_var.set("Live preview disabled")

    def toggle_animation(self):
        """Toggle animation on/off"""
        if not self.animating:
            self.start_animation()
        else:
            self.stop_animation()

    def start_animation(self):
        """Start the animation sequence"""
        if self.animating:
            return

        self.animating = True
        self.anim_btn.config(text="⏹️ Stop", style="Action.TButton")

        # Disable other controls during animation
        self.text_entry.config(state=tk.DISABLED)
        self.font_combo.config(state=tk.DISABLED)
        self.font_slider.config(state=tk.DISABLED)

        # Start animation in a separate thread
        self.animation_thread = threading.Thread(target=self.run_animation)
        self.animation_thread.daemon = True
        self.animation_thread.start()

    def stop_animation(self):
        """Stop the animation sequence"""
        self.animating = False
        self.anim_btn.config(text="▶️ Animate", style="Anim.TButton")

        # Re-enable controls
        self.text_entry.config(state=tk.NORMAL)
        self.font_combo.config(state="readonly")
        self.font_slider.config(state=tk.NORMAL)

    def run_animation(self):
        """Run the animation loop"""
        original_text = self.text_var.get()
        original_font = self.figlet_font.get()

        try:
            # First animation: Text typing effect
            self.status_var.set("Animation: Text typing effect")
            for i in range(1, len(original_text) + 1):
                if not self.animating:
                    break
                self.text_var.set(original_text[:i])
                self.update_banner()
                time.sleep(self.animation_speed.get() / 2)

            time.sleep(self.animation_speed.get() * 2)

            # Second animation: Font cycling
            if self.animating:
                self.status_var.set("Animation: Font cycling effect")
                fonts_to_cycle = (
                    self.figlet_fonts[:20]
                    if len(self.figlet_fonts) > 20
                    else self.figlet_fonts
                )
                for font in fonts_to_cycle:
                    if not self.animating:
                        break
                    self.figlet_font.set(font)
                    index = self.figlet_fonts.index(font)
                    self.font_slider.set(index)
                    self.font_slider_label.config(text=font)
                    self.update_banner()
                    time.sleep(self.animation_speed.get())

            # Reset to original settings
            if self.animating:
                self.text_var.set(original_text)
                self.figlet_font.set(original_font)
                index = self.figlet_fonts.index(original_font)
                self.font_slider.set(index)
                self.font_slider_label.config(text=original_font)
                self.update_banner()

        except Exception as e:
            self.status_var.set(f"Animation error: {str(e)}")
        finally:
            # Always reset UI state when done
            self.root.after(0, self.stop_animation)

    def add_to_history(self, text):
        """Add text to history, avoid duplicates"""
        if text and text not in self.text_history:
            self.text_history.insert(0, text)
            if len(self.text_history) > self.max_history:
                self.text_history.pop()
            self.update_history_menu()

    def update_history_menu(self):
        """Update the history dropdown menu"""
        if hasattr(self, "history_menu"):
            self.history_menu.delete(0, tk.END)
            if not self.text_history:
                self.history_menu.add_command(label="No history yet", state=tk.DISABLED)
            else:
                for text in self.text_history:
                    # Truncate long texts for the menu
                    display_text = text if len(text) < 30 else text[:27] + "..."
                    self.history_menu.add_command(
                        label=display_text,
                        command=lambda t=text: self.load_history_item(t),
                    )

    def load_history_item(self, text):
        """Load a history item into the text entry"""
        self.text_var.set(text)
        self.update_banner()

    def create_footer(self):
        # Create a dedicated footer frame at the bottom of main_frame
        footer_frame = ttk.Frame(self.main_frame)
        footer_frame.grid(row=1, column=0, sticky="ew", padx=18, pady=6)

        # Configure three equally weighted columns
        footer_frame.columnconfigure(0, weight=1)
        # footer_frame.columnconfigure(0, weight=1)

        made_label = ttk.Label(
            footer_frame,
            text="       Made by nav9v🏄\nCopyright ©CC 2025 - 2049",
            style="Footer.TLabel",
            anchor="center",
        )
        made_label.grid(row=0, column=0, sticky="ew")
        made_label.bind(
            "<Button-1>", lambda e: webbrowser.open("https://github.com/nav9v/")
        )


if __name__ == "__main__":
    try:
        from ttkthemes import ThemedTk

        root = ThemedTk(theme="arc")
        # Don't set background color here, it will be set by the theme system

    except Exception as e:
        root = tk.Tk()
        messagebox.showinfo(
            "Tip", "For best experience, install ttkthemes: pip install ttkthemes"
        )

    app = ASCIIArtStudio(root)
    root.mainloop()
