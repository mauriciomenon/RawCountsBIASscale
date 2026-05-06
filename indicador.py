import tkinter as tk
from tkinter import messagebox

RAW_MAX = 2**15 - 1
DEFAULT_LIM_INF = 4.0
DEFAULT_LIM_SUP = 20.0
DEFAULT_RAN_INF = 0.0
DEFAULT_RAN_SUP = 10.0
DEFAULT_PONTEIRO = 5.0
CANVAS_WIDTH = 360
CANVAS_HEIGHT = 120
CANVAS_LEFT = 60
CANVAS_RIGHT = 14
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
POINT_LABELS = {
    "x=0": "(x,y) min",
    "x=max": "(x,y) max",
    "y=0": "(x,y) zero",
    "y=min": "(x,y) ymin",
    "y=max": "(x,y) ymax",
    "medido": "(x,y) med",
}
FORM_LABEL_MIN_WIDTH = 190
VALUE_COLUMN_WIDTH = 24
FRAME_PADY = (6, 0)


def configurar_colunas(frame):
    frame.grid_columnconfigure(0, minsize=FORM_LABEL_MIN_WIDTH)
    frame.grid_columnconfigure(1, weight=0)


def criar_saida_valor(parent):
    return tk.Label(parent, text="--", anchor=tk.W, width=VALUE_COLUMN_WIDTH, relief="groove", bd=1, padx=4)


def calcular_valores(lim_inf, lim_sup, ran_inf, ran_sup, ponteiro):
    f_lim = lim_sup - lim_inf
    f_ran = ran_sup - ran_inf
    if f_ran == 0:
        raise ValueError("Range fisico nao pode ser zero")
    if f_lim == 0:
        raise ValueError("Range de corrente nao pode ser zero")
    if lim_sup == 0:
        raise ValueError("Limite superior nao pode ser zero")
    ran_min = min(ran_inf, ran_sup)
    ran_max = max(ran_inf, ran_sup)
    if not (ran_min <= ponteiro <= ran_max):
        raise ValueError("Ponteiro fora do range fisico")

    corrente = ((ponteiro - ran_inf) * f_lim / f_ran) + lim_inf
    scale_calc = lim_sup * f_ran / f_lim
    bias_calc = ran_sup - scale_calc
    raw_int16 = int((corrente / lim_sup) * RAW_MAX)
    raw_hexa16 = hex(raw_int16)
    return corrente, bias_calc, scale_calc, raw_int16, raw_hexa16


def limites_grafico(bias_val, scale_val):
    graph_upper = bias_val + scale_val
    graph_min = min(0, bias_val, graph_upper)
    graph_max = max(0, bias_val, graph_upper)
    if graph_min == graph_max:
        raise ValueError("Escala do grafico nao pode ser zero")
    graph_tick = abs(graph_max - graph_min) / 4 or 1
    return graph_min, graph_max, graph_tick


app = tk.Tk()
app.title( "SCADA: Raw Counts & BIAS/SCALE")

content_frame = tk.Frame(app, padx=8, pady=8, highlightbackground="white", highlightthickness=1)
content_frame.pack(fill="x", padx=6, pady=(8, 6))

_, bias, scale, raw_int16, _ = calcular_valores(
    DEFAULT_LIM_INF,
    DEFAULT_LIM_SUP,
    DEFAULT_RAN_INF,
    DEFAULT_RAN_SUP,
    DEFAULT_PONTEIRO,
)
calculo_valido = True

#app.geometry

# NOTE: avoid mixing pack and grid in same container

# ----------------------------------------------------------------------
# FRAME de valores em miliamperes
amp_frame = tk.LabelFrame(content_frame, text="Valores de Corrente do Transdutor (mA)", padx=10, pady=5)
amp_frame.pack(fill="x", pady=FRAME_PADY)
configurar_colunas(amp_frame)

