from django.contrib import admin
from tracker.models import SiteUser
from tracker.models import Author
from tracker.models import Tag
from tracker.models import Folder
from tracker.models import ContentItem
from tracker.models import Link
from tracker.models import Author
from tracker.models import ConferenceTalk
from tracker.models import Completion

# Register your models here.
admin.site.register(SiteUser)
admin.site.register(Tag)
admin.site.register(Folder)
admin.site.register(ContentItem)
admin.site.register(Link)
admin.site.register(Author)
admin.site.register(ConferenceTalk)
admin.site.register(Completion)