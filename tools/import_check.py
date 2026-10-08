import importlib, sys, traceback
mods = ['brain','voice','commands','memory','reminder','todo','notes']
ok = True
for m in mods:
    try:
        importlib.reload(importlib.import_module(m))
        print(f'Imported {m} OK')
    except Exception:
        ok = False
        print(f'ERROR importing {m}:')
        traceback.print_exc()
if not ok:
    sys.exit(1)
print('ALL IMPORTS OK')