# Limites amperimetro
l_lim_inf = tk.Label(amp_frame, text="Limite inferior", anchor=tk.W)
l_lim_sup = tk.Label(amp_frame, text="Limite superior", anchor=tk.W)

ptr_e_lim_inf = tk.StringVar()
ptr_e_lim_inf.set("4")
ptr_e_lim_sup = tk.StringVar()
ptr_e_lim_sup.set("20")

e_lim_inf = tk.Entry(amp_frame, textvariable=ptr_e_lim_inf, width=VALUE_COLUMN_WIDTH)
e_lim_sup = tk.Entry(amp_frame, textvariable=ptr_e_lim_sup, width=VALUE_COLUMN_WIDTH)

l_lim_inf.grid(row=0, column=0, sticky=(tk.W, tk.E))
l_lim_sup.grid(row=1, column=0, sticky=(tk.W, tk.E))
e_lim_inf.grid(row=0, column=1, sticky=tk.W)
e_lim_sup.grid(row=1, column=1, sticky=tk.W)

# ----------------------------------------------------------------------
# FRAME das escalas (grandeza)
scale_frame = tk.LabelFrame(content_frame, text="Escala de Grandeza do Equipamento Primario", padx=10, pady=5)
scale_frame.pack(fill="x", pady=FRAME_PADY)
configurar_colunas(scale_frame)

# Limites Range Fisico
l_ran_inf = tk.Label(scale_frame, text="Range inferior", anchor=tk.W)
l_ran_sup = tk.Label(scale_frame, text="Range superior", anchor=tk.W)

ptr_e_ran_inf = tk.StringVar()
ptr_e_ran_inf.set("0")
ptr_e_ran_sup = tk.StringVar()
ptr_e_ran_sup.set("10")

e_ran_inf = tk.Entry(scale_frame, textvariable=ptr_e_ran_inf, width=VALUE_COLUMN_WIDTH)
e_ran_sup = tk.Entry(scale_frame, textvariable=ptr_e_ran_sup, width=VALUE_COLUMN_WIDTH)

l_ran_inf.grid(row=0, column=0, sticky=(tk.W, tk.E))
l_ran_sup.grid(row=1, column=0, sticky=(tk.W, tk.E))
e_ran_inf.grid(row=0, column=1, sticky=tk.W)
e_ran_sup.grid(row=1, column=1, sticky=tk.W)

# Ponteiro
l_ponteiro = tk.Label(scale_frame, text="Valor medido", anchor=tk.W)
ptr_e_ponteiro = tk.StringVar()
ptr_e_ponteiro.set("5")
e_ponteiro = tk.Entry(scale_frame, textvariable=ptr_e_ponteiro, width=VALUE_COLUMN_WIDTH)

l_ponteiro.grid(row=2, column=0, sticky=(tk.W, tk.E))
e_ponteiro.grid(row=2, column=1, sticky=tk.W)

# ----------------------------------------------------------------------
# FRAME dos resultados SCADA
return_frame = tk.LabelFrame(content_frame, text="Resultado SCADA", padx=10, pady=5)
return_frame.pack(fill="x", pady=FRAME_PADY)
configurar_colunas(return_frame)

# Ponteiros BIAS e SCALE
l_cal_bias_text = tk.Label(return_frame, text="BIAS", anchor=tk.W)
l_cal_bias_val = criar_saida_valor(return_frame)
l_cal_bias_text.grid(row=1, column=0, sticky=(tk.W, tk.E))
l_cal_bias_val.grid(row=1, column=1, sticky=tk.W)

l_cal_scale_text = tk.Label(return_frame, text="SCALE", anchor=tk.W)
l_cal_scale_val = criar_saida_valor(return_frame)
l_cal_scale_text.grid(row=2, column=0, sticky=(tk.W, tk.E))
l_cal_scale_val.grid(row=2, column=1, sticky=tk.W)

#l_cal_bias_val["text"] = "--"
#l_cal_scale_val["text"]= "--"

# ----------------------------------------------------------------------
# FRAME dos resultados UTR

