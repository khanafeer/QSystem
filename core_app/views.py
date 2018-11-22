from django.shortcuts import render
from django.utils.timezone import datetime

from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from core_app.models import Service
from core_app.serializers import ServiceSerializer,QlogSerializer,UserSerializer,TerminalSerializer,DetailedSerializer
from core_app.models import Queue,QueLog,Terminal,TerminalUser,User
from django.db.models import Q
import json

class ServiceView(APIView):
    def get(self,request):
        s = Service.objects.all()
        ser = ServiceSerializer(s,many=True)
        return Response(ser.data)

class TerminalView(APIView):
    def get(self,request):
        s = Terminal.objects.all()
        ser = TerminalSerializer(s,many=True)
        return Response(ser.data)

class UserView(APIView):
    def get(self,request):
        s = User.objects.all()
        ser = UserSerializer(s,many=True)
        return Response(ser.data)

@api_view(['POST'])
def new_queue_cust(request):
    if request.method == 'POST':
        d = request.data['service']
        try:
            service = Service.objects.get(name=d)
            start = service.start
            end = service.end
            last = Queue.objects.last(service)
            if last:
                print(last.num)
                new = last.num + 1
                new = new if start <= new <= end else start
            else:
                new = start
            Queue.objects.enqueue(service=service,num=new)
            return Response({'status': True,'num':new,'date':datetime.now()}, status.HTTP_200_OK)
        except Service.DoesNotExist:
            return Response({'status':False},status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            print(ex)
            return Response({'status':False},status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def call_queue_client(request):
    if request.method == 'GET':
        try:
            current_terminal = TerminalUser.objects.get(user=request.user).terminal

            current_queue = Queue.objects.dequeue(current_terminal.service)
            if current_queue:
                log = QueLog(service=current_terminal.service, user=request.user, terminal=current_terminal,
                             date_join=current_queue['date_join'], date_call=datetime.now(),num=current_queue['num'])
                log.save()
                return Response({'status': True,'num':current_queue['num'],'length':Queue.objects.length(current_terminal.service)}, status.HTTP_200_OK)
            else:
                return Response({'status': False}, status.HTTP_404_NOT_FOUND)
        except Queue.DoesNotExist:
            return Response({'status':False},status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            print(ex)
            return Response({'status':False},status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def servcice_que(request):
    if request.method == 'POST':
        try:
            service = Service.objects.get(name=request.data['service'])
            length = Queue.objects.length(service)
            first = Queue.objects.first(service)
            data = {'length':length,'next':first.num}
            return Response(data, status.HTTP_200_OK)
        except Service.DoesNotExist:
            return Response({'status':False},status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            print(ex)
            return Response({'status':False},status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def change_terminal(request):
    if request.method == 'POST':
        try:
            t = Terminal.objects.get(name=request.data['terminal'])
            TerminalUser.objects.filter(user=request.user).update(terminal=t)
            data = {'status':True}
            return Response(data, status.HTTP_200_OK)
        except Exception as ex:
            print(ex)
            return Response({'status':False},status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_terminal(request):
    if request.method == 'GET':
        try:
            t = TerminalUser.objects.get(user=request.user).terminal.name
            print(t,request.user)
            data = {'terminal':t}
            return Response(data, status.HTTP_200_OK)
        except Exception as ex:
            print(ex)
            return Response({'status':False},status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def reports(request):
    if request.method == 'GET':
        try:
            data = json.loads(request.data)
            start_dt = data['start']
            end_dt = data['end']
            kwargs = {}
            try:
                s = Service.objects.get(name=data['info']['service'])
                kwargs['service'] = s
            except:pass
            try:
                s = Terminal.objects.get(name=data['info']['terminal'])
                kwargs['terminal'] = s
            except:pass
            try:
                s = User.objects.get(username=data['info']['user'])
                kwargs['user'] = s
            except:pass
            d = QueLog.objects.all().filter(date_join__range=(start_dt,end_dt),**kwargs)
            s = QlogSerializer(d,many=True)
            return Response(s.data,status.HTTP_200_OK)
        except Exception as ex:
            print(ex)
            return Response({"error":str(ex)},status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def report_detailed(request):
    def comp_avg(key,dic):
        try:
            return sum(dic[key]) / len(dic[key])
        except:
            return 0
    if request.method == 'GET':
            data = json.loads(request.data)
            start_dt = data['start']
            end_dt = data['end']
            rep_type = data['service']
            final_m1 = {}
            final_m2 = {}
            d = QueLog.objects.all().filter(date_join__range=(start_dt,end_dt))
            for i in d:
                if rep_type:
                    nm = i.service.name
                else:
                    nm = i.terminal.name
                try:
                    m1 = (i.date_call - i.date_join).seconds * 60
                    if nm in final_m1.keys():
                        final_m1.setdefault(nm, []).append(m1)
                    else:
                        final_m1[nm] = [m1]
                except:pass

                try:
                    m2 = (i.date_end - i.date_call).seconds * 60
                    if nm in final_m2.keys():
                        final_m2.setdefault(nm, []).append(m2)
                    else:
                        final_m2[nm] = [m2]
                except:pass
            x = [{'name':key,'avg1':comp_avg(key,final_m1),'avg2':comp_avg(key,final_m2)} for key in final_m1.keys()]
            s = DetailedSerializer(x,many=True)
            return Response(s.data,status.HTTP_200_OK)
