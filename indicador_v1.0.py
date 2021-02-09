import tkinter as tk

app = tk.Tk()

# DISCLAIMER:
# NÃO É RECOMENDADO MISTURAR OS LAYOUT MANAGERS `pack` E `grid`

# ----------------------------------------------------------------------
# FRAME de valores em miliamperes
amp_frame = tk.LabelFrame(app, text="Valores de corrente (mA)")
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

# Ponteiro do amperimetro

l_amp_text = tk.Label(amp_frame, text="Valor (A)", anchor=tk.W)
l_amp_val = tk.Label(amp_frame, text="", anchor=tk.W)
l_amp_text.grid(row=2, column=0, sticky=(tk.W, tk.E))
l_amp_val.grid(row=2, column=1, sticky=(tk.W, tk.E))


# ----------------------------------------------------------------------
# FRAME das escalas (grandeza)
scale_frame = tk.LabelFrame(app, text="Escala de grandeza")
scale_frame.pack(fill="both", expand="yes")

# Limites Range Fisico
l_ran_inf = tk.Label(scale_frame, text="Range inferior", anchor=tk.W)
l_ran_sup = tk.Label(scale_frame, text="Range superior", anchor=tk.W)

ptr_e_ran_inf = tk.StringVar()
ptr_e_ran_inf.set("-100")
ptr_e_ran_sup = tk.StringVar()
ptr_e_ran_sup.set("1000")

e_ran_inf = tk.Entry(scale_frame, textvariable=ptr_e_ran_inf)
e_ran_sup = tk.Entry(scale_frame, textvariable=ptr_e_ran_sup)

l_ran_inf.grid(row=0, column=0, sticky=(tk.W, tk.E))
l_ran_sup.grid(row=1, column=0, sticky=(tk.W, tk.E))
e_ran_inf.grid(row=0, column=1, sticky=(tk.W, tk.E))
e_ran_sup.grid(row=1, column=1, sticky=(tk.W, tk.E))

# Ponteiro
l_ponteiro = tk.Label(scale_frame, text="Medição", anchor=tk.W)
ptr_e_ponteiro = tk.StringVar()
ptr_e_ponteiro.set("450")
e_ponteiro = tk.Entry(scale_frame, textvariable=ptr_e_ponteiro)

l_ponteiro.grid(row=2, column=0, sticky=(tk.W, tk.E))
e_ponteiro.grid(row=2, column=1, sticky=(tk.W, tk.E))

# ----------------------------------------------------------------------
# FUNCTION calcular
def calcular():
    f_lim = float(ptr_e_lim_sup.get()) - float(ptr_e_lim_inf.get())
    f_ran = float(ptr_e_ran_sup.get()) - float(ptr_e_ran_inf.get())
    f_med = float(ptr_e_ponteiro.get()) - float(ptr_e_ran_inf.get())

    try:
        valor = f_med*f_lim/f_ran + float(ptr_e_lim_inf.get())
    #
    # FIX-ME !!!!!
    #
    except ZeroDivisionError:
        valor = 0
    
    l_amp_val["text"] = str(valor)
    return "break"


# ----------------------------------------------------------------------
# BUTTON calcular
b_calcular = tk.Button(app, text="Calcular", command=calcular)
b_calcular.pack()

# BINDINGS
app.bind_all("<Return>", lambda x: calcular())
app.mainloop()
