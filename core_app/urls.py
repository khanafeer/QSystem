from django.conf.urls import url
from core_app.views import ServiceView,TerminalView,UserView
from core_app.views import new_queue_cust,call_queue_client,servcice_que,change_terminal,user_terminal,reports,report_detailed

urlpatterns = [
    url(r'^services/', ServiceView.as_view()),
    url(r'^terminals/', TerminalView.as_view()),
    url(r'^users/', UserView.as_view()),
    url(r'^new-client/', new_queue_cust),
    url(r'^call-client/', call_queue_client),
    url(r'^change-terminal/', change_terminal),
    url(r'^get-terminal/', user_terminal),
    url(r'^service-queue/', servcice_que),
    url(r'^general-report/', reports),
    url(r'^detailed-report/', report_detailed),
]
