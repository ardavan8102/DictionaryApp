from webbrowser import open as go
from googletrans import Translator

trans = Translator()

from flet import(
    Page, app,
    MainAxisAlignment, CrossAxisAlignment,
    Row, Column,
    AppBar, Dropdown, dropdown,
    Icon, icons,
    IconButton, FloatingActionButton, ButtonStyle,
    #PopupMenuButton, PopupMenuItem,
    Text, TextField, SnackBar,
    colors,
    NavigationRail, NavigationRailLabelType, NavigationRailDestination,
    VerticalDivider,
    AlertDialog, ElevatedButton, OutlinedButton, ProgressBar,
    Ref
)

class Refrences:
    GET_WORD = Ref[TextField]()
    FROM_LANG = Ref[Dropdown]()
    TO_LANG = Ref[Dropdown]()

def main(page: Page):
    
    page.title = "Dictionary Application"
    page.vertical_alignment = "center"

    
    page.window_width = 800
    page.window_height = 500
    page.window_resizable = False

    def toggleTheme(e):
        e.control.selected = not e.control.selected
        e.control.update()
       
       
    def openMsgBarAfterDeny():
        page.snack_bar = SnackBar(
            Text("Backed To Application, Enjoy !"),
            bgcolor = colors.GREEN_800,
        )
        page.snack_bar.open = True
        page.update()
      
        
      
    def getUserWord(e):
        user_word = Refrences.GET_WORD.current.value

        From_lang = Refrences.FROM_LANG.current.value

        To_lang = Refrences.TO_LANG.current.value
        
        Refrences.GET_WORD.current.value = ""
        Refrences.FROM_LANG.current.value = ""
        Refrences.TO_LANG.current.value = ""
        
        page.update()

        result = trans.translate(
            user_word,
            To_lang,
            From_lang
        )
        
        def close_dialog(e):
            trans_dialog.open = False
            page.update()
        
        
        trans_dialog = AlertDialog(
            modal = True,
            title = Text("Translation Is Done"),
            content = Text(f"{result.origin} ({result.src}) -> {result.text} ({result.dest})"),
            
            actions = [
                OutlinedButton(
                    "Cool, Thanks",
                    on_click = close_dialog,
                    icon = icons.CHECK,
                    icon_color = colors.GREEN_600
                ),
            ],
            actions_alignment = MainAxisAlignment.END,
        )
        
        def trans_dialog_open():
            page.dialog = trans_dialog
            trans_dialog.open = True
            page.update()
        
        trans_dialog_open()

        
          
    def window_event(e):
        if e.data == "close":
            page.dialog = confirm_dialog
            confirm_dialog.open = True
            page.update()

    page.window_prevent_close = True
    page.on_window_event = window_event


    def confirmExit(e):
        page.window_destroy()


    def denyExit(e):
        confirm_dialog.open = False
        page.update()
        openMsgBarAfterDeny()


    confirm_dialog = AlertDialog(
        modal = True,
        title = Text("Confirm Your Action"),
        content = Text("Do you Want To Exit Program?"),
        
        actions = [
            ElevatedButton(
                "Quit", 
                on_click = confirmExit,
                bgcolor = colors.RED_600,
                color = colors.WHITE
            ),
            OutlinedButton(
                "No, Stay", 
                on_click = denyExit,
                icon = icons.CHECK,
                icon_color = colors.GREEN_600
            ),
        ],
        actions_alignment = MainAxisAlignment.END,
    )
        
    
    page.appbar = AppBar(
        leading = Icon(icons.BOOKMARK),
        leading_width = 40,
        
        title = Text("Dictionary Application"),
        center_title = False,
        
        bgcolor = colors.SURFACE_VARIANT,
        
        actions = [
            IconButton(
                icon = icons.WB_SUNNY_OUTLINED,
                
                selected = False,
                selected_icon = icons.MODE_NIGHT,
                
                on_click = toggleTheme,
                tooltip = "Change Theme",
                
                style = ButtonStyle(
                    color = {
                        "selected" : colors.BLUE_400,
                        "" : colors.YELLOW_900
                    },
                ),
            ),
            
            IconButton(
                icon = icons.LINK_ROUNDED,
                icon_color = colors.CYAN_700,
                tooltip = "Github",
                on_click = lambda _: go("https://github.com/ardavan8102")
            ),
            
            
            IconButton(
                icon = icons.SETTINGS,
                tooltip = "Settings",
            ),
        ],
    )
    
    searchField = Row(
        controls = [
            TextField(
                ref = Refrences.GET_WORD,
                label = "Search A Word",
                hint_text = "Type Your Word ...",
            ),
            
            Dropdown(
                ref = Refrences.FROM_LANG,
                width = 120,
                label = "From",
                options = [
                    dropdown.Option("English"),
                    dropdown.Option("Persian"),
                    dropdown.Option("Spanish"),
                ],
            ),
            
            Dropdown(
                ref = Refrences.TO_LANG,
                width = 120,
                label = "To",
                options = [
                    dropdown.Option("English"),
                    dropdown.Option("Persian"),
                    dropdown.Option("Spanish"),
                ],
            ),
        ],
    )
    
    rail = NavigationRail(
        selected_index = 0,
        label_type = NavigationRailLabelType.ALL,
        
        min_width = 100,
        min_extended_width = 400,
        
        leading = FloatingActionButton(
            icon = icons.SEARCH_OUTLINED, 
            text = "Translate",
            on_click = getUserWord
        ),
        
        
        group_alignment = -0.9,
        
        destinations = [
            NavigationRailDestination(
                icon = icons.FAVORITE_BORDER, 
                selected_icon = icons.FAVORITE, 
                label = "Likes"
            ),
            
            NavigationRailDestination(
                icon_content = Icon(icons.BOOKMARK_BORDER),
                selected_icon_content = Icon(icons.BOOKMARK),
                label = "Saved",
            ),
        ]
    )

    page.add(
        
        
        Row(
            controls = [
                rail,
                VerticalDivider( width = 2 ),
                
                Row(
                    controls = [
                        
                        searchField,
                        
                    ], 
                    alignment = "spaceAround",
                    expand = True
                ),
            ],
            
            expand = True,
            
        )
    )


if __name__ == "__main__":
    app(target = main)