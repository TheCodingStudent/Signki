import os
import random
import tkinter as tk
import ttkbootstrap as ttk
from UIron.ui import Image
from scripts.ui import Draggable
from PIL import Image as pil_image


TRADUCTIONS = {
    'added lane': 'Se agrega un carril',
    'bycicle crossing': 'Cruce de bicicletas',
    'buggy warning': 'Cuidado con las carretas',
    'cattle crossing': 'Cruce de ganado',
    'intersection ahead': 'Intersección adelante',
    'curve ahead': 'Curva adelante',

    'deer crossing': 'Cruce de venados',
    'detour in 1000 ft': 'Desviación a mil pies',
    'divided highway begins': 'Inicia separación de la carretera',
    'farm machinery': 'Maquinaria agrícola',
    'fire station': 'Estación de bomberos',
    'lane end': 'Termina carril',

    'lanes shifting': 'Cambio de carriles',
    'low clearance': 'Restricción de altura',
    'low shoulder': 'Acotamiento a desnivel',
    'merging traffic': 'Incorporación de tráfico',
    'narrow bridge': 'Puente angosto',
    'pedestrian crossing': 'Cruce peatonal',

    'playground warning': '¡Cuidado! Zona de juegos',
    'prepare to stop': 'Prepárese para detenerse',
    'sharp turn': 'Curva pronunciada',
    'slippery when wet': 'Resbaloso cuando está mojado',
    'steep degree': 'Pendiente peligrosa',
    'stop ahead': 'Alto adelante',

    't intersection': 'Intersección "T"',
    'traffic light': 'Semáforo',
    'two way traffic': 'Doble sentido',
    'winding road': 'Curvas continuas',
    'watch for ice on bridges': 'Cuidado con el hielo en los puentes',
    'yield ahead': 'Ceder el paso adelante',

    'pavement ends': 'Termina el pavimento',
    'speed hump': 'Tope',
    'grooved pavement': 'Pavimento disparejo',
    'fallen rocks': 'Caída de rocas',
    'road may flood': 'Camino se puede inundar',
    'gusty winds area': 'Área de ráfagas de viento',

    'fog area': 'Área de neblina',
    'stop ahead pay toll': 'Alto adelante caseta de cobro',
    'truck roll over warning': 'Advertencia de volcadura en exceso de velocidad',
    'circular intersection': 'Glorieta',
    'lane ends': 'Termina el carril',
    'one way road': 'Un solo sentido',

    'no outlet': 'No hay salida',
    'fallen stones': 'Derrumbes',
    'detour': 'Desviación',
    'detour ahead': 'Desviación adelante',
    'fines double in work zone': 'Multas al doble en zona de trabajo',
    'flagger ahead': 'Trabajadores adelante',

    'right lane closed ahead': 'Carril derecho cerrado',
    'road work ahead': 'Trabajo en carretera adelante',
    'work crew ahead': 'Hombres trabajando adelante',
    'thru traffic merge left': 'Tráfico circulando, introducirse a la izquierda',
    'left shoulder closed half mile': 'Acotamiento cerrado a media milla',
    'right lane closed': 'Carril derecho cerrado',

    'crossing rail road': 'Cruce de ferrocarril',
    'buckle up for safety': 'Abróchese el cinturón por seguridad',
    'click it or ticket': 'Póngase el cinturón o multa',

    'school crossing': 'Cruce de escolares',
    'school bus stop ahead': 'Parada de autobús escolar adelante',
    'slow moving vehicles': 'Vehículos de baja velocidad',

    'speed advisory ahead': 'Indicador de velocidad adelante',
    'speed advisory at a roundabout': 'Indicador de velocidad en glorieta',
    'speed advisory in ramp': 'Indicador de velocidad en rampa',
    'speed limit ahead': 'Límite de velocidad adelante',

    'do not block intersection': 'No bloquear intersección',
    'do not enter': 'No entrar',
    'do not pass': 'No rebasar',
    'pass with care': 'Rebase con cuidado',
    'emergency stop only': 'Solamente paradas de emergencia',
    'keep right': 'Mantengáse a la derecha',

    'left lane must turn left': 'Carril izquierdo debe dar vuelta a la izquierda',
    'left on green arrow only': 'Vuelta a la izquierda solamente con flecha en verde',
    'left turn signal': 'Vuelta a la izquirda con señal',
    'left turn yield on green': 'Permitida vuelta a la izquierda con luz verde',
    '2 hours parking': '2 horas de estacionamiento',
    'minimum speed': 'Velocidad mínima',
    'multiple turns': 'Vueltas múltiples',
    'no left turn': 'No vuelta a la izquierda',

    'no parking': 'No estacionarse',
    'no parking anytime': 'No estacionarse a ninguna hora',
    'no right turns': 'No vuelta a la derecha',
    'no trucks': 'No camiones',
    'no turn on red': 'No dar vuelta en rojo',
    'no u turn': 'No dar vuelta en "U"',
    'one way': 'Un solo sentido',
    'restricted lane ends': 'Termina carril restringido',

    'reserved handicapped': 'Estacionamiento reservado para discapacitado',
    'right lane must turn right': 'Carril derecho tiene que dar vuelta a la derecha',
    'slower traffic keep right': 'Tráfico lento mantenerse a la derecha',
    'speed zone ahead': 'Zona de velocidad adelante',
    'stop': 'Alto',
    'stop here on red': 'Alto en rojo aquí',
    'tow away zone': 'Zona de grúa',
    'turn left or go through': 'Vuelta a la izquierda o sigue en tu carril',

    'turn right or go through': 'Vuelta a la derecha o sigue en tu carril',
    'center lane': 'Carril central',
    'wrong way': 'Sentido contrario',
    'yield': 'Ceder el paso',
    '4 way': '4 altos',
    'all way': '4 altos',
    'biohazard': 'Material químico peligroso',
    'hazmat': 'Líquido inflamable',

    'weigh station 1 mile': 'Estación de pesaje a 1 milla',
    'prepass': 'Pasar sin pensar',
    'by pass': 'Pasar sin pensar',
    'sidewalk closed ahead cross here': 'Banqueta cerrada adelante, cruzar aqui',
    'no overnight parking': 'No estacionarse toda la noche'
}


