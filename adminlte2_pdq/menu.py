"""Django AdminLTE2 default Sidebar menu."""
from django.conf import settings

# Default Menu
MENU = [
    {
        'text': 'Home',
        'nodes': [
            {
                'route': getattr(settings, 'ADMINLTE2_HOME_ROUTE', 'adminlte2_pdq:home'),
                'text': 'Home',
                'icon': 'fa fa-dashboard',
            },
            {
                'route': 'adminlte2_pdq:demo-css',
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
                'route': 'adminlte2_pdq:sample_form',
                'text': 'Sample Form',
                'icon': 'fa fa-list-alt',
            },
            {
                'route': 'adminlte2_pdq:sample1',
                'text': 'Sample1',
                'icon': 'fa fa-group',
            },
            {
                'text': 'Sample Tree',
                'icon': 'fa fa-leaf',
                'nodes': [
                    {
                        'route': 'adminlte2_pdq:sample2',
                        'text': 'Sample2',
                        'icon': 'fa fa-building',
                    },
                ],
            },
        ],
    },
]
