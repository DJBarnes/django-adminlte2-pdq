"""Django AdminLTE2 Views"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django_adminlte_2.decorators import requires_all_permissions, requires_one_permission


def home(request):
    """Show default home page"""
    return render(request, 'adminlte2/home.html', {})


def register(request):
    """Show default register page"""
    dummy_form = {
        'errors': None,
        'non_field_errors': None,
    }
    return render(request, 'registration/register.html', {
        'form': dummy_form,
    })


@requires_all_permissions(
    ['auth.add_group', 'auth.change_group', 'auth.delete_group']
)
def sample1(request):
    """Show default sample1 page"""
    return render(request, 'adminlte2/sample1.html', {})


@requires_one_permission(
    ['auth.add_permission', 'auth.change_permission', 'auth.delete_permission']
)
def sample2(request):
    """Show default sample2 page"""
    return render(request, 'adminlte2/sample2.html', {})

@login_required()
def demo_css(request):
    """Show examples of extra-features.css"""

    # Add messages to demo them.
    messages.set_level(request, messages.DEBUG)
    messages.debug(request, 'This is a debug message via the messages framework')
    messages.info(request, 'This is a info message via the messages framework')
    messages.success(request, 'This is a success message via the messages framework')
    messages.warning(request, 'This is a warning message via the messages framework')
    messages.error(request, 'This is a error message via the messages framework')
    messages.add_message(request, 50, 'This is an unknown level message via the messages framework')

    # Define the bootstrap "colors" to demo.
    bootstrap_types = [
        'default',
        'primary',
        'info',
        'success',
        'warning',
        'danger',

        'navy',
        'teal',
        'olive',
        'lime',
        'orange',
        'fuchsia',
        'indigo',
        'purple',
        'maroon',
        'gray',
        'black',
    ]
    return render(request, 'adminlte2/demo_css.html', {
        'bootstrap_types': bootstrap_types,
    })
