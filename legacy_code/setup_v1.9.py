from cx_Freeze import setup, Executable

base = None    

executables = [Executable("indicador_v1.9.py", base=base)]

packages = ["idna","tkinter"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "BIAS/SCALE RAW COUNTS SCADA/UTR",
    options = options,
    version = "19",
    description = 'Verificação de valores analógicos na UTR/SCADA; BIAS/SCALE; Raw Counts',
    executables = executables
)

