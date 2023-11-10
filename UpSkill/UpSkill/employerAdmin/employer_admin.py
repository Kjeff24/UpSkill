from django.contrib.admin import AdminSite

class MyAdminSite(AdminSite):
    """
    Custom admin site for U employers.

    :site_header: The header displayed on the admin site. :noindex:
    :site_title: The title displayed on the admin site. :noindex:
    :login_template: The template used for the admin login page. :noindex:
    """
    site_header = 'UpSkill Tutor Administration'
    site_title = 'Upskill Tutor Administration'
    login_template = 'admin/login.html'

tutor_admin_site = MyAdminSite(name='tutor_admin')