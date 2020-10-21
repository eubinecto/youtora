from django.contrib import admin

from youtora.collect.models import ChannelRaw, VideoRaw, TracksRaw, IdiomRaw

# Register your models here.
admin.site.register(ChannelRaw)
admin.site.register(VideoRaw)
admin.site.register(TracksRaw)
admin.site.register(IdiomRaw)
