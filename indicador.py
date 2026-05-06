import datetime
import subprocess
import tkinter as tk
from tkinter import messagebox

RAW_MAX = 2**15 - 1
APP_VERSION = "1.1"
APP_AUTHOR = "Mauricio Menon"
APP_GITHUB = "https://github.com/mauriciomenon/RawCountsBIASscale"
APP_DESCRIPTION = "Analog point calculator between SCADA systems and RTUs"
DEFAULT_LIM_INF = 4.0
DEFAULT_LIM_SUP = 20.0
DEFAULT_RAN_INF = 0.0
DEFAULT_RAN_SUP = 10.0
DEFAULT_PONTEIRO = 5.0
CANVAS_WIDTH = 360
CANVAS_HEIGHT = 120
CANVAS_LEFT = 60
CANVAS_RIGHT = 8
CANVAS_TOP = 8
CANVAS_BOTTOM = 8
LEGEND_LINES = 4
LEGEND_HEIGHT = 68
LEGEND_WIDTH = 300
LEGEND_LABEL_X = 2
LEGEND_DOT_X = 76
LEGEND_RAW_LABEL_X = 88
LEGEND_RAW_VALUE_X = 152
LEGEND_SEPARATOR_X = 160
LEGEND_VALUE_LABEL_X = 172
LEGEND_VALUE_X = 220
POINT_COLORS = {
    "x=0": "#1f77b4",
    "x=max": "#17becf",
    "y=0": "#2ca02c",
    "y=min": "#9467bd",
    "y=max": "#ff7f0e",
    "medido": "#d62728",
}
POINT_LABEL_KEYS = {
    "x=0": "point_min",
    "x=max": "point_max",
    "y=0": "point_zero",
    "y=min": "point_ymin",
    "y=max": "point_ymax",
    "medido": "point_measured",
}
TEXTOS = {
    "pt": {
        "title": "SCADA: Raw Counts & BIAS/SCALE",
        "amp_frame": "Valores de Corrente do Transdutor (mA)",
        "lim_inf": "Limite inferior",
        "lim_sup": "Limite superior",
        "scale_frame": "Escala de Grandeza do Equipamento Primario",
        "ran_inf": "Range inferior",
        "ran_sup": "Range superior",
        "ponteiro": "Valor medido",
        "scada_frame": "Resultado SCADA",
        "bias": "BIAS",
        "scale": "SCALE",
        "utr_frame": "Resultado UTR",
        "valor_ma": "Valor (mA)",
        "int_16": "INT (16 bits)",
        "hex_16": "HEXA (16 bits)",
        "graph_frame": "Grafico BIAS/SCALE",
        "calculate": "Calcular",
        "about": "Sobre",
        "language_button": "EN",
        "about_title": "Sobre",
        "about_description": "Calculadora de pontos analogicos entre sistemas SCADA e RTUs",
        "about_author": "Autor",
        "about_version": "Versao",
        "about_commit": "Commit",
        "about_date": "Data",
        "legend_value": "valor=",
        "error_title": "Erro",
        "error_numeric": "Informe apenas valores numericos",
        "range_physical_zero": "Range fisico nao pode ser zero",
        "current_range_zero": "Range de corrente nao pode ser zero",
        "upper_limit_zero": "Limite superior nao pode ser zero",
        "pointer_out_of_range": "Ponteiro fora do range fisico",
        "graph_scale_zero": "Escala do grafico nao pode ser zero",
        "point_min": "(x,y) min",
        "point_max": "(x,y) max",
        "point_zero": "(x,y) zero",
        "point_ymin": "(x,y) ymin",
        "point_ymax": "(x,y) ymax",
        "point_measured": "(x,y) med",
    },
    "en": {
        "title": "SCADA: Raw Counts & BIAS/SCALE",
        "amp_frame": "Transducer Current Values (mA)",
        "lim_inf": "Lower limit",
        "lim_sup": "Upper limit",
        "scale_frame": "Primary Equipment Engineering Scale",
        "ran_inf": "Lower range",
        "ran_sup": "Upper range",
        "ponteiro": "Measured value",
        "scada_frame": "SCADA Result",
        "bias": "BIAS",
        "scale": "SCALE",
        "utr_frame": "RTU Result",
        "valor_ma": "Value (mA)",
        "int_16": "INT (16 bits)",
        "hex_16": "HEX (16 bits)",
        "graph_frame": "BIAS/SCALE Graph",
        "calculate": "Calculate",
        "about": "About",
        "language_button": "PT",
        "about_title": "About",
        "about_description": "Analog point calculator between SCADA systems and RTUs",
        "about_author": "Author",
        "about_version": "Version",
        "about_commit": "Commit",
        "about_date": "Date",
        "legend_value": "value=",
        "error_title": "Error",
        "error_numeric": "Enter numeric values only",
        "range_physical_zero": "Physical range cannot be zero",
        "current_range_zero": "Current range cannot be zero",
        "upper_limit_zero": "Upper limit cannot be zero",
        "pointer_out_of_range": "Pointer is outside the physical range",
        "graph_scale_zero": "Graph scale cannot be zero",
        "point_min": "(x,y) min",
        "point_max": "(x,y) max",
        "point_zero": "(x,y) zero",
        "point_ymin": "(x,y) ymin",
        "point_ymax": "(x,y) ymax",
        "point_measured": "(x,y) meas",
    },
}
FORM_LABEL_MIN_WIDTH = 145
VALUE_COLUMN_WIDTH = 24
FIELD_PAD_X = 12
INPUT_INNER_BD = 0
FRAME_PADY = (6, 0)


