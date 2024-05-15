"""
Tests for Admin Template Tags
"""

# Third-Party Imports.
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import User
from django.template import Template, Context
from django.test import TestCase, override_settings


class TemplateTagAdminTestCase(TestCase):
    """
    Test Template Tags
    """

    # |-------------------------------------------------------------------------
    # | Test index_app_display
    # |-------------------------------------------------------------------------

    @override_settings(ADMINLTE2_ADMIN_INDEX_USE_APP_LIST=False)
    def test_index_app_display_shows_box_when_setting_is_false(self):
        """Test index app display shows box when setting is false"""

        app = {
            "app_url": "/foo",
            "app_name": "foo",
            "name": "foo",
            "app_label": "foo",
            "models": [],
        }

        context = Context({"app": app})
        template_to_render = Template("{% load admin.admin_index %}" "{% index_app_display %}")

        rendered_template = template_to_render.render(context)

        self.assertIn('<div class="box-body">', rendered_template)
        self.assertNotIn('<table class="table table-hover table-striped">', rendered_template)

    @override_settings(ADMINLTE2_ADMIN_INDEX_USE_APP_LIST=True)
    def test_index_app_display_shows_list_when_setting_is_true(self):
        """Test index app display shows list when setting is true"""
        app = {
            "app_url": "/foo",
            "app_name": "foo",
            "name": "foo",
            "app_label": "foo",
            "models": [],
        }

        context = Context({"app": app})
        template_to_render = Template("{% load admin.admin_index %}" "{% index_app_display %}")

        rendered_template = template_to_render.render(context)

        self.assertIn('<table class="table table-hover table-striped">', rendered_template)
        self.assertNotIn('<div class="box-body">', rendered_template)

    # |-------------------------------------------------------------------------
    # | Test show_control_sidebar_button
    # |-------------------------------------------------------------------------

    def test_show_control_sidebar_button_shows_up_when_settings_are_left_as_default_tabs_to_show(self):
        """Test show control sidebar button shows up when settings are left as
        default tabs to show"""

        context = Context({})
        template_to_render = Template("{% load admin.admin_header %}" "{% show_control_sidebar_button %}")

        rendered_template = template_to_render.render(context)

        self.assertIn(
            '<a href="#" data-toggle="control-sidebar"><i class="fa fa-gears"></i></a>',
            rendered_template,
        )

    @override_settings(ADMINLTE2_ADMIN_CONTROL_SIDEBAR_TABS={"SHOW_SETTINGS_TAB": True, "SHOW_EXTRA_TABS": True})
    def test_show_control_sidebar_button_shows_up_when_settings_defines_all_tabs_to_show(self):
        """Test show control sidebar button shows up when settings defines all
        tabs to show"""

        context = Context({})
        template_to_render = Template("{% load admin.admin_header %}" "{% show_control_sidebar_button %}")

        rendered_template = template_to_render.render(context)

        self.assertIn(
            '<a href="#" data-toggle="control-sidebar"><i class="fa fa-gears"></i></a>',
            rendered_template,
        )

    @override_settings(ADMINLTE2_ADMIN_CONTROL_SIDEBAR_TABS={"SHOW_RECENT_ACTIVITY_TAB": False})
    def test_show_control_sidebar_button_is_missing_when_settings_hides_all_tabs_to_show(self):
        """Test show control sidebar button is missing when settings hides all tabs to show"""
        context = Context({})
        template_to_render = Template("{% load admin.admin_header %}" "{% show_control_sidebar_button %}")

        rendered_template = template_to_render.render(context)

        self.assertNotIn(
            '<a href="#" data-toggle="control-sidebar"><i class="fa fa-gears"></i></a>',
            rendered_template,
        )

    # |-------------------------------------------------------------------------
    # | Test show_control_sidebar_recent_activity_tab_pane
    # |-------------------------------------------------------------------------

    def test_show_control_sidebar_recent_activity_tab_pane_displays_when_setting_is_default(self):
        """Test show control sidebar recent activity tab pane displays when
        setting is default"""

        user = User()

        context = Context(
            {
                "user": user,
                "log_entries": LogEntry.objects.none(),
            }
        )
        template_to_render = Template(
            "{% load admin.admin_control_sidebar %}" "{% show_control_sidebar_recent_activity_tab_pane %}"
        )

        rendered_template = template_to_render.render(context)

        self.assertIn("None available", rendered_template)

    @override_settings(ADMINLTE2_ADMIN_CONTROL_SIDEBAR_TABS={"SHOW_RECENT_ACTIVITY_TAB": True})
    def test_show_control_sidebar_recent_activity_tab_pane_displays_when_setting_is_true(self):
        """Test show control sidebar recent activity tab pane displays when
        setting is true"""

        user = User()

        context = Context(
            {
                "user": user,
                "log_entries": LogEntry.objects.none(),
            }
        )
        template_to_render = Template(
            "{% load admin.admin_control_sidebar %}" "{% show_control_sidebar_recent_activity_tab_pane %}"
        )

        rendered_template = template_to_render.render(context)

        self.assertIn("None available", rendered_template)

    @override_settings(ADMINLTE2_ADMIN_CONTROL_SIDEBAR_TABS={"SHOW_RECENT_ACTIVITY_TAB": False})
    def test_show_control_sidebar_recent_activity_tab_pane_is_hidden_when_setting_is_false(self):
        """Tests show control sidebar recent activity tab pane is hidden when
        setting is false"""

        user = User()

        context = Context({"user": user})
        template_to_render = Template(
            "{% load admin.admin_control_sidebar %}" "{% show_control_sidebar_recent_activity_tab_pane %}"
        )

        rendered_template = template_to_render.render(context)

        self.assertNotIn("None available", rendered_template)

    # |-------------------------------------------------------------------------
    # | Test show_control_sidebar_settings_tab_pane
    # |-------------------------------------------------------------------------

    def test_show_control_sidebar_settings_tab_pane_is_hidden_when_setting_is_default(self):
        """Test show control sidebar settings tab pane is hidden when setting
        is default"""

        context = Context({})
        template_to_render = Template(
            "{% load admin.admin_control_sidebar %}" "{% show_control_sidebar_settings_tab_pane %}"
        )

        rendered_template = template_to_render.render(context)

        self.assertNotIn('<h3 class="control-sidebar-heading">General Settings</h3>', rendered_template)

    @override_settings(ADMINLTE2_ADMIN_CONTROL_SIDEBAR_TABS={"SHOW_SETTINGS_TAB": True})
    def test_show_control_sidebar_settings_tab_pane_displays_when_setting_is_true(self):
        """Test show control sidebar settings tab pane displays when setting
        is true"""

        context = Context({})
        template_to_render = Template(
            "{% load admin.admin_control_sidebar %}" "{% show_control_sidebar_settings_tab_pane %}"
        )

        rendered_template = template_to_render.render(context)

        self.assertIn('<h3 class="control-sidebar-heading">General Settings</h3>', rendered_template)

    @override_settings(ADMINLTE2_ADMIN_CONTROL_SIDEBAR_TABS={"SHOW_SETTINGS_TAB": False})
    def test_show_control_sidebar_settings_tab_pane_is_hidden_when_setting_is_false(self):
        """Test show control sidebar settings tab pane is hidden when setting
        is false"""

        context = Context({})
        template_to_render = Template(
            "{% load admin.admin_control_sidebar %}" "{% show_control_sidebar_settings_tab_pane %}"
        )

        rendered_template = template_to_render.render(context)

        self.assertNotIn('<h3 class="control-sidebar-heading">General Settings</h3>', rendered_template)

    # |-------------------------------------------------------------------------
    # | Test show_control_sidebar_extra_tab_panes
    # |-------------------------------------------------------------------------

    def test_show_control_sidebar_extra_tab_panes_is_hidden_when_setting_is_default(self):
        """Test show control sidebar extra tab panes is hidden when setting
        is default"""

        context = Context({})
        template_to_render = Template(
            "{% load admin.admin_control_sidebar %}" "{% show_control_sidebar_extra_tab_panes %}"
        )

        rendered_template = template_to_render.render(context)

        self.assertNotIn('<h3 class="control-sidebar-heading">Extra Tab</h3>', rendered_template)

    @override_settings(ADMINLTE2_ADMIN_CONTROL_SIDEBAR_TABS={"SHOW_EXTRA_TABS": True})
    def test_show_control_sidebar_extra_tab_panes_displays_when_setting_is_true(self):
        """Test show control sidebar extra tab panes displays when setting is true"""

        context = Context({})
        template_to_render = Template(
            "{% load admin.admin_control_sidebar %}" "{% show_control_sidebar_extra_tab_panes %}"
        )

        rendered_template = template_to_render.render(context)

        self.assertIn('<h3 class="control-sidebar-heading">Extra Tab</h3>', rendered_template)

    @override_settings(ADMINLTE2_ADMIN_CONTROL_SIDEBAR_TABS={"SHOW_EXTRA_TABS": False})
    def test_show_control_sidebar_extra_tab_panes_is_hidden_when_setting_is_false(self):
        """Test show control sidebar extra tab panes is hidden when setting is false"""

        context = Context({})
        template_to_render = Template(
            "{% load admin.admin_control_sidebar %}" "{% show_control_sidebar_extra_tab_panes %}"
        )

        rendered_template = template_to_render.render(context)

        self.assertNotIn('<h3 class="control-sidebar-heading">Extra Tab</h3>', rendered_template)

    # |-------------------------------------------------------------------------
    # | Test show_control_sidebar_tabs
    # |-------------------------------------------------------------------------

    @override_settings(ADMINLTE2_ADMIN_CONTROL_SIDEBAR_TABS={"SHOW_SETTINGS_TAB": True, "SHOW_EXTRA_TABS": True})
    def test_show_control_sidebar_tabs_displays_the_enabled_tabs_as_tabs_when_there_is_more_than_one(self):
        """Test show control sidebar tabs displays the enabled tabs as tabs when
        there is more than one"""

        context = Context({})
        template_to_render = Template("{% load admin.admin_control_sidebar %}" "{% show_control_sidebar_tabs %}")

        rendered_template = template_to_render.render(context)

        self.assertIn('<ul class="nav nav-tabs nav-justified control-sidebar-tabs">', rendered_template)

    def test_show_control_sidebar_tabs_displays_the_enabled_tab_by_itself_and_not_as_a_tab_when_there_is_only_one(self):
        """Test show control sidebar tabs displays the enabled tab by itself and
        not as a tab when there is only one"""

        context = Context({})
        template_to_render = Template("{% load admin.admin_control_sidebar %}" "{% show_control_sidebar_tabs %}")

        rendered_template = template_to_render.render(context)

        self.assertNotIn('<ul class="nav nav-tabs nav-justified control-sidebar-tabs">', rendered_template)
