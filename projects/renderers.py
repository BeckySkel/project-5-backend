# Code to hide PUT form when object does not exist from
# https://forum.djangoproject.com/t/django-rest-framework-404-not-found-put-delete/7980
from rest_framework.renderers import BrowsableAPIRenderer


class MyBrowsableAPIRenderer(BrowsableAPIRenderer):

    """
    Only render the browsable API if there is no 404 error
    """

    def get_context(self, *args, **kwargs):
        context = super().get_context(*args, **kwargs)

        response = args[2]['response']
        if response.status_code == 404 or response.status_code == 204:
            # do not display PUT form
            context['display_edit_forms'] = False

        return context

    def get_rendered_html_form(self, data, view, method, request):
        """
        {
            "detail": "Not found.
        }
        """
        try:
            if 'detail' in data:
                return
            return super().get_rendered_html_form(data, view, method,  request)
        except TypeError:
            return
