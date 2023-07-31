import os
import random
import tkinter as tk
import ttkbootstrap as ttk
from UIron.ui import Image
from scripts.ui import Draggable
from PIL import Image as pil_image
from scripts.traduction import TRADUCTIONS
import pygame
# from winsound import PlaySound, SND_FILENAME
pygame.mixer.init()

class App(ttk.Window):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # SOUNDS
        self.error_sound = pygame.mixer.Sound('sounds/error.mp3') 
        self.correct_sound = pygame.mixer.Sound('sounds/correct.mp3') 

        # PROPERTIES
        self.image_size = 200
        self.icon_size = 100
        self.image_dir = os.path.join(os.path.dirname(__file__), 'images')
        self.images_paths = os.listdir(self.image_dir)
        self.answers = 0
        self.wins = -1
        self.errors = False
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

    def collide_rect(self, x: int, y: int, i: int, j: int) -> bool:
        image_x, image_y = 100 + i*self.image_size, 100 + j*self.image_size
        if (x >= image_x) and (x+self.icon_size <= image_x+self.image_size):
            if (y >= image_y) and (y+self.icon_size <= image_y+self.image_size):
                return True
        return False

    def render_game(self, *_) -> None:
        self.answers = 0
        if not self.errors: self.wins += 1
        self.errors = False
        def attach(icon_, image_, image_index, icon_index) -> None:
            icon_x, icon_y = icon_.winfo_x(), icon_.winfo_y()
            collisions = [
                self.collide_rect(icon_x, icon_y, i%2, i//2)
                for i in range(4)
            ]

            if any(collisions):
                if not collisions[image_index]:
                    self.errors = True
                    pygame.mixer.Sound.play(self.error_sound)
                else:
                    self.answers += 1
                    pygame.mixer.Sound.play(self.correct_sound)
                    if self.answers == 4: self.after(200, self.render_game)
                    icon_.place_forget()
                    return image_.lift()
            
            icon_x, icon_y = 100 + icon_index*self.icon_size, 550
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
            frame = tk.Frame(self, bg='red', highlightthickness=1, highlightbackground='green')
            tk.Label(frame, text=name, justify='center', wraplength=180).place(relx=0.5, rely=0.5, anchor='center')
            frame.pack_propagate(False)
            frame.place(x=image_x, y=image_y, width=self.image_size, height=self.image_size)
            frame.lift()

            icon.place(x=icon_x, y=icon_y)

            command = lambda _, icon_=icon, image_=image, image_index=i, icon_index=icon_index: attach(icon_, image_, image_index, icon_index)
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