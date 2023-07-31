import os
import shutil
import subprocess

path = os.path.dirname(__file__)
command = f'''pyinstaller --noconfirm --onefile --windowed \
--add-data "{path}/images;images/" \
--add-data "{path}/scripts;scripts/" \
--add-data "{path}/sounds;sounds/" \
"{path}/main.py"'''

subprocess.run(command)
if os.path.isdir(f'{path}/build'): shutil.rmtree(f'{path}/build')
if os.path.isfile(f'{path}/main.spec'): os.remove(f'{path}/main.spec')
shutil.move(f'{path}/dist/main.exe', f'{path}/signki.exe')
shutil.rmtree(f'{path}/dist')