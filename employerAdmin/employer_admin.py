from django.contrib.admin import AdminSite

class MyAdminSite(AdminSite):
    """
    Custom admin site for SkillBuilder employers.

    :site_header: The header displayed on the admin site. :noindex:
    :site_title: The title displayed on the admin site. :noindex:
    :login_template: The template used for the admin login page. :noindex:
    """
    site_header = 'SkillBuilder Employer Administration'
    site_title = 'SkillBuilder Employer Administration'
    login_template = 'admin/login.html'

employer_admin_site = MyAdminSite(name='employer_admin')