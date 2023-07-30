import types


class Draggable:
    def __new__(cls, widget, just_droppable: bool=False, **kwargs):
        cls.__init__(cls, widget, just_droppable)
        return widget

    def __init__(self, widget, just_droppable: bool):
        self.widget = widget
        self.widget.bind('<Button-1>', self.on_drag_start)
        self.widget.bind('<B1-Motion>', self.on_drag_motion)

        self.widget.just_droppable = just_droppable
        self.widget.original_place = getattr(self.widget, 'place')
        self.widget.place = types.MethodType(self.place, self.widget)
        self.widget.origin_x, self.widget.origin_y = None, None

    def place(self, *args, **kwargs) -> None:
        self.original_place(*args, **kwargs)
        if self.origin_x is None: self.origin_x = self.winfo_x()
        if self.origin_y is None: self.origin_y = self.winfo_y()

    def on_drag_start(event) -> None:
        event.widget.lift()
        event.widget._drag_start_x = event.x
        event.widget._drag_start_y = event.y
        event.widget._origin_start_x = event.widget.winfo_x()
        event.widget._origin_start_y = event.widget.winfo_y()
    
    def on_drag_motion(event):
        x = event.widget.winfo_x() - event.widget._drag_start_x + event.x
        y = event.widget.winfo_y() - event.widget._drag_start_y + event.y
        event.widget.place(x=x, y=y)