def configurar_colunas(frame):
    frame.grid_columnconfigure(0, minsize=FORM_LABEL_MIN_WIDTH)
    frame.grid_columnconfigure(1, weight=0)


def criar_saida_valor(parent):
    return tk.Label(
        parent,
        text="--",
        anchor=tk.W,
        width=VALUE_COLUMN_WIDTH,
        relief="solid",
        bd=1,
        padx=FIELD_PAD_X,
        highlightbackground="white",
        highlightthickness=1,
    )


def criar_campo_entrada(parent, textvariable):
    input_frame = tk.Frame(parent, relief="solid", bd=1, highlightbackground="white", highlightthickness=1)
    input_widget = tk.Entry(
        input_frame,
        textvariable=textvariable,
        width=VALUE_COLUMN_WIDTH,
        relief="flat",
        bd=INPUT_INNER_BD,
        highlightthickness=0,
    )
    input_frame.configure(background=input_widget.cget("background"))
    input_widget.pack(fill="x", padx=FIELD_PAD_X)
    return input_frame


def commit_atual():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


class ErroCalculo(ValueError):
    chave = "calculation_error"


class RangeFisicoZero(ErroCalculo):
    chave = "range_physical_zero"


class RangeCorrenteZero(ErroCalculo):
    chave = "current_range_zero"


class LimiteSuperiorZero(ErroCalculo):
    chave = "upper_limit_zero"


class PonteiroForaDoRange(ErroCalculo):
    chave = "pointer_out_of_range"


class EscalaGraficoZero(ErroCalculo):
    chave = "graph_scale_zero"


def formatar_hex_16(raw_int16):
    return f"0x{raw_int16 & 0xFFFF:04X}"


def calcular_valores(lim_inf, lim_sup, ran_inf, ran_sup, ponteiro):
    f_lim = lim_sup - lim_inf
    f_ran = ran_sup - ran_inf
    if f_ran == 0:
        raise RangeFisicoZero
    if f_lim == 0:
        raise RangeCorrenteZero
    if lim_sup == 0:
        raise LimiteSuperiorZero
    ran_min = min(ran_inf, ran_sup)
    ran_max = max(ran_inf, ran_sup)
    if not (ran_min <= ponteiro <= ran_max):
        raise PonteiroForaDoRange

    corrente = ((ponteiro - ran_inf) * f_lim / f_ran) + lim_inf
    scale_calc = lim_sup * f_ran / f_lim
    bias_calc = ran_sup - scale_calc
    raw_int16 = max(0, min(RAW_MAX, int((corrente / lim_sup) * RAW_MAX)))
    return corrente, bias_calc, scale_calc, raw_int16