class App(ttk.Window):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # PROPERTIES
        self.image_size = 200
        self.icon_size = 100
        self.image_dir = os.path.join(os.path.dirname(__file__), 'images')
        self.images_paths = os.listdir(self.image_dir)
        self.answers = 0
        self.wins = -1
        self.font = ('Segoe UI', 16)
        self.reset_images()
        self.render_game()

    def load_image(self, image_name: str) -> tuple[Image, str]:

        # LOADING IMAGE
        result = pil_image.new(mode='RGB', size=(self.image_size-2, self.image_size-2), color=(255, 255, 255))
        image = pil_image.open(f'{self.image_dir}/{image_name}')
        width, height = image.size

        # RESIZING IMAGE
        hwidth, hheight = int(width/2), int(height/2)
        image = image.resize((hwidth, hheight))

        # ADDING WHITE SPACE TO MAKE EACH IMAGE EQUAL SIZE
        x, y = (self.image_size-hwidth)//2, (self.image_size-hheight)//2
        result.paste(image, (x, y))
        image = Image(self)
        image.set_image(result)

        name = image_name.replace('.png', '').lower()

        return image, TRADUCTIONS[name]
    
    def load_icon(self, image_name: str) -> Image:

        # LOADING IMAGE
        result = pil_image.new(mode='RGB', size=(self.icon_size, self.icon_size), color=(255, 255, 255))
        image = pil_image.open(f'{self.image_dir}/{image_name}')
        width, height = image.size

        # RESIZING IMAGE
        hwidth, hheight = int(width/4), int(height/4)
        image = image.resize((hwidth, hheight))

        # ADDING WHITE SPACE TO MAKE EACH IMAGE EQUAL SIZE
        x, y = (self.icon_size-hwidth)//2, (self.icon_size-hheight)//2
        result.paste(image, (x, y))
        image = Image(self)
        image.set_image(result)

        return Draggable(image)

    def reset_images(self) -> None:
        random.shuffle(self.images_paths)
        self.images = [self.load_image(image_name) for image_name in self.images_paths]
        self.icons = [self.load_icon(image_name) for image_name in self.images_paths]

    def render_game(self, *_) -> None:
        self.answers = 0
        self.wins += 1
        def attach(icon_, image_, index) -> bool:
            icon_x, icon_y = icon_.winfo_x(), icon_.winfo_y()
            image_x, image_y = image_.winfo_x(), image_.winfo_y()
            if (icon_x >= image_x) and (icon_x+self.icon_size <= image_x+self.image_size):
                if (icon_y >= image_y) and (icon_y+self.icon_size <= image_y+self.image_size):
                    self.answers += 1
                    if self.answers == 4: self.after(200, self.render_game)
                    icon_.place_forget()
                    return image_.lift()
            
            icon_x, icon_y = 100 + index*self.icon_size, 550
            icon_.place(x=icon_x, y=icon_y)

        for children in self.winfo_children():
            children.place_forget()

        ttk.Label(self, text=f'Puntos: {self.wins}', font=self.font).place(x=25, y=25)

        if len(self.images) < 4: self.reset_images()
        numbers = [0, 1, 2, 3]
        for i in range(4):
            x, y = i%2, i//2
            image_x, image_y = 100 + x*self.image_size, 100 + y*self.image_size
    
            icon_index = random.choice(numbers)
            icon_x, icon_y = 100 + icon_index*self.icon_size, 550
            numbers.remove(icon_index)
            index = random.randint(0, len(self.images)-1)
            image, name = self.images[index] 
            icon = self.icons[index]
            self.images.pop(index)
            self.icons.pop(index)
            
            image.place(x=image_x, y=image_y)
            frame = tk.Frame(self, bg='red', highlightthickness=1, highlightbackground='red')
            tk.Label(frame, text=name, justify='center', wraplength=180).place(relx=0.5, rely=0.5, anchor='center')
            frame.pack_propagate(False)
            frame.place(x=image_x, y=image_y, width=self.image_size, height=self.image_size)
            frame.lift()

            icon.place(x=icon_x, y=icon_y)

            command = lambda _, icon_=icon, image_=image, index=icon_index: attach(icon_, image_, index)
            icon.bind('<ButtonRelease-1>', command)


if __name__ == '__main__':
    app = App(
        title='Signki By Javier Vazquez & Armando Chaparro 29/07/23',
        themename='darkly',
        resizable=(False, False),
        size=(600, 700)
    )

    app.place_window_center()
    app.mainloop()