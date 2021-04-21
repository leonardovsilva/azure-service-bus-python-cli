from python_console_menu import AbstractMenu, MenuItem

from queue_process import QueueProcess


class MainMenu(AbstractMenu):
    queue_process_obj = QueueProcess()

    def __init__(self):
        super().__init__("Azure Service Bus Python Explorer")

    def initialise(self):
        self.add_menu_item(MenuItem(100, "Exit").set_as_exit_option())
        self.add_menu_item(MenuItem(101, "Queue management - Spying message queue",
                                    lambda: MainMenu.queue_process_obj.spying_message_queue()))
        self.add_menu_item(MenuItem(102, "Topic management - Spying message queue", lambda: print("Hello World!")))

    def item_line(self, index: int, item: 'MenuItem'):
        return "%d: %s" % (index, self.item_text(item))
