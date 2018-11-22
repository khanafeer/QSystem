from django.contrib import admin

from core_app.models import Service,Terminal,ServiceUser,Queue,QueLog,TerminalUser



admin.site.register(ServiceUser)
admin.site.register(Service)
admin.site.register(Terminal)
admin.site.register(TerminalUser)
admin.site.register(Queue)

class LogAdmin(admin.ModelAdmin):
    list_filter = ('service', 'terminal','user')
    list_display = ['id','num','service','terminal','user','date_join']
admin.site.register(QueLog,LogAdmin)


