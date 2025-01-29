from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.video import Video
import os
import shutil

# Paths
WHATSAPP_STATUS_DIR = "/storage/emulated/0/WhatsApp/Media/.Statuses"
DEFAULT_SAVE_DIR = "/storage/emulated/0/Muqtarik_Saved_Statuses"

# Helper Function to Save Files
def save_file(src):
    if not os.path.exists(DEFAULT_SAVE_DIR):
        os.makedirs(DEFAULT_SAVE_DIR)
    shutil.copy(src, DEFAULT_SAVE_DIR)

# Main App
class MuqtarikApp(App):
    def build(self):
        # Main Layout
        main_layout = BoxLayout(orientation="vertical")
        
        # Tabbed Panel
        panel = TabbedPanel(do_default_tab=False)
        
        # Images Tab
        images_tab = TabbedPanelItem(text="Images")
        images_tab.add_widget(self.create_status_view("Images"))
        panel.add_widget(images_tab)

        # Videos Tab
        videos_tab = TabbedPanelItem(text="Videos")
        videos_tab.add_widget(self.create_status_view("Videos"))
        panel.add_widget(videos_tab)

        # Add to Main Layout
        main_layout.add_widget(panel)
        return main_layout

    def create_status_view(self, content_type):
        scroll_view = ScrollView()
        content = BoxLayout(orientation="vertical", size_hint_y=None)
        content.bind(minimum_height=content.setter("height"))

        if not os.path.exists(WHATSAPP_STATUS_DIR):
            content.add_widget(Label(text="No statuses found!"))
        else:
            for file in os.listdir(WHATSAPP_STATUS_DIR):
                if content_type == "Images" and file.endswith((".jpg", ".png")):
                    content.add_widget(self.create_image_widget(file))
                elif content_type == "Videos" and file.endswith(".mp4"):
                    content.add_widget(self.create_video_widget(file))

        scroll_view.add_widget(content)
        return scroll_view

    def create_image_widget(self, file):
        layout = BoxLayout(orientation="vertical", size_hint_y=None, height=300)
        img = Image(source=os.path.join(WHATSAPP_STATUS_DIR, file), size_hint_y=None, height=200)
        save_btn = Button(text="Download", size_hint_y=None, height=50)
        save_btn.bind(on_press=lambda x: save_file(os.path.join(WHATSAPP_STATUS_DIR, file)))
        layout.add_widget(img)
        layout.add_widget(save_btn)
        return layout

    def create_video_widget(self, file):
        layout = BoxLayout(orientation="vertical", size_hint_y=None, height=300)
        vid = Video(source=os.path.join(WHATSAPP_STATUS_DIR, file), size_hint_y=None, height=200)
        save_btn = Button(text="Download", size_hint_y=None, height=50)
        save_btn.bind(on_press=lambda x: save_file(os.path.join(WHATSAPP_STATUS_DIR, file)))
        layout.add_widget(vid)
        layout.add_widget(save_btn)
        return layout


if __name__ == "__main__":
    MuqtarikApp().run()
