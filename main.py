from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
import socket
import webbrowser
from kivy.utils import platform

class NetworkMonitorApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_ip = "192.168.4.1"
        self.check_event = None

    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Status label
        self.status_label = Label(
            text='Waiting for network...',
            size_hint_y=None,
            height=50
        )
        
        # IP Address label
        self.ip_label = Label(
            text=f'Target IP: http://{self.target_ip}/',
            size_hint_y=None,
            height=50
        )
        
        # Open Browser button
        self.open_button = Button(
            text='Open in Browser',
            size_hint_y=None,
            height=60,
            disabled=True
        )
        self.open_button.bind(on_press=self.open_browser)
        
        # Add widgets to layout
        self.layout.add_widget(self.status_label)
        self.layout.add_widget(self.ip_label)
        self.layout.add_widget(self.open_button)
        
        # Start checking network
        self.check_event = Clock.schedule_interval(self.check_network, 2)
        
        return self.layout

    def check_network(self, dt):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            if self.status_label.text != 'Network Connected!':
                self.status_label.text = 'Network Connected!'
                self.open_button.disabled = False
                # Automatically open browser when connection is detected
                Clock.schedule_once(lambda dt: self.open_browser(None), 1)
        except OSError:
            self.status_label.text = 'Waiting for network...'
            self.open_button.disabled = True
    
    def open_browser(self, instance):
        try:
            webbrowser.open(f'http://{self.target_ip}/')
        except Exception as e:
            self.status_label.text = f'Error opening browser: {str(e)}'

    def on_stop(self):
        # Cleanup when app is closed
        if self.check_event:
            self.check_event.cancel()

if __name__ == '__main__':
    NetworkMonitorApp().run()
