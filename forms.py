from django import forms
from django.db.models import Q

from .models import Station
from .models import Line
from .models import Change
from .models import Direction

class AddChange(forms.ModelForm):
    class Meta:
        model = Change
        fields = ('__all__')
        labels = { 
            'at': 'Station',
            'from_direction': 'Direction of travel',
            'to_direction': 'Transfer to',
            'waggon': 'Boarding position',
            'name': 'Thanks to (optional)',
            'email': 'Email (optional, for inquiries)',
            'comment': 'Comment (optional)',
            }
        widgets = {
            'at': forms.HiddenInput(),
            }

    def __init__(self, station, *args, **kwargs):
        super(AddChange, self).__init__(*args, **kwargs)
        lines = Line.objects.filter(id__in=station.lines.all())
        self.fields['at'].queryset = Station.objects.filter(id=station.id)
        self.fields['from_direction'].queryset = Direction.objects.filter( Q(id__in=lines.values_list('start', flat=True)) | Q(id__in=lines.values_list('end', flat=True)))
        self.fields['to_direction'].queryset = Direction.objects.filter( Q(id__in=lines.values_list('start', flat=True)) | Q(id__in=lines.values_list('end', flat=True)))