return_frame_utr = tk.LabelFrame(content_frame, text="Resultado UTR", padx=10, pady=5)
return_frame_utr.pack(fill="x", pady=FRAME_PADY)
configurar_colunas(return_frame_utr)

# Ponteiro do amperimetro

l_cal_text = tk.Label(return_frame_utr, text="Valor (mA)", anchor=tk.W)
l_cal_val = criar_saida_valor(return_frame_utr)
l_cal_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
l_cal_val.grid(row=0, column=1, sticky=tk.W)

# Ponteiro do raw_couts INT 

l_cal_text_int = tk.Label(return_frame_utr, text="INT (16 bits)", anchor=tk.W)
l_cal_val_int = criar_saida_valor(return_frame_utr)
l_cal_text_int.grid(row=1, column=0, sticky=(tk.W, tk.E))
l_cal_val_int.grid(row=1, column=1, sticky=tk.W)

# Ponteiro do raw_couts HEXA 

l_cal_text_hex = tk.Label(return_frame_utr, text="HEXA (16 bits)", anchor=tk.W)
l_cal_val_hex = criar_saida_valor(return_frame_utr)
l_cal_text_hex.grid(row=2, column=0, sticky=(tk.W, tk.E))
l_cal_val_hex.grid(row=2, column=1, sticky=tk.W)

#-----------------------------------------------------------------------
#FUNCTION acionar botao (parametros multiplos)
def acionar():
    calcular()
    if calculo_valido:
        plotar()
    return "break"
# ----------------------------------------------------------------------
# FRAME do grafico
graph_frame = tk.LabelFrame(content_frame, text="Grafico BIAS/SCALE", padx=10, pady=5)
graph_min, graph_max, _ = limites_grafico(bias, scale)


def y_para_px(valor_y, y_min, y_max):
    if y_max == y_min:
        return CANVAS_HEIGHT / 2
    return CANVAS_HEIGHT - CANVAS_BOTTOM - ((valor_y - y_min) / (y_max - y_min)) * (
        CANVAS_HEIGHT - CANVAS_TOP - CANVAS_BOTTOM
    )


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


def x_para_px(raw_val):
    return CANVAS_LEFT + (raw_val / RAW_MAX) * (CANVAS_WIDTH - CANVAS_LEFT - CANVAS_RIGHT)


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
    for label, raw_val, y_val in pontos_analise:
        raio = 4
        cor = POINT_COLORS.get(label, "#444444")
        x_px = x_para_px(raw_val)
        y_px = y_para_px(y_val, y_min, y_max)
        canvas.create_oval(x_px - raio, y_px - raio, x_px + raio, y_px + raio, fill=cor, outline="")


def atualizar_legenda(pontos_analise, y_min, y_max):
    legend_canvas.delete("all")
    legend_canvas.create_line(0, 1, LEGEND_WIDTH, 1, fill="#8a8a8a")
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
        label_texto = POINT_LABELS.get(label, label)
        valor_texto = f"{y_val:.3f}"
        y_px = 14 + idx * 14
        legend_canvas.create_text(LEGEND_LABEL_X, y_px, text=label_texto, anchor="w", font=("Consolas", 7))
        legend_canvas.create_oval(LEGEND_DOT_X - 4, y_px - 4, LEGEND_DOT_X + 4, y_px + 4, fill=cor, outline="")
        legend_canvas.create_text(LEGEND_RAW_LABEL_X, y_px, text="raw=", anchor="w", font=("Consolas", 7))
        legend_canvas.create_text(LEGEND_RAW_VALUE_X, y_px, text=raw_texto, anchor="e", font=("Consolas", 7))
        legend_canvas.create_text(LEGEND_SEPARATOR_X, y_px, text="|", anchor="center", font=("Consolas", 7))
        legend_canvas.create_text(LEGEND_VALUE_LABEL_X, y_px, text="valor=", anchor="w", font=("Consolas", 7))
        legend_canvas.create_text(LEGEND_VALUE_X, y_px, text=valor_texto, anchor="w", font=("Consolas", 7))


