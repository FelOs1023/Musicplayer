from playwright.sync_api import sync_playwright
import time, os, pyautogui, threading, json
#import config
import gui

CONFIG_FILE = "Musicplayer/data/playlist.json"

PROFILE_DIR = os.path.join("Musicplayer", "data", "ytmusic_profile")
os.makedirs(PROFILE_DIR, exist_ok=True)

def load_playlist():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            daten = json.load(f)
    except FileNotFoundError:
        return {}
    
    return daten.get("PLAYLIST", {})

class Music:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.playlists = load_playlist()
        self.player = self

    def start_browser(self):
        if not self.browser:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch_persistent_context(
                user_data_dir=PROFILE_DIR,
                headless=False,
                args=[
                    "--start-maximized",
                    "--disable-blink-features=AutomationControlled"
                ]
            )
    
    def play_playlist(self, url: str, shuffle: bool= False):
        self.start_browser()
        page = self.browser.new_page()
        page.goto(url)
        time.sleep(3)

        if shuffle:
            self.press_option()
            self.shuffle_play()
            self.shrink()
            time.sleep(1)
            self.player_window()
        else:
            self.normal_play()
            self.shrink()
            time.sleep(1)
            self.player_window()

        time.sleep(3)
    
    def normal_play(self):
        PlayButton_Location = pyautogui.locateOnScreen("Musicplayer/assets/images/PlayButton.png", confidence=.8)
        if PlayButton_Location:
            pyautogui.moveTo(PlayButton_Location)
            pyautogui.click()

    def press_option(self):
        OptionButton_Location = pyautogui.locateOnScreen("Musicplayer/assets/images/OptionButton3.png", confidence=.8)
        if OptionButton_Location:
            center = pyautogui.center(OptionButton_Location)
            pyautogui.moveTo(center)
            pyautogui.click()
            time.sleep(2)

    def shuffle_play(self):
        ShuffleButton_Location = pyautogui.locateOnScreen("Musicplayer/assets/images/Shuffle.png", confidence=.8)
        if ShuffleButton_Location:
            center = pyautogui.center(ShuffleButton_Location)
            pyautogui.moveTo(center)
            pyautogui.click()

    def player_window(self):
        Player_Location = pyautogui.locateOnScreen("Musicplayer/assets/images/PlayerWindow.png", confidence=.7)
        if Player_Location:
            center = pyautogui.center(Player_Location)
            pyautogui.moveTo(center)
            pyautogui.click()

    def open_browser(self):
        Browser_Location = pyautogui.locateOnScreen("Musicplayer/assets/images/Chromium.png", confidence=.8)
        if Browser_Location:
            pyautogui.moveTo(Browser_Location)
            pyautogui.click()

    def shrink(self):
        ShrinkButton_Location = pyautogui.locateOnScreen("Musicplayer/assets/images/Shrink.png", confidence=.7)
        if ShrinkButton_Location:
            pyautogui.moveTo(ShrinkButton_Location)
            pyautogui.click()

    def check_command(self, command: str):
        playlist_name = None
        shuffle = False

        #Erkennt Playlist Namen
        for input_name in self.playlists:
            if input_name in command:
                playlist_name = input_name
                break

        #Erkennt Shuffle Auswahl
        shuffle_keywords = ["shuffle", "random", "zufall", "zufällig"]
        if any(word in command.lower() for word in shuffle_keywords):
            shuffle = True

        return playlist_name, shuffle
    
    def music_command(self, command_input):
        if command_input in ["stop", "exit", "beenden"] :
            print("Programm beendet")
            return
        
        if command_input in ["help", "option", "commands", "eingabe", "hilfe"]:
            pass
        
        #Wirft den Input durch check_command und gibt das Ergebnis in die neuen Variablen
        input_playlist_name, input_shuffle = self.player.check_command(command_input)

        if input_playlist_name:
            url = self.playlists[input_playlist_name]
            self.player.play_playlist(url, shuffle=input_shuffle)
            gui_manager.log_message(f"Spiele: {input_playlist_name}", level='INFO')
        else:
            gui_manager.log_message("Playlist nicht gefunden", level='ERROR')

if __name__ == "__main__":
    player = Music()
    gui_manager = gui.GUI(command_handler=player.music_command, title="Music Player")
    gui_manager.run()

