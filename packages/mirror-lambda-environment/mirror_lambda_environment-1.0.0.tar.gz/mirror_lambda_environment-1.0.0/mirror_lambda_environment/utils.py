from simple_term_menu import TerminalMenu


def get_terminal_menu_selection(options: list, title: str = None, **settings):
    terminal_menu = TerminalMenu(options, title=title, **settings)
    menu_entry_index = terminal_menu.show()
    return menu_entry_index
