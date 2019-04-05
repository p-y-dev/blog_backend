from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.template.loader import render_to_string


def _get_description():
    context_data = {}
    return render_to_string("doc_swagger/doc_swagger.html", context_data)


swagger_schema_view = get_schema_view(
    openapi.Info(
        title='Документация Blog API',
        default_version='v1',
        description=_get_description(),
    ),
    public=False,
    permission_classes=(permissions.IsAdminUser,),
)
