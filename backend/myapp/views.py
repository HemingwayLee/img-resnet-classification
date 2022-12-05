import os
import json
import traceback
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.db import connection

def index(request):
    return render(request, 'index.html')

# def show1(request):
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT * FROM person_info;")
#         data = cursor.fetchall()

#     output = ""
#     for p in data:
#       output += str(p[0]) + " " + p[1] + " " + p[2] + "<br>"

#     return JsonResponse({"result": output})


# def show2(request):
#     with connection.cursor() as cursor:
#         # `person_info` is view, callproc does not work
#         # cursor.callproc("person_info")
#         cursor.callproc("my_func") 
#         data = cursor.fetchall()

#     output = ""
#     for p in data:
#         output += str(p[0]) + " " + p[1] + " " + p[2] + "<br>"

#     return JsonResponse({"result": output})