def limites_grafico(bias_val, scale_val):
    graph_upper = bias_val + scale_val
    graph_min = min(0, bias_val, graph_upper)
    graph_max = max(0, bias_val, graph_upper)
    if graph_min == graph_max:
        raise EscalaGraficoZero
    graph_tick = abs(graph_max - graph_min) / 4 or 1
    return graph_min, graph_max, graph_tick


def y_para_px(
    valor_y,
    y_min,
    y_max,
    height=CANVAS_HEIGHT,
    top=CANVAS_TOP,
    bottom=CANVAS_BOTTOM,
):
    if y_max == y_min:
        return height / 2
    return height - bottom - ((valor_y - y_min) / (y_max - y_min)) * (height - top - bottom)


def desenhar_eixos(canvas, y_min, y_max):
    canvas.create_line(CANVAS_LEFT, CANVAS_TOP, CANVAS_LEFT, CANVAS_HEIGHT - CANVAS_BOTTOM, fill="#444")
    canvas.create_line(CANVAS_LEFT, CANVAS_HEIGHT - CANVAS_BOTTOM, CANVAS_WIDTH - CANVAS_RIGHT, CANVAS_HEIGHT - CANVAS_BOTTOM, fill="#444")
    if y_max == y_min:
        return
    passo_y = (CANVAS_HEIGHT - CANVAS_TOP - CANVAS_BOTTOM) / 4
    valor_passo = (y_max - y_min) / 4
    for i in range(5):
        y_px = CANVAS_TOP + i * passo_y
        valor = y_max - i * valor_passo
        canvas.create_line(CANVAS_LEFT, y_px, CANVAS_WIDTH - CANVAS_RIGHT, y_px, fill="#ddd")
        canvas.create_text(CANVAS_LEFT - 4, y_px, text=f"{valor:.2f}", anchor="e", font=("Arial", 8))


def x_para_px(raw_val, width=CANVAS_WIDTH, left=CANVAS_LEFT, right=CANVAS_RIGHT):
    return left + (raw_val / RAW_MAX) * (width - left - right)


def coletar_pontos_analise(bias_val, escala_val, y_min, y_max, ponto_raw):
    pontos = []

    def ponto_de_raw(raw_val):
        y_val = bias_val + (escala_val * raw_val / RAW_MAX)
        return raw_val, y_val

    pontos.append(("x=0", *ponto_de_raw(0)))
    pontos.append(("x=max", *ponto_de_raw(RAW_MAX)))

    if escala_val != 0:
        raw_zero = (-bias_val * RAW_MAX) / escala_val
        if 0 <= raw_zero <= RAW_MAX:
            pontos.append(("y=0", *ponto_de_raw(raw_zero)))
        for valor_ref, tag in ((y_min, "y=min"), (y_max, "y=max")):
            raw_ref = ((valor_ref - bias_val) * RAW_MAX) / escala_val
            if 0 <= raw_ref <= RAW_MAX:
                pontos.append((tag, *ponto_de_raw(raw_ref)))

    if ponto_raw is not None:
        pontos.append(("medido", *ponto_de_raw(ponto_raw)))

    pontos_unicos = {}
    for label, raw_val, y_val in pontos:
        chave = round(raw_val)
        if chave not in pontos_unicos or label == "medido":
            pontos_unicos[chave] = (label, raw_val, y_val)

    return list(pontos_unicos.values())


