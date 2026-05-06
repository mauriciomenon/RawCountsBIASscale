from cx_Freeze import setup, Executable

base = None    

executables = [Executable("indicador.py", base=base)]

options = {
    'build_exe': {    
        'packages':[],
    },    
}

setup(
    name = "BIAS/SCALE RAW COUNTS SCADA/UTR",
    options = options,
    version = "1.12",
    description = 'Verificação de valores analógicos na UTR/SCADA; BIAS/SCALE; Raw Counts',
    executables = executables
)
