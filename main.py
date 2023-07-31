import os
import random
import pygame
import tkinter as tk
import ttkbootstrap as ttk
from UIron.ui import Image
from scripts.ui import Draggable
from PIL import Image as pil_image
from scripts.traduction import TRADUCTIONS
from ttkbootstrap.scrolled import ScrolledFrame

pygame.mixer.init()


class App(ttk.Window):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # STYLE
        self.font = ('Segoe UI', 16)

        # GAME PROPERTIES
        self.answers = 0
        self.wins = -1
        self.errors = False
        self.numbers = [0, 1, 2, 3]

        # PROPERTIES
        self.icon_size = 140
        self.image_size = 200
        self.image_dir = os.path.join(os.path.dirname(__file__), 'images')
        self.sound_dir = os.path.join(os.path.dirname(__file__), 'sounds')
        self.images_paths = os.listdir(self.image_dir)

        # SOUNDS
        self.error_sound = pygame.mixer.Sound(f'{self.sound_dir}/error.mp3') 
        self.correct_sound = pygame.mixer.Sound(f'{self.sound_dir}/correct.mp3') 

        # BUILD
        self.tutorial = Tutorial(self, width=600, height=700)
        self.reset_images()
        self.render_game()

    def show_tutorial(self) -> None:
        """Shows the tutorial frame"""
        self.tutorial.place(x=0, y=0)
        self.tutorial.lift()

    def load_image(self, image_name: str) -> tuple[Image, str, str]:
        """Loads an image with its traduction"""

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

        # GETTING TRADUCTION
        name = image_name.replace('.png', '').lower()
        return image, name, TRADUCTIONS[name]
    
    def load_icon(self, image_name: str) -> Image:
        """ Loads an icon and returns a draggable icon"""

        # LOADING IMAGE
        result = pil_image.new(mode='RGB', size=(self.icon_size, self.icon_size), color=(255, 255, 255))
        image = pil_image.open(f'{self.image_dir}/{image_name}')
        width, height = image.size

        # RESIZING IMAGE
        hwidth, hheight = int(width * self.icon_size/400), int(height * self.icon_size/400)
        image = image.resize((hwidth, hheight))

        # ADDING WHITE SPACE TO MAKE EACH IMAGE EQUAL SIZE
        x, y = (self.icon_size-hwidth)//2, (self.icon_size-hheight)//2
        result.paste(image, (x, y))
        image = Image(self)
        image.set_image(result)

        # RETURN A DRAGGABLE
        return Draggable(image)

    def reset_images(self) -> None:
        """Shuffles the images and loads the images and icons"""
        random.shuffle(self.images_paths)
        self.images = [self.load_image(image_name) for image_name in self.images_paths]
        self.icons = [self.load_icon(image_name) for image_name in self.images_paths]

    def collide_rect(self, x: int, y: int, i: int, j: int) -> bool:
        """Checks if the x, y collides entirely on the image"""
        image_x, image_y = 100 + i*self.image_size, 100 + j*self.image_size
        conditions = [
            (x >= image_x), (x+self.icon_size <= image_x+self.image_size),
            (y >= image_y), (y+self.icon_size <= image_y+self.image_size)
        ]
        return all(conditions)

    def reset(self) -> None:
        """Resets the UI for the game"""

        # DELETE PREVIOUS ELEMENTS
        for children in self.winfo_children():
            children.place_forget()

        # PLACE THE UI
        ttk.Button(self, text='Tutorial', command=self.show_tutorial, bootstyle='info', width=10).place(x=25, y=25)
        ttk.Label(self, text=f'Puntos: {self.wins}', font=self.font).place(x=400, y=25)
        if len(self.images) < 4: self.reset_images()
        random.shuffle(self.numbers)

    def render_game(self, *_) -> None:
        """Renders a new game"""

        # RESET CONFIGURATION EACH GAME
        self.answers = 0
        if not self.errors: self.wins += 1
        self.errors = False

        # CUSTOM ATTACH FUNCTION
        def attach(icon_, image_, image_index, icon_index) -> None:
            """Checks collision for the icon and its attached image"""
            icon_x, icon_y = icon_.winfo_x(), icon_.winfo_y()

            # GET COLISIONS
            collisions = [self.collide_rect(icon_x, icon_y, i%2, i//2) for i in range(4)]
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
            
            # PLACE ICON TO ITS ORIGINAL POSITION
            padding = (300-2*self.icon_size)
            icon_x, icon_y = padding + icon_index*self.icon_size, 700-padding-self.icon_size
            icon_.place(x=icon_x, y=icon_y)
            
        # DELETE PREVIOUS GAME
        self.reset()
        for i, icon_index in enumerate(self.numbers):

            # GET COORDINATES
            x, y = i%2, i//2
            image_x, image_y = 100 + x*self.image_size, 100 + y*self.image_size
            padding = (300-2*self.icon_size)
            icon_x, icon_y = padding + icon_index*self.icon_size, 700-padding-self.icon_size

            # GET IMAGE AND ICON
            image, _, traduction = self.images.pop(0) 
            icon = self.icons.pop(0)
            image.place(x=image_x, y=image_y)

            # ADD NEW FRAME TO RECEIVE AN IMAGE
            frame = tk.Frame(self, bg='red', highlightthickness=1, highlightbackground='green')
            tk.Label(frame, text=traduction, justify='center', wraplength=180).place(relx=0.5, rely=0.5, anchor='center')
            frame.pack_propagate(False)
            frame.place(x=image_x, y=image_y, width=self.image_size, height=self.image_size)
            frame.lift()

            # ADD THE ICON
            icon.place(x=icon_x, y=icon_y)
            command = lambda _, icon_=icon, image_=image, image_index=i, icon_index=icon_index: attach(icon_, image_, image_index, icon_index)
            icon.bind('<ButtonRelease-1>', command)


class Tutorial(ttk.Frame):
    def __init__(self, master: App, **kwargs):
        super().__init__(master, **kwargs)

        self.scale = 0.9
        self.image_size = 380
        self.font = ('Segoe UI', 16)

        self.inner_frame = tk.Frame(self, width=400, height=500)
        self.inner_frame.place(x=100, y=100, width=400, height=500)
        ttk.Button(self, text='Regresar...', bootstyle='danger', command=self.leave, width=10).place(x=25, y=25)
    
        self.index = 0
        self.images = [self.load_image(image_path) for image_path in master.images_paths]
        self.render_image()
        ttk.Button(self, text='<', command=self.previous_image).place(x=60, y=330, width=40, height=40)
        ttk.Button(self, text='>', command=self.previous_image).place(x=500, y=330, width=40, height=40)
            
    def previous_image(self) -> None:
        self.index = (self.index-1) % len(self.images)
        self.render_image()
    
    def next_image(self) -> None:
        self.index = (self.index+1) % len(self.images)
        self.render_image()

    def render_image(self) -> None:
        """Renders the current image"""
        for child in self.inner_frame.winfo_children(): child.pack_forget()
        image, name, traduction = self.images[self.index]
        ttk.Label(self.inner_frame, text=name, font=self.font).pack()
        ttk.Label(self.inner_frame, text=traduction, font=self.font).pack()
        image.pack()

    def leave(self) -> None:
        """Returns to the app"""
        self.place_forget()
    
    def load_image(self, image_name: str) -> tuple[Image, str, str]:
        """Loads an image with its traduction"""

        # LOADING IMAGE
        result = pil_image.new(mode='RGB', size=(self.image_size, self.image_size), color=(255, 255, 255))
        image = pil_image.open(f'{self.master.image_dir}/{image_name}')
        width, height = image.size

        # RESIZING IMAGE
        hwidth, hheight = int(width*self.scale), int(height*self.scale)
        image = image.resize((hwidth, hheight))

        # ADDING WHITE SPACE TO MAKE EACH IMAGE EQUAL SIZE
        x, y = (self.image_size-hwidth)//2, (self.image_size-hheight)//2
        result.paste(image, (x, y))
        image = Image(self.inner_frame)
        image.set_image(result)

        # GETTING TRADUCTION
        name = image_name.replace('.png', '').lower()
        return image, name.capitalize(), TRADUCTIONS[name]


if __name__ == '__main__':
    app = App(
        title='Signki By Javier Vazquez & Armando Chaparro 29/07/23',
        themename='darkly',
        resizable=(False, False),
        size=(600, 700)
    )

    app.place_window_center()
    app.mainloop()