def desenhar_pontos_analise(canvas, pontos_analise, y_min, y_max):
    canvas.delete("all")
    desenhar_eixos(canvas, y_min, y_max)
    width = canvas.winfo_reqwidth()
    height = canvas.winfo_reqheight()
    for label, raw_val, y_val in pontos_analise:
        raio = 4
        cor = POINT_COLORS.get(label, "#444444")
        x_px = x_para_px(raw_val, width=width)
        y_px = y_para_px(y_val, y_min, y_max, height=height)
        canvas.create_oval(x_px - raio, y_px - raio, x_px + raio, y_px + raio, fill=cor, outline="")


def atualizar_legenda(canvas, pontos_analise, y_min, y_max, textos):
    canvas.delete("all")
    canvas.create_line(0, 1, LEGEND_WIDTH, 1, fill="#8a8a8a")
    linhas = list(pontos_analise)
    if any(label == "medido" for label, _, _ in linhas):
        item_raw = next(item for item in linhas if item[0] == "medido")
        outras = [item for item in linhas if item[0] != "medido"]
        linhas = outras[:3] + [item_raw]
    for idx, (label, raw_val, y_val) in enumerate(linhas[:LEGEND_LINES]):
        cor = POINT_COLORS.get(label, "#444444")
        if 0 <= raw_val <= RAW_MAX and y_min <= y_val <= y_max:
            raw_texto = str(int(round(raw_val)))
        else:
            raw_texto = f"{raw_val:.2f}"
        label_key = POINT_LABEL_KEYS.get(label)
        label_texto = textos.get(label_key, label)
        valor_texto = f"{y_val:.3f}"
        y_px = 14 + idx * 14
        canvas.create_text(LEGEND_LABEL_X, y_px, text=label_texto, anchor="w", font=("Consolas", 7))
        canvas.create_oval(LEGEND_DOT_X - 4, y_px - 4, LEGEND_DOT_X + 4, y_px + 4, fill=cor, outline="")
        canvas.create_text(LEGEND_RAW_LABEL_X, y_px, text="raw=", anchor="w", font=("Consolas", 7))
        canvas.create_text(LEGEND_RAW_VALUE_X, y_px, text=raw_texto, anchor="e", font=("Consolas", 7))
        canvas.create_text(LEGEND_SEPARATOR_X, y_px, text="|", anchor="center", font=("Consolas", 7))
        canvas.create_text(LEGEND_VALUE_LABEL_X, y_px, text=textos["legend_value"], anchor="w", font=("Consolas", 7))
        canvas.create_text(LEGEND_VALUE_X, y_px, text=valor_texto, anchor="w", font=("Consolas", 7))


class RegistroIdioma:
    def __init__(self, idioma="pt"):
        self.idioma = idioma
        self.frame_widgets = {}
        self.text_widgets = {}

    def textos(self):
        return TEXTOS[self.idioma]

    def texto(self, chave):
        return self.textos()[chave]

    def registrar_frame(self, chave, widget):
        self.frame_widgets[chave] = widget
        return widget

    def registrar_texto(self, chave, widget):
        self.text_widgets[chave] = widget
        return widget

    def trocar(self):
        self.idioma = "en" if self.idioma == "pt" else "pt"

    def aplicar(self, app, b_calcular, b_about, b_idioma):
        textos = self.textos()
        app.title(textos["title"])
        for chave, widget in self.frame_widgets.items():
            widget.configure(text=textos[chave])
        for chave, widget in self.text_widgets.items():
            widget.configure(text=textos[chave])
        b_calcular.configure(text=textos["calculate"])
        b_about.configure(text=textos["about"])
        b_idioma.configure(text=textos["language_button"])


