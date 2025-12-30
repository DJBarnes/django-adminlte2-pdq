"""
Custom menu definition, for testing proper rendering of sidebar menu, such as
cases when the following variables are used:
* ADMINLTE2_MENU_FIRST
* ADMINLTE2_MENU
* Admin_Menu
* ADMINLTE2_MENU_LAST
"""

# Custom Menu definition for testing ADMINLTE2_MENU_FIRST.
CUSTOM_MENU_FIRST = [
    {
        "text": "Custom Menu - First",
        "nodes": [
            {
                "route": "adminlte2_pdq:home",
                "text": "[First] Custom Url 1",
                "icon": "fa fa-dashboard",
            },
            {
                "route": "adminlte2_pdq:home",
                "text": "[First] Custom Url 2",
                "icon": "fa fa-user",
            },
        ],
    },
]


# Custom Menu definition for testing ADMINLTE2_MENU.
CUSTOM_MENU_STANDARD = [
    {
        "text": "Custom Menu - Standard",
        "nodes": [
            {
                "route": "adminlte2_pdq:home",
                "text": "[Standard] Custom Url 1",
                "icon": "fa fa-dashboard",
            },
            {
                "route": "adminlte2_pdq:home",
                "text": "[Standard] Custom Url 2",
                "icon": "fa fa-user",
            },
        ],
    },
]


# Custom Menu definition for testing ADMINLTE2_MENU_LAST.
CUSTOM_MENU_LAST = [
    {
        "text": "Custom Menu - Last",
        "nodes": [
            {
                "route": "adminlte2_pdq:home",
                "text": "[Last] Custom Url 1",
                "icon": "fa fa-dashboard",
            },
            {
                "route": "adminlte2_pdq:home",
                "text": "[Last] Custom Url 2",
                "icon": "fa fa-user",
            },
        ],
    },
]
