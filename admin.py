from django.contrib import admin
#from import_export.admin import ImportExportMixin

# Register your models here.
from .models import Line
from .models import Station
from .models import Direction
from .models import Change
#from .models import StationOnLine

class ChangeAdmin(admin.ModelAdmin):
  list_display = ('__str__', 'name', 'updated_at')

class StationAdmin(admin.ModelAdmin):
  list_display = ('__str__', 'complete', 'schema_pic', 'lat', 'lon')
  list_filter = ['change_station', 'complete']


admin.site.register(Line)
#admin.site.register(Station)
admin.site.register(Station, StationAdmin)
#admin.site.register(StationOnLine)
admin.site.register(Direction)
admin.site.register(Change, ChangeAdmin)

admin.site.site_header = "Umsteigen - Administration"
