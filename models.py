from django.db import models
from datetime import date

# Create your models here.

class Line(models.Model):
    number = models.CharField(max_length=3)
    line_type_choices = (
        ('s', 'S-Tog'),
        ('m', 'Metro'),
    )
    line_type = models.CharField(max_length=1, choices=line_type_choices)
    start = models.ForeignKey('Direction', blank=True, null=True, on_delete=models.CASCADE, related_name='start')
    end = models.ForeignKey('Direction', blank=True, null=True, on_delete=models.CASCADE, related_name='end')
    sequence_available = models.BooleanField(default=False)
    url = models.CharField(max_length=2000, null=True, blank=True)

    @property
    def line_id(self):
      return self.id

    @property
    def bvg_details(self):
        return None # TODO: to be implemented

    @property
    def name(self):
        return str(self.number)
 
    @property
    def css(self):
        return str.lower(self.line_type) + "line " + str(self.number)

    @property
    def css_prefix(self):
        return str(self.number)

    def __str__(self):
        return self.name
 
    class Meta:
        ordering = ['line_type', 'number']

#class StationOnLine(models.Model):
#    sequence = models.SmallIntegerField(null=True, blank=True)
#    liine = models.ForeignKey('Line', blank=True, null=True, on_delete=models.CASCADE)
#    staation = models.ForeignKey('Station', blank=True, null=True, on_delete=models.CASCADE)
    
class Direction(models.Model):
    name = models.CharField(max_length = 200)
    line = models.ForeignKey('Line', blank=True, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.line.name + "->" + self.name

    class Meta:
        ordering = ['line', 'name']

class Station(models.Model):
    name = models.CharField(max_length = 200)
    url_name = models.CharField(max_length = 200, null=True, blank=True)
    #liness = models.ManyToManyField('Line', through='StationOnLine', related_name='liness')
    lines = models.ManyToManyField('Line')
    bvg_details = models.CharField(max_length=2000, null=True, blank=True)  # DOT/DSB/Movia details
    bvg_pic = models.CharField(max_length=2000, null=True, blank=True)      # DOT/DSB/Movia map
    schema_pic = models.CharField(max_length=2000, null=True, blank=True)
    complete = models.BooleanField(default=False)
    change_station = models.BooleanField(default=False)
    sequence = models.BigIntegerField()
    lat = models.FloatField(default=0)
    lon = models.FloatField(default=0)
    db_station_name = models.CharField(max_length = 200, null=True, blank=True)

    def __str__(self):
        return self.name + " (" + ", ".join([i.name for i in self.lines.all()]) + ")"

    @property
    def station_id(self):
      return self.id

    @property
    def last_modified(self):
      return Change.objects.filter(at__exact=self.id).order_by('-updated_at').values('updated_at')[0]['updated_at']

    @property
    def count(self):
        return Change.objects.filter(at__exact=self.id).count()

    @property
    def nice_name(self):
        return self.name + "".join([ ("<span class='"+i.css+"'>"+i.name+"</span>") for i in self.lines.all()]) 

    class Meta:
        ordering = ['name']

class Change(models.Model):
    at = models.ForeignKey('Station', on_delete=models.CASCADE, blank=False)
    from_direction = models.ManyToManyField('Direction', related_name='from_direction')
    to_direction = models.ManyToManyField('Direction', related_name='to_direction')
    waggon_choices = (
        (1, 'rear'),
        (2, 'rear third'),
        (3, 'middle'),
        (4, 'front third'),
        (5, 'front'),
        (6, 'front or rear third'),
        (7, 'any'),
        (8, 'front or rear'),
        (9, 'front third, middle, or rear third'),
        (10, 'front third or front'),
        (11, 'rear third or rear'),
    )
    waggon = models.PositiveSmallIntegerField( choices = waggon_choices )
    email = models.EmailField(null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    comment = models.TextField(max_length=2000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    @property
    def waggon_template(self):
        return "umsteigen/waggon-" + str(self.waggon) + ".html"

    @property
    def direction_names(self):
        return " oder ".join([i.name for i in self.from_direction.all()])
    
    def __str__(self):
        return str(self.at) + ": " + ", ".join([str(i) for i in self.from_direction.all()]) + " ==to==> " + ", ".join([str(i) for i in self.to_direction.all()]) + ": " + str(self.waggon)

    class Meta:
        ordering = ['at']
