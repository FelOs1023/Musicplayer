from playwright.sync_api import sync_playwright
import time, os, pyautogui, threading
#import config
from gui import GUI

PROFILE_DIR = os.path.join(os.getcwd(), "ytmusic_profile")

class Play_Music:
    def __init__(self):
        self.playwright = None
        self.browser = None

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

    def play_playlist(self, url: str, shuffle: bool = False):
        self.start_browser()
        page = self.browser.new_page()
        page.goto(url)
        time.sleep(3)

        if shuffle:
            self.Press_Option()
            self.Shuffle_Play()
            self.Shrink()
            self.Player_Window()
        else:
            self.Normal_Play()
            self.Shrink()
            self.Player_Window()

        time.sleep(3)

    def Normal_Play(self):
        PlayButton_location = pyautogui.locateOnScreen("Quick_Actions/Buttons/PlayButton.png", confidence=0.8)
        if PlayButton_location:
            pyautogui.moveTo(PlayButton_location)
            pyautogui.click()

    def Press_Option(self):
        OptionButton_location = pyautogui.locateOnScreen("Quick_Actions/Buttons/OptionButton3.png", confidence=.8)
        if OptionButton_location:
            center = pyautogui.center(OptionButton_location)
            pyautogui.moveTo(center)
            pyautogui.click()
            time.sleep(3)

    def Shuffle_Play(self):
        ShuffleButton_location = pyautogui.locateOnScreen("Quick_Actions/Buttons/Shuffle.png", confidence=.8)
        if ShuffleButton_location:
            center = pyautogui.center(ShuffleButton_location)
            pyautogui.moveTo(center)
            pyautogui.click()

    def Player_Window(self):
        Player_location = pyautogui.locateOnScreen("Quick_Actions/Buttons/PlayerWindow.png", confidence=.8)
        if Player_location:
            center = pyautogui.center(Player_location)
            pyautogui.moveTo(center)
            pyautogui.click()

    def Open_Browser(self):
        Browser_Location = pyautogui.locateOnScreen("Quick_Actions/Buttons/Chromium.png", confidence=.8)
        if Browser_Location:
            pyautogui.moveTo(Browser_Location)
            pyautogui.click()

    def Shrink(self):
        ShrinkButton_location = pyautogui.locateOnScreen("Quick_Actions/Buttons/Shrink.png", confidence=0.7)
        if ShrinkButton_location:
            center = pyautogui.center(ShrinkButton_location)
            pyautogui.moveTo(center)
            pyautogui.click()

    @staticmethod
    def parse_command(command: str):
        #Analysiert den Befehl 
        playlist_name = None
        shuffle = False

        # Playlist erkennen
        for name in config.PLAYLISTS:
            if name in command:
                playlist_name = name
                break

        # Shuffle/Normal erkennen
        if "shuffle" in command or "zufällig" in command:
            shuffle = True

        return playlist_name, shuffle

    def music_command(input):
        player = Play_Music()

        if input in ["stop", "exit", "beenden"]:
            print("Programm beendet.")
            return
        
        if "speech" in input or "sprache" in input or "stimme" in input or "listen" in input:
            input = speech_prog.SpeechListener().listen(gui, prompt="Bitte sprechen Sie Ihren Musikbefehl...")
            if input:
                gui.log_message(f"Erkannter Musikbefehl: {input}", level='INFO')
            else:
                gui.log_message("Kein Musikbefehl erkannt.", level='WARN')
                return
            
        if input in ["eingabe", "option", "help", "commands"]:
            gui.log_message(config.HELP_MUSIC, level='INFO')

        playlist_name, shuffle = player.parse_command(input)

        if playlist_name:
            url = config.PLAYLISTS[playlist_name]
            player.play_playlist(url, shuffle=shuffle)
            gui.log_message(f"Spiele: {playlist_name}", level='INFO')

        if input in ["shrink", "klein", "weg", "gone"]:
            player.Shrink()
            gui.log_message("Browser verkleinert.", level='INFO')

        if input in ["open", "öffnen", "browser"]:
            player.Open_Browser()
            gui.log_message("Browser geöffnet.", level='INFO')

if __name__ == "__main__":
    gui = GUI(command_handler=Play_Music.music_command, title="Music Player")
    gui.run()

