import tkinter as tk
import tk_tools
from tkinter import messagebox

RAW_MAX = 2**15 - 1
DEFAULT_LIM_INF = 4.0
DEFAULT_LIM_SUP = 20.0
DEFAULT_RAN_INF = 0.0
DEFAULT_RAN_SUP = 10.0
DEFAULT_PONTEIRO = 5.0


def calcular_valores(lim_inf, lim_sup, ran_inf, ran_sup, ponteiro):
    f_lim = lim_sup - lim_inf
    f_ran = ran_sup - ran_inf
    if f_ran == 0:
        raise ValueError("Range fisico nao pode ser zero")
    if f_lim == 0:
        raise ValueError("Range de corrente nao pode ser zero")
    if lim_sup == 0:
        raise ValueError("Limite superior nao pode ser zero")

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

_, bias, scale, _, _ = calcular_valores(
    DEFAULT_LIM_INF,
    DEFAULT_LIM_SUP,
    DEFAULT_RAN_INF,
    DEFAULT_RAN_SUP,
    DEFAULT_PONTEIRO,
)
calculo_valido = True

#app.geometry

# DISCLAIMER:
# NÃO É RECOMENDADO MISTURAR OS LAYOUT MANAGERS `pack` E `grid`

# ----------------------------------------------------------------------
# FRAME de valores em miliamperes
amp_frame = tk.LabelFrame(app, text="Valores de Corrente do Transdutor (mA)", padx=10, pady=5)
amp_frame.pack(fill="both", expand=True)

# Limites amperimetro
l_lim_inf = tk.Label(amp_frame, text="Limite inferior", anchor=tk.W)
l_lim_sup = tk.Label(amp_frame, text="Limite superior", anchor=tk.W)

ptr_e_lim_inf = tk.StringVar()
ptr_e_lim_inf.set("4")
ptr_e_lim_sup = tk.StringVar()
ptr_e_lim_sup.set("20")

e_lim_inf = tk.Entry(amp_frame, textvariable=ptr_e_lim_inf)
e_lim_sup = tk.Entry(amp_frame, textvariable=ptr_e_lim_sup)

l_lim_inf.grid(row=0, column=0, sticky=(tk.W, tk.E))
l_lim_sup.grid(row=1, column=0, sticky=(tk.W, tk.E))
e_lim_inf.grid(row=0, column=1, sticky=(tk.W, tk.E))
e_lim_sup.grid(row=1, column=1, sticky=(tk.W, tk.E))

# ----------------------------------------------------------------------
# FRAME das escalas (grandeza)
scale_frame = tk.LabelFrame(app, text="Escala de Grandeza do Equipamento Primário", padx=10, pady=5)
scale_frame.pack(fill="both", expand=True)

# Limites Range Fisico
l_ran_inf = tk.Label(scale_frame, text="Range inferior", anchor=tk.W)
l_ran_sup = tk.Label(scale_frame, text="Range superior", anchor=tk.W)

ptr_e_ran_inf = tk.StringVar()
ptr_e_ran_inf.set("0")
ptr_e_ran_sup = tk.StringVar()
ptr_e_ran_sup.set("10")

e_ran_inf = tk.Entry(scale_frame, textvariable=ptr_e_ran_inf)
e_ran_sup = tk.Entry(scale_frame, textvariable=ptr_e_ran_sup)

l_ran_inf.grid(row=0, column=0, sticky=(tk.W, tk.E))
l_ran_sup.grid(row=1, column=0, sticky=(tk.W, tk.E))
e_ran_inf.grid(row=0, column=1, sticky=(tk.W, tk.E))
e_ran_sup.grid(row=1, column=1, sticky=(tk.W, tk.E))

# Ponteiro
l_ponteiro = tk.Label(scale_frame, text="Valor medido", anchor=tk.W)
ptr_e_ponteiro = tk.StringVar()
ptr_e_ponteiro.set("5")
e_ponteiro = tk.Entry(scale_frame, textvariable=ptr_e_ponteiro)

l_ponteiro.grid(row=2, column=0, sticky=(tk.W, tk.E))
e_ponteiro.grid(row=2, column=1, sticky=(tk.W, tk.E))

# ----------------------------------------------------------------------
# FRAME dos resultados SCADA
return_frame = tk.LabelFrame(app, text="Resultado SCADA", padx=10, pady=5)
return_frame.pack(fill="both", expand=True)

# Ponteiros BIAS e SCALE
l_cal_bias_text = tk.Label(return_frame, text="BIAS", anchor=tk.W)
l_cal_bias_val = tk.Label(return_frame, text="--", anchor=tk.W)
l_cal_bias_text.grid(row=1, column=0, sticky=(tk.W, tk.E))
l_cal_bias_val.grid(row=1, column=1, sticky=(tk.W, tk.E))

