"""Django AdminLTE2 Views"""
from django.contrib import messages
from django.shortcuts import render
from django_adminlte_2.decorators import (
    login_required,
    permission_required,
    permission_required_one,
)
from django_adminlte_2.forms import SampleForm


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

def sample_form(request):
    """Show sample form page"""
    form = SampleForm()
    form['sample_phone'].phone_info = {'pattern': r'\([0-9]{3}\) [0-9]{3}-[0-9]{4}', 'inputmask': '(999) 999-9999'}
    form['sample_range'].range_min_max = {'min':5, 'max':10}
    form['sample_color'].is_color = True
    form['sample_datalist'].datalist = {'name':'my_awesome_datalist', 'data': ('foo','bar')}

    return render(request, 'adminlte2/sample_form.html', {'form':form})

@permission_required(
    ['auth.add_group', 'auth.change_group', 'auth.delete_group']
)
def sample1(request):
    """Show default sample1 page"""
    return render(request, 'adminlte2/sample1.html', {})


@permission_required_one(
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
