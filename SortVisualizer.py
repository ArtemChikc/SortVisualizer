from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Line
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.metrics import dp
from kivy.properties import StringProperty, ListProperty
import random
import threading
import time
import copy

import sorting_algorithms



class SortVisualizer(Widget):
    sort_name = StringProperty("None")
    border_color = ListProperty([0.9, 0.9, 0.9, 1])


    def __init__(self, index, **kwargs):
        super().__init__(**kwargs)
        self.data = []
        self.index = index
        self.size_hint = (1, 0.2)
        self.bind(pos=self._update_canvas, size=self._update_canvas)

        self._label = Label(
            text=self.sort_name, 
            size_hint=(None, None),
            size=(self.width, dp(25)),
            pos=(self.x + dp(10), self.y + self.height - dp(25)),
            color=(1, 1, 1, 1),
            bold=True,
            halign='left',
            valign='middle')
        self.add_widget(self._label)


    def update_data(self, data):
        self.data = data.copy()
        self._update_canvas()


    def _update_canvas(self, *args):
        self.canvas.before.clear()
        self.canvas.after.clear()

        border_padding = dp(2)
        with self.canvas.before:
            Color(*self.border_color)
            Line(rectangle=(
                self.x + border_padding,
                self.y + border_padding,
                self.width - border_padding*2,
                self.height - border_padding*2
            ), width=border_padding)

        if not self.data:
            return

        bar_area_height = self.height - dp(40)
        bar_spacing = dp(0.5)

        available_width = self.width - 6 * border_padding
        total_bars = len(self.data)

        total_spacing = bar_spacing * (total_bars - 1)
        bar_width = (available_width - total_spacing) / total_bars

        max_val = max(self.data)

        with self.canvas.after:
            for i, val in enumerate(self.data):
                hue = val / total_bars
                Color(hue, 0.8, 0.8, mode='hsv')
                bar_height = (val / max_val) * bar_area_height

                x_pos = self.x + border_padding*3 + i*(bar_width + bar_spacing)
                y_pos = self.y + border_padding + dp(3)

                Rectangle(
                    pos=(x_pos, y_pos),
                    size=(bar_width, bar_height))

        self._label.text = self.sort_name
        self._label.pos = (self.x + dp(10), self.y + self.height - dp(25))
        self._label.size = (self.width - dp(20), dp(20))



class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.N = 50
        self.INTERVAL = 0.05
        self.sorting = False
        self.threads = []
        self.lock = threading.Lock()


    def build(self):
        self.title = "SortVisualizer by B1t0ne"
        main_layout = BoxLayout(orientation='vertical')

        top_panel = BoxLayout(size_hint=(1, None), height=dp(30))
        top_panel.add_widget(Label(text="SortVisualizer by B1t0ne",
                                   size_hint=(1, 1), halign='center', valign='middle'))

        size_layout = BoxLayout(orientation='horizontal', size_hint=(1, 1))
        size_layout.add_widget(Label(text="Array Size:", size_hint=(None, 1), width=dp(75)))
        self.size_input = TextInput(text=str(self.N), multiline=False, size_hint=(None, 1))
        size_layout.add_widget(self.size_input)
        top_panel.add_widget(size_layout)

        interval_layout = BoxLayout(orientation='horizontal', size_hint=(1, 1))
        interval_layout.add_widget(Label(text="Interval (sec):", size_hint=(None, 1), width=dp(90)))
        self.interval_input = TextInput(text=str(self.INTERVAL), multiline=False, size_hint=(None, 1))
        interval_layout.add_widget(self.interval_input)
        top_panel.add_widget(interval_layout)

        main_layout.add_widget(top_panel)

        button_panel = BoxLayout(size_hint=(1, None), height=dp(50))
        button_panel.add_widget(Button(text='Generate', on_press=self.generate))
        button_panel.add_widget(Button(text='Sort', on_press=self.start_sort))
        main_layout.add_widget(button_panel)

        self.visualizers = []
        visualizers_layout = BoxLayout(orientation='vertical')

        for i in range(4):
            algo_name = random.choice(list(sorting_algorithms.SORT_ALGORITHMS.keys()))
            vis = SortVisualizer(index=i)
            vis.sort_name = algo_name
            vis.bind(on_touch_down=self.on_visualizer_click)
            self.visualizers.append(vis)
            visualizers_layout.add_widget(vis)

        main_layout.add_widget(visualizers_layout)
        self.generate()
        return main_layout


    def on_visualizer_click(self, visualizer, touch):
        if not visualizer.collide_point(*touch.pos) or self.sorting:
            return

        dropdown = DropDown()
        for algo in sorting_algorithms.SORT_ALGORITHMS:
            btn = Button(text=algo, size_hint_y=None, height=dp(40))
            btn.bind(on_release=lambda b: self._select_algorithm(dropdown, visualizer, b.text))
            dropdown.add_widget(btn)
        dropdown.open(visualizer)


    def _select_algorithm(self, dropdown, visualizer, algo):
        visualizer.sort_name = algo
        dropdown.dismiss()


    def generate(self, *args):
        self.N = int(self.size_input.text)
        self.stop_sort()
        self.data = [i for i in range(1, self.N+1)]
        random.shuffle(self.data)
        for vis in self.visualizers:
            vis.update_data(self.data)


    def start_sort(self, *args):
        if self.sorting:
            return
        self.sorting = True
        self.threads = []

        for vis in self.visualizers:
            if vis.sort_name not in sorting_algorithms.SORT_ALGORITHMS:
                continue

            data_copy = copy.deepcopy(self.data)
            generator = sorting_algorithms.SORT_ALGORITHMS[vis.sort_name](data_copy)

            thread = threading.Thread(
                target=lambda v=vis, d=data_copy, g=generator: self.sort_thread(v, d, g))
            thread.daemon = True
            self.threads.append(thread)
            thread.start()


    def sort_thread(self, vis, data_copy, generator):
        try:
            for _ in generator:
                with self.lock:
                    vis.data = copy.deepcopy(data_copy)
                Clock.schedule_once(lambda dt: vis._update_canvas())
                time.sleep(float(self.interval_input.text))
        except Exception as e:
            print(f"Error in {vis.sort_name}: {str(e)}")
        finally:
            Clock.schedule_once(lambda dt: self.check_all_done())


    def check_all_done(self):
        with self.lock:
            alive = any(t.is_alive() for t in self.threads)
            if not alive:
                self.sorting = False


    def stop_sort(self, *args):
        self.sorting = False
        self.threads = []



if __name__=='__main__':
    MainApp().run()