l_cal_scale_text = tk.Label(return_frame, text="SCALE", anchor=tk.W)
l_cal_scale_val = tk.Label(return_frame, text="--", anchor=tk.W)
l_cal_scale_text.grid(row=2, column=0, sticky=(tk.W, tk.E))
l_cal_scale_val.grid(row=2, column=1, sticky=(tk.W, tk.E))

#l_cal_bias_val["text"] = "--"
#l_cal_scale_val["text"]= "--"

# ----------------------------------------------------------------------
# FRAME dos resultados UTR

return_frame_utr = tk.LabelFrame(app, text="Resultado UTR", padx=10, pady=5)
return_frame_utr.pack(fill="both", expand=True)

# Ponteiro do amperimetro

l_cal_text = tk.Label(return_frame_utr, text="Valor (mA)", anchor=tk.W)
l_cal_val = tk.Label(return_frame_utr, text="--", anchor=tk.W)
l_cal_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
l_cal_val.grid(row=0, column=1, sticky=(tk.W, tk.E))

# Ponteiro do raw_couts INT 

l_cal_text_int = tk.Label(return_frame_utr, text="INT (16 bits)", anchor=tk.W)
l_cal_val_int = tk.Label(return_frame_utr, text="--", anchor=tk.W)
l_cal_text_int.grid(row=1, column=0, sticky=(tk.W, tk.E))
l_cal_val_int.grid(row=1, column=1, sticky=(tk.W, tk.E))

# Ponteiro do raw_couts HEXA 

l_cal_text_hex = tk.Label(return_frame_utr, text="HEXA (16 bits)", anchor=tk.W)
l_cal_val_hex = tk.Label(return_frame_utr, text="--", anchor=tk.W)
l_cal_text_hex.grid(row=2, column=0, sticky=(tk.W, tk.E))
l_cal_val_hex.grid(row=2, column=1, sticky=(tk.W, tk.E))

#-----------------------------------------------------------------------
#FUNCTION acionar botao (parametros multiplos)
def acionar():
    calcular()
    if calculo_valido:
        plotar()
    return "break"
# ----------------------------------------------------------------------
# BUTTON calcular
b_calcular = tk.Button(app, text="Calcular", height=2, width=10, command=acionar)
b_calcular.pack()

# ----------------------------------------------------------------------
# FRAME do gráfico
graph_frame = tk.LabelFrame(app, text="Gráfico BIAS/SCALE", padx=10, pady=5)
graph_min, graph_max, graph_tick = limites_grafico(bias, scale)
graph_axis_state = (graph_min, graph_max, graph_tick)
bias_graph = tk_tools.Graph(
    parent=graph_frame,
    x_min=0,
    x_max=32768,
    y_min=graph_min,
    y_max=graph_max,
    x_tick=8192,
    y_tick=graph_tick,
    width=300,
    height=300
)
bias_graph.grid(row=0, column=0)
line_0 = ((0,bias),(32767,bias + scale))
bias_graph.plot_line(line_0,color='black',point_visibility=True)
graph_frame.pack(fill="both", expand=True)

#----------------------------------------------------------------------
# FUNCTION plotar
def plotar():
    global graph_axis_state
    #graph_frame = tk.LabelFrame(app, text="Gráfico", padx=10, pady=5)
    graph_min, graph_max, graph_tick = limites_grafico(bias, scale)
    if graph_axis_state != (graph_min, graph_max, graph_tick):
        bias_graph.y_min = graph_min
        bias_graph.y_max = graph_max
        bias_graph.y_tick = graph_tick
        graph_axis_state = (graph_min, graph_max, graph_tick)
    graph_upper = bias + scale
    bias_graph.draw_axes()
    # create an initial line
    line_0 = ((0,bias),(32767,graph_upper))
    bias_graph.plot_line(line_0,color='black',point_visibility=True)
    # atualiza o grafico sem recriar o widget
    graph_frame.pack(fill="both", expand=True)
    return "break"

# ----------------------------------------------------------------------
# FUNCTION calcular
def calcular():
    global bias, scale, calculo_valido
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
    messagebox.showinfo("About", "Versão 1.12; tk/Python; Maurício Menon Obs: gráfico beta")
    return "break"
#-----------------------------------------------------------------------
#BUTTON about
b_about= tk.Button(app, text="About", command=about)
b_about.place(x=0,y=0)
b_about.pack()

#------------------------------
# BINDINGS
app.bind_all("<Return>", lambda x: calcular())
app.mainloop()
