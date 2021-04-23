import main_menu
import config
import time

if __name__ == '__main__':
    config_obj = config.Config()
    config_obj.init()
    time.sleep(0.1)
    mainMenu = main_menu.MainMenu()
    mainMenu.display()

