import tkinter as tk
import tk_tools
from tkinter import messagebox

app = tk.Tk()
app.title( "SCADA: Raw Counts & BIAS/SCALE")

#app.geometry

# DISCLAIMER:
# NÃO É RECOMENDADO MISTURAR OS LAYOUT MANAGERS `pack` E `grid`

# ----------------------------------------------------------------------
# FRAME de valores em miliamperes
amp_frame = tk.LabelFrame(app, text="Valores de Corrente do Transdutor (mA)", padx=10, pady=5)
amp_frame.pack(fill="both", expand="yes")

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
scale_frame.pack(fill="both", expand="yes")

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
return_frame.pack(fill="both", expand="yes")

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
return_frame_utr.pack(fill="both", expand="yes")

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
    plotar()
    return "break"
# ----------------------------------------------------------------------
# BUTTON calcular
b_calcular = tk.Button(app, text="Calcular", height=2, width=10, command=acionar)
b_calcular.pack()

# ----------------------------------------------------------------------
# FRAME do gráfico
graph_frame = tk.LabelFrame(app, text="Gráfico BIAS/SCALE", padx=10, pady=5)
bias_graph = tk_tools.Graph(
    parent=graph_frame,
    x_min=0,
    x_max=32768,
    y_min=0.0,
    y_max=10.0,
    x_tick=8192,
    y_tick=2.5,
    width=300,
    height=300
)
bias_graph.grid(row=0, column=0)
graph_frame.pack(fill="both", expand="yes")

#----------------------------------------------------------------------
# FUNCTION plotar
def plotar():
    #graph_frame = tk.LabelFrame(app, text="Gráfico", padx=10, pady=5)
    bias_graph = tk_tools.Graph(
        parent=graph_frame,
        x_min=-0,
        x_max=32768,
        #y_min=bias,
        y_min=0,
        y_max=scale,
        x_tick=8192,
        y_tick=(scale-bias)/4,
        width=300,
        height=300
    )

    bias_graph.grid(row=0, column=0)
    # create an initial line
    line_0 = ((0,bias),(32767,scale))
    bias_graph.plot_line(line_0,color='black',point_visibility=True)
    #evita a abertura de frames multiplos mas também não atualiza os valores
    graph_frame.pack(fill="both", expand="yes")
    return "break"

# ----------------------------------------------------------------------
# FUNCTION calcular
def calcular():
    f_lim = float(ptr_e_lim_sup.get()) - float(ptr_e_lim_inf.get())
    f_ran = float(ptr_e_ran_sup.get()) - float(ptr_e_ran_inf.get())
    f_med = float(ptr_e_ponteiro.get()) - float(ptr_e_ran_inf.get())
    f_e_ran_sup_neg= -(float(ptr_e_ran_sup.get()))

    try:
        corrente = f_med*f_lim/f_ran + float(ptr_e_lim_inf.get())
        global bias,scale
        bias = float ((f_e_ran_sup_neg  +(5*float(ptr_e_ran_inf.get())))/4)
        scale = float(ptr_e_ran_sup.get()) #versoes antigas erro com ran_inf
        #considerado valores positivos de corrente para raw_int16, caso seja negativo não tem o -1
        #verificar se o /20 nao pode ser sunstituido pelo variavel de fundo de escala amperimetro (20ma)
        raw_int16 = int ((corrente/20)*(2**15-1)) 
        raw_hexa16 = hex(raw_int16) #TO DO tratamento de erro
                      
    except ZeroDivisionError:
        corrente = 0
    
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
    messagebox.showinfo("About", "Versão 1.11; tk/Python; Maurício Menon Obs: gráfico beta")
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



