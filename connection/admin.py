from django.contrib import admin
from .models import Connection, UserConnectionIntermediateTable

admin.site.register(Connection)
admin.site.register(UserConnectionIntermediateTable)