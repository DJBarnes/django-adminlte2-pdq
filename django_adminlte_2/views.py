"""Django AdminLTE2 Views"""
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
