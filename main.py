import main_menu
import config

if __name__ == '__main__':
    config_obj = config.Config()
    config_obj.init()
    mainMenu = main_menu.MainMenu()
    mainMenu.display()

