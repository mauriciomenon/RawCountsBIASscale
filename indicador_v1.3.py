import tkinter as tk

app = tk.Tk()

# DISCLAIMER:
# NÃO É RECOMENDADO MISTURAR OS LAYOUT MANAGERS `pack` E `grid`

# ----------------------------------------------------------------------
# FRAME de valores em miliamperes
amp_frame = tk.LabelFrame(app, text="Valores de Corrente do Transdutor (mA)")
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
scale_frame = tk.LabelFrame(app, text="Escala de Grandeza do Equipamento Primário")
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
# FRAME dos resultados
return_frame = tk.LabelFrame(app, text="Resultados Transdutor e DB SCADA")
return_frame.pack(fill="both", expand="yes")

# Ponteiro do amperimetro (valor calculado)

l_cal_text = tk.Label(return_frame, text="Valor (mA)", anchor=tk.W)
l_cal_val = tk.Label(return_frame, text="", anchor=tk.W)
l_cal_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
l_cal_val.grid(row=0, column=1, sticky=(tk.W, tk.E))

# Limites Range Fisico
l_cal_inf = tk.Label(return_frame, text="BIAS", anchor=tk.W)
l_cal_sup = tk.Label(return_frame, text="SCALE", anchor=tk.W)



# ----------------------------------------------------------------------
# FUNCTION calcular
def calcular():
    f_lim = float(ptr_e_lim_sup.get()) - float(ptr_e_lim_inf.get())
    f_ran = float(ptr_e_ran_sup.get()) - float(ptr_e_ran_inf.get())
    f_med = float(ptr_e_ponteiro.get()) - float(ptr_e_ran_inf.get())

    try:
        corrente = f_med*f_lim/f_ran + float(ptr_e_lim_inf.get())
        
    #
    # FIX-ME !!!!!
    #
    except ZeroDivisionError:
        corrente = 0
    
    l_cal_val["text"] = str(corrente)

    ptr_e_ran_sup_neg= -(float(ptr_e_ran_sup.get()))
    BIAS = float ((ptr_e_ran_sup_neg  +(5*float(ptr_e_ran_inf.get())))/4)
    print (float(BIAS))
    
    return "break"


# ----------------------------------------------------------------------
# BUTTON calcular
b_calcular = tk.Button(app, text="Calcular", command=calcular)
b_calcular.pack()

# BINDINGS
app.bind_all("<Return>", lambda x: calcular())
app.mainloop()
