"""Django AdminLTE2 default Sidebar menu."""
from django.conf import settings

# Default Menu
MENU = [
    {
        'text': 'Home',
        'nodes': [
            {
                'route': getattr(settings, 'ADMINLTE2_HOME_ROUTE', 'django_adminlte_2:home'),
                'text': 'Home',
                'icon': 'fa fa-dashboard',
            },
            {
                'route': 'django_adminlte_2:demo-css',
                'text': 'Demo CSS',
                'icon': 'fa fa-file'
            },
        ]
    },
    {
        'text': 'Profile',
        'nodes': [
            {
                'route': 'password_change',
                'text': 'Change Password',
                'icon': 'fa fa-lock'
            }
        ]
    },
    {
        'text': 'Samples',
        'nodes': [
            {
                'route': 'django_adminlte_2:sample1',
                'text': 'Sample1',
                'icon': 'fa fa-group',
            },
            {
                'text': 'Sample Tree',
                'icon': 'fa fa-leaf',
                'nodes': [
                    {
                        'route': 'django_adminlte_2:sample2',
                        'text': 'Sample2',
                        'icon': 'fa fa-building',
                    },
                ],
            },
        ],
    },
]

# Default Whitelist
WHITELIST = [
    'password_change',
    'django_adminlte_2:register',
    'django_adminlte_2:demo-css',
]