def mostrar_about(app, textos):
    janela_about = tk.Toplevel(app)
    janela_about.title(textos["about_title"])
    janela_about.resizable(False, False)
    janela_about.transient(app)
    janela_about.grab_set()

    frame_about = tk.Frame(janela_about, padx=16, pady=14)
    frame_about.pack(fill="both", expand=True)

    tk.Label(frame_about, text=textos["about_description"], anchor=tk.W, justify="left").pack(fill="x")
    tk.Label(frame_about, text=f"{textos['about_author']}: {APP_AUTHOR}", anchor=tk.W).pack(fill="x", pady=(10, 0))
    tk.Label(frame_about, text=f"{textos['about_version']}: {APP_VERSION}", anchor=tk.W).pack(fill="x")
    tk.Label(frame_about, text=f"{textos['about_commit']}: {commit_atual()}", anchor=tk.W).pack(fill="x")
    tk.Label(frame_about, text=f"{textos['about_date']}: {datetime.date.today().isoformat()}", anchor=tk.W).pack(fill="x")
    tk.Label(frame_about, text=f"GitHub: {APP_GITHUB}", anchor=tk.W).pack(fill="x", pady=(0, 10))
    tk.Button(frame_about, text="OK", width=8, command=janela_about.destroy).pack(anchor="center")

    janela_about.update_idletasks()
    x_pos = app.winfo_rootx() + (app.winfo_width() - janela_about.winfo_width()) // 2
    y_pos = app.winfo_rooty() + (app.winfo_height() - janela_about.winfo_height()) // 2
    janela_about.geometry(f"+{x_pos}+{y_pos}")
    return "break"


