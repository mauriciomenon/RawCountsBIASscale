import tkinter as tk

app = tk.Tk()

# Limites amperimetro
l_lim_inf = tk.Label(app, text="Limite inferior", anchor=tk.W)
l_lim_sup = tk.Label(app, text="Limite superior", anchor=tk.W)

ptr_e_lim_inf = tk.StringVar()
ptr_e_lim_sup = tk.StringVar()

ptr_e_lim_inf.set("4")
ptr_e_lim_sup.set("20")

e_lim_inf = tk.Entry(app, textvariable=ptr_e_lim_inf)
e_lim_sup = tk.Entry(app, textvariable=ptr_e_lim_sup)

# Limites Range Fisico
l_ran_inf = tk.Label(app, text="Range inferior", anchor=tk.W)
l_ran_sup = tk.Label(app, text="Range superior", anchor=tk.W)

ptr_e_ran_inf = tk.StringVar()
ptr_e_ran_sup = tk.StringVar()

ptr_e_ran_inf.set("-100")
ptr_e_ran_sup.set("1000")

e_ran_inf = tk.Entry(app, textvariable=ptr_e_ran_inf)
e_ran_sup = tk.Entry(app, textvariable=ptr_e_ran_sup)

# Ponteiro

l_ponteiro = tk.Label(app, text="Medição", anchor=tk.W)
ptr_e_ponteiro = tk.StringVar()
ptr_e_ponteiro.set("450")
e_ponteiro = tk.Entry(app, textvariable=ptr_e_ponteiro)

# Ponteiro do amperimetro

l_amp_text = tk.Label(app, text="Valor (A)", anchor=tk.W)
l_amp_val = tk.Label(app, text="", anchor=tk.W)

# Button
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

b_calcular = tk.Button(app, text="Calcular", command=calcular)

l_lim_inf.grid(row=0, column=0, sticky=(tk.W, tk.E))
l_lim_sup.grid(row=1, column=0, sticky=(tk.W, tk.E))
e_lim_inf.grid(row=0, column=1, sticky=(tk.W, tk.E))
e_lim_sup.grid(row=1, column=1, sticky=(tk.W, tk.E))

l_ran_inf.grid(row=2, column=0, sticky=(tk.W, tk.E))
l_ran_sup.grid(row=3, column=0, sticky=(tk.W, tk.E))
e_ran_inf.grid(row=2, column=1, sticky=(tk.W, tk.E))
e_ran_sup.grid(row=3, column=1, sticky=(tk.W, tk.E))

l_ponteiro.grid(row=4, column=0, sticky=(tk.W, tk.E))
e_ponteiro.grid(row=4, column=1, sticky=(tk.W, tk.E))

l_amp_text.grid(row=5, column=0, sticky=(tk.W, tk.E))
l_amp_val.grid(row=5, column=1, sticky=(tk.W, tk.E))

b_calcular.grid(row=6, column=1, sticky=(tk.W, tk.E))

#e_ponteiro.bind_all("<Enter>", lambda x: calcular())

app.mainloop()