bias_graph = tk.Canvas(graph_frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, highlightthickness=0)
bias_graph.grid(row=0, column=0, sticky="w")
legend_canvas = tk.Canvas(graph_frame, width=LEGEND_WIDTH, height=LEGEND_HEIGHT, highlightthickness=0)
legend_canvas.grid(row=1, column=0, sticky="w", padx=CANVAS_LEFT, pady=(0, 0))
pontos_analise = coletar_pontos_analise(bias, scale, graph_min, graph_max, raw_int16)
desenhar_pontos_analise(bias_graph, pontos_analise, graph_min, graph_max)
atualizar_legenda(pontos_analise, graph_min, graph_max)
graph_frame.pack(fill="x", pady=FRAME_PADY)

#----------------------------------------------------------------------
# FUNCTION plotar
def plotar():
    graph_min, graph_max, _ = limites_grafico(bias, scale)
    pontos_analise = coletar_pontos_analise(bias, scale, graph_min, graph_max, raw_int16)
    desenhar_pontos_analise(bias_graph, pontos_analise, graph_min, graph_max)
    atualizar_legenda(pontos_analise, graph_min, graph_max)
    return "break"

# ----------------------------------------------------------------------
# FUNCTION calcular
def calcular():
    global bias, scale, raw_int16, calculo_valido
    calculo_valido = False

    try:
        lim_inf = float(ptr_e_lim_inf.get())
        lim_sup = float(ptr_e_lim_sup.get())
        ran_inf = float(ptr_e_ran_inf.get())
        ran_sup = float(ptr_e_ran_sup.get())
        ponteiro = float(ptr_e_ponteiro.get())
    except ValueError:
        l_cal_val["text"] = "--"
        l_cal_bias_val["text"] = "--"
        l_cal_scale_val["text"]= "--"
        l_cal_val_int["text"]= "--"
        l_cal_val_hex["text"]= "--"
        messagebox.showerror("Erro", "Informe apenas valores numericos")
        return "break"

    try:
        corrente, bias, scale, raw_int16, raw_hexa16 = calcular_valores(
            lim_inf,
            lim_sup,
            ran_inf,
            ran_sup,
            ponteiro,
        )
    except ValueError as exc:
        raw_hexa16 = "--"
        l_cal_val["text"] = "--"
        l_cal_bias_val["text"] = "--"
        l_cal_scale_val["text"]= "--"
        l_cal_val_int["text"]= "--"
        l_cal_val_hex["text"]= str(raw_hexa16)
        messagebox.showerror("Erro", str(exc))
        return "break"
    
    calculo_valido = True
    l_cal_val["text"] = str(corrente)
    l_cal_bias_val["text"] = str(bias)
    l_cal_scale_val["text"]= str(scale)
    l_cal_val_int["text"]= str(raw_int16)
    l_cal_val_hex["text"]= str(raw_hexa16)
       
    #print (int(raw_int16))
    return "break"


#------------------------------------------------------
#acao botao info
def about():
    messagebox.showinfo("About", "Versao de trabalho; tk/Python; Mauricio Menon")
    return "break"
#-----------------------------------------------------------------------
#BUTTON about
footer_frame = tk.Frame(content_frame, height=34)
footer_frame.pack(fill="x", pady=(8, 2))
footer_frame.pack_propagate(False)

b_calcular = tk.Button(footer_frame, text="Calcular", width=7, command=acionar, font=("Arial", 10))
b_calcular.place(relx=0.5, rely=0.5, anchor="center")

b_about = tk.Button(footer_frame, text="About", width=4, command=about, font=("Arial", 7), padx=1, pady=1, anchor="center")
b_about.place(relx=0.98, rely=0.5, anchor="e")

#------------------------------
# BINDINGS
app.bind_all("<Return>", lambda x: acionar())
app.mainloop()