class IndicadorApp:
    def __init__(self):
        self.localizacao = RegistroIdioma()
        self.graph_min = 0
        self.graph_max = 0
        self.pontos_analise = []

        self.app = tk.Tk()
        self.content_frame = tk.Frame(self.app, padx=8, pady=8, highlightbackground="white", highlightthickness=1)
        self.content_frame.pack(padx=8, pady=(8, 6))

        _, self.bias_inicial, self.scale_inicial, self.raw_inicial = calcular_valores(
            DEFAULT_LIM_INF,
            DEFAULT_LIM_SUP,
            DEFAULT_RAN_INF,
            DEFAULT_RAN_SUP,
            DEFAULT_PONTEIRO,
        )

        self.criar_campos_entrada()
        self.criar_resultados()
        self.criar_grafico()
        self.criar_rodape()
        self.aplicar_idioma()
        self.app.bind_all("<Return>", lambda _event: self.acionar())

    def textos(self):
        return self.localizacao.textos()

    def texto(self, chave):
        return self.localizacao.texto(chave)

    def registrar_frame(self, chave, widget):
        return self.localizacao.registrar_frame(chave, widget)

    def registrar_texto(self, chave, widget):
        return self.localizacao.registrar_texto(chave, widget)

    def criar_campos_entrada(self):
        amp_frame = self.registrar_frame("amp_frame", tk.LabelFrame(
            self.content_frame,
            padx=10,
            pady=5,
        ))
        amp_frame.pack(fill="x", pady=FRAME_PADY)
        configurar_colunas(amp_frame)

        self.ptr_e_lim_inf = tk.StringVar(value="4")
        self.ptr_e_lim_sup = tk.StringVar(value="20")

        self.registrar_texto("lim_inf", tk.Label(amp_frame, anchor=tk.W)).grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.registrar_texto("lim_sup", tk.Label(amp_frame, anchor=tk.W)).grid(row=1, column=0, sticky=(tk.W, tk.E))
        criar_campo_entrada(amp_frame, self.ptr_e_lim_inf).grid(row=0, column=1, sticky=tk.W)
        criar_campo_entrada(amp_frame, self.ptr_e_lim_sup).grid(row=1, column=1, sticky=tk.W)

        scale_frame = self.registrar_frame("scale_frame", tk.LabelFrame(
            self.content_frame,
            padx=10,
            pady=5,
        ))
        scale_frame.pack(fill="x", pady=FRAME_PADY)
        configurar_colunas(scale_frame)

        self.ptr_e_ran_inf = tk.StringVar(value="0")
        self.ptr_e_ran_sup = tk.StringVar(value="10")
        self.ptr_e_ponteiro = tk.StringVar(value="5")

        self.registrar_texto("ran_inf", tk.Label(scale_frame, anchor=tk.W)).grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.registrar_texto("ran_sup", tk.Label(scale_frame, anchor=tk.W)).grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.registrar_texto("ponteiro", tk.Label(scale_frame, anchor=tk.W)).grid(row=2, column=0, sticky=(tk.W, tk.E))
        criar_campo_entrada(scale_frame, self.ptr_e_ran_inf).grid(row=0, column=1, sticky=tk.W)
        criar_campo_entrada(scale_frame, self.ptr_e_ran_sup).grid(row=1, column=1, sticky=tk.W)
        criar_campo_entrada(scale_frame, self.ptr_e_ponteiro).grid(row=2, column=1, sticky=tk.W)

    def criar_resultados(self):
        return_frame = self.registrar_frame(
            "scada_frame",
            tk.LabelFrame(self.content_frame, padx=10, pady=5),
        )
        return_frame.pack(fill="x", pady=FRAME_PADY)
        configurar_colunas(return_frame)

        self.l_cal_bias_val = criar_saida_valor(return_frame)
        self.l_cal_scale_val = criar_saida_valor(return_frame)
        self.registrar_texto("bias", tk.Label(return_frame, anchor=tk.W)).grid(
            row=1,
            column=0,
            sticky=(tk.W, tk.E),
        )
        self.l_cal_bias_val.grid(row=1, column=1, sticky=tk.W)
        self.registrar_texto("scale", tk.Label(return_frame, anchor=tk.W)).grid(
            row=2,
            column=0,
            sticky=(tk.W, tk.E),
        )
        self.l_cal_scale_val.grid(row=2, column=1, sticky=tk.W)

        return_frame_utr = self.registrar_frame(
            "utr_frame",
            tk.LabelFrame(self.content_frame, padx=10, pady=5),
        )
        return_frame_utr.pack(fill="x", pady=FRAME_PADY)
        configurar_colunas(return_frame_utr)

        self.l_cal_val = criar_saida_valor(return_frame_utr)
        self.l_cal_val_int = criar_saida_valor(return_frame_utr)
        self.l_cal_val_hex = criar_saida_valor(return_frame_utr)
        self.registrar_texto("valor_ma", tk.Label(return_frame_utr, anchor=tk.W)).grid(
            row=0,
            column=0,
            sticky=(tk.W, tk.E),
        )
        self.l_cal_val.grid(row=0, column=1, sticky=tk.W)
        self.registrar_texto("int_16", tk.Label(return_frame_utr, anchor=tk.W)).grid(
            row=1,
            column=0,
            sticky=(tk.W, tk.E),
        )
        self.l_cal_val_int.grid(row=1, column=1, sticky=tk.W)
        self.registrar_texto("hex_16", tk.Label(return_frame_utr, anchor=tk.W)).grid(
            row=2,
            column=0,
            sticky=(tk.W, tk.E),
        )
        self.l_cal_val_hex.grid(row=2, column=1, sticky=tk.W)

    def criar_grafico(self):
        graph_frame = self.registrar_frame(
            "graph_frame",
            tk.LabelFrame(self.content_frame, padx=10, pady=5),
        )
        self.bias_graph = tk.Canvas(graph_frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, highlightthickness=0)
        self.bias_graph.grid(row=0, column=0, sticky="w")
        self.legend_canvas = tk.Canvas(graph_frame, width=LEGEND_WIDTH, height=LEGEND_HEIGHT, highlightthickness=0)
        self.legend_canvas.grid(row=1, column=0, sticky="w", padx=CANVAS_LEFT, pady=(0, 0))

        self.plotar(self.bias_inicial, self.scale_inicial, self.raw_inicial)
        graph_frame.pack(fill="x", pady=FRAME_PADY)

    def criar_rodape(self):
        footer_frame = tk.Frame(self.content_frame, height=34)
        footer_frame.pack(fill="x", pady=(8, 2))
        footer_frame.pack_propagate(False)

        self.b_idioma = tk.Button(
            footer_frame,
            width=4,
            command=self.trocar_idioma,
            font=("Arial", 7),
            padx=1,
            pady=1,
            anchor="center",
        )
        self.b_idioma.place(relx=0.02, rely=0.5, anchor="w")

        self.b_calcular = tk.Button(footer_frame, width=7, command=self.acionar, font=("Arial", 10))
        self.b_calcular.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
        )
        self.b_about = tk.Button(
            footer_frame,
            width=4,
            command=self.about,
            font=("Arial", 7),
            padx=1,
            pady=1,
            anchor="center",
        )
        self.b_about.place(relx=0.98, rely=0.5, anchor="e")

    def aplicar_idioma(self):
        textos = self.textos()
        self.localizacao.aplicar(self.app, self.b_calcular, self.b_about, self.b_idioma)
        if self.pontos_analise:
            atualizar_legenda(self.legend_canvas, self.pontos_analise, self.graph_min, self.graph_max, textos)

    def trocar_idioma(self):
        self.localizacao.trocar()
        self.aplicar_idioma()
        return "break"

    def ler_valores_entrada(self):
        return (
            float(self.ptr_e_lim_inf.get()),
            float(self.ptr_e_lim_sup.get()),
            float(self.ptr_e_ran_inf.get()),
            float(self.ptr_e_ran_sup.get()),
            float(self.ptr_e_ponteiro.get()),
        )

    def limpar_resultados(self):
        self.l_cal_val["text"] = "--"
        self.l_cal_bias_val["text"] = "--"
        self.l_cal_scale_val["text"] = "--"
        self.l_cal_val_int["text"] = "--"
        self.l_cal_val_hex["text"] = "--"

    def exibir_resultado(self, resultado):
        corrente, bias_calc, scale_calc, raw_calc = resultado
        self.l_cal_val["text"] = str(corrente)
        self.l_cal_bias_val["text"] = str(bias_calc)
        self.l_cal_scale_val["text"] = str(scale_calc)
        self.l_cal_val_int["text"] = str(raw_calc)
        self.l_cal_val_hex["text"] = formatar_hex_16(raw_calc)

    def calcular(self):
        try:
            valores_entrada = self.ler_valores_entrada()
        except ValueError:
            self.limpar_resultados()
            messagebox.showerror(self.texto("error_title"), self.texto("error_numeric"))
            return None

        try:
            resultado = calcular_valores(*valores_entrada)
        except ErroCalculo as exc:
            self.limpar_resultados()
            messagebox.showerror(self.texto("error_title"), self.texto(exc.chave))
            return None

        self.exibir_resultado(resultado)
        return resultado

    def plotar(self, bias_val, scale_val, raw_val):
        graph_min, graph_max, _ = limites_grafico(bias_val, scale_val)
        self.graph_min = graph_min
        self.graph_max = graph_max
        self.pontos_analise = coletar_pontos_analise(bias_val, scale_val, graph_min, graph_max, raw_val)
        desenhar_pontos_analise(self.bias_graph, self.pontos_analise, graph_min, graph_max)
        atualizar_legenda(self.legend_canvas, self.pontos_analise, graph_min, graph_max, self.textos())
        return "break"

    def acionar(self):
        resultado = self.calcular()
        if resultado is not None:
            _, bias_calc, scale_calc, raw_calc = resultado
            self.plotar(bias_calc, scale_calc, raw_calc)
        return "break"

    def about(self):
        return mostrar_about(self.app, self.textos())

    def run(self):
        self.app.mainloop()


def main():
    IndicadorApp().run()


if __name__ == "__main__":
    main()
