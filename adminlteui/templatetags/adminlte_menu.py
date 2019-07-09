import logging

import django
from django import template
from django.contrib.admin import AdminSite
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from adminlteui.templatetags.adminlte_options import get_adminlte_option
from adminlteui.models import Menu

try:
    from django.urls import reverse, resolve
except:
    from django.core.urlresolvers import reverse, resolve

register = template.Library()

if django.VERSION < (1, 9):
    simple_tag = register.assignment_tag
else:
    simple_tag = register.simple_tag


def get_reverse_link(link):
    if not link or '/' in link:
        return link

    try:
        return reverse(link)
    except Exception as e:
        return None


def get_custom_menu(request):
    """
    use content_type and user.permission control the menu

    `label:model`

    :param request:
    :return:
    """
    all_permissions = request.user.get_all_permissions()

    limit_for_interval_link = []
    for permission in all_permissions:
        app_label = permission.split('.')[0]
        model = permission.split('.')[1].split('_')[1]
        limit_for_interval_link.append('{}:{}'.format(app_label, model))

    limit_for_interval_link = set(limit_for_interval_link)
    new_available_apps = []
    menu = Menu.dump_bulk()
    for menu_item in menu:
        new_available_apps_item = {}
        data = (menu_item.get('data'))
        if data.get('valid') is False:
            continue

        new_available_apps_item['name'] = data.get('name')
        new_available_apps_item['icon'] = data.get('icon')

        children = menu_item.get('children')
        if not children:
            # skip menu_item that no children and link type is devide.
            if data.get('link_type') in (0, 1):
                new_available_apps_item['admin_url'] = get_reverse_link(
                    data.get('link'))
                new_available_apps.append(new_available_apps_item)
            continue
        new_available_apps_item['models'] = []

        for children_item in children:
            if children_item.get('data').get('link_type') == 0:
                # interval link should connect a content_type, otherwise it will be hide.
                if children_item.get('data').get('content_type'):
                    obj = ContentType.objects.get(id=children_item.get('data').get('content_type'))
                    # if user hasn't permission, the model will be skip.
                    if obj.app_label + ':' + obj.model not in limit_for_interval_link:
                        continue
                else:
                    continue

            if children_item.get('data').get('valid') is False:
                continue
            new_children_item = {}
            new_children_item['name'] = children_item.get('data').get('name')
            new_children_item['admin_url'] = get_reverse_link(
                children_item.get('data').get('link')
            )
            if not new_children_item['admin_url']:
                continue
            new_children_item['icon'] = children_item.get('data').get('icon')
            # new_children_item['admin_url'] = children_item.get('link')
            new_available_apps_item['models'].append(new_children_item)
        if new_available_apps_item['models']:
            new_available_apps.append(new_available_apps_item)

    return new_available_apps


@simple_tag(takes_context=True)
def get_menu(context, request):
    """
    :type request: WSGIRequest
    """
    if not isinstance(request, HttpRequest):
        return None

    use_custom_menu = get_adminlte_option('USE_CUSTOM_MENU')
    if use_custom_menu.get('USE_CUSTOM_MENU',
                           '0') == '1' and use_custom_menu.get('valid') is True:
        return get_custom_menu(request)

    # Django 1.9+
    available_apps = context.get('available_apps')
    if not available_apps:

        # Django 1.8 on app index only
        available_apps = context.get('app_list')

        # Django 1.8 on rest of the pages
        if not available_apps:
            try:
                from django.contrib import admin
                template_response = get_admin_site(request.current_app).index(
                    request)
                available_apps = template_response.context_data['app_list']
            except Exception:
                pass
    if not available_apps:
        logging.warn('adminlteui was unable to retrieve apps list for menu.')

    for app in available_apps:
        if app.get('app_label') == 'django_admin_settings':
            app.get('models').insert(0,
                                     {
                                         'name': _('General Option'),
                                         'object_name': 'Options',
                                         'perms':
                                             {
                                                 'add': True,
                                                 'change': True,
                                                 'delete': True,
                                                 'view': True
                                             },
                                         'admin_url': reverse(
                                             'admin:general_option'),
                                         'view_only': False
                                     }
                                     )
    # return MenuManager(available_apps, context, request)
    return available_apps


def get_admin_site(current_app):
    """
    Method tries to get actual admin.site class, if any custom admin sites
    were used. Couldn't find any other references to actual class other than
    in func_closer dict in index() func returned by resolver.
    """
    try:
        resolver_match = resolve(reverse('%s:index' % current_app))
        # Django 1.9 exposes AdminSite instance directly on view function
        if hasattr(resolver_match.func, 'admin_site'):
            return resolver_match.func.admin_site

        for func_closure in resolver_match.func.__closure__:
            if isinstance(func_closure.cell_contents, AdminSite):
                return func_closure.cell_contents
    except:
        pass
    from django.contrib import admin
    return admin.site
