from azure.iot.device import Message
from azure.iot.hub import IoTHubRegistryManager
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

IOT_HUB_CONNECTION_STRING = "HostName=msdocs-python-django-webapp-quickstart-hub.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=XsjnSl7p82qVYP16a93zekwFcg0b/SPh/AIoTJFmW3M="
DEVICE_ID = "rasberry-pi-simulator"


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is None:
            context = {"error": "Invalid credentials"}
            return render(request, "hello_azure/login_view.html", context)
        login(request, user)
        return redirect("/valve/")
    return render(request, "hello_azure/login_view.html")


def message(device_id, message_string):
    try:
        registry_manager = IoTHubRegistryManager(IOT_HUB_CONNECTION_STRING)
        message = Message(message_string)
        message.content_encoding = "utf-8"
        message.content_type = "application/json"
        registry_manager.send_c2d_message(device_id, message)
        print(f"Sent message to {device_id}: {message_string}")
    except Exception as e:
        print(f"Error sending C2D message: {e}")


@csrf_exempt
def valve(request):
    valves = list(range(1, 6))
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "toggle_valve":
            message(DEVICE_ID, "toggle_valve")
        elif action == "set_times":
            open_time = request.POST.get("open_time")
            close_time = request.POST.get("close_time")
            message(DEVICE_ID, f"set_times {open_time} {close_time}")
        return HttpResponseRedirect("/")  # Redirect to home page or appropriate URL
    return render(request, "hello_azure/valve.html", {"valves": valves})
