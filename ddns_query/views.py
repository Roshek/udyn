# from django.shortcuts import render
from django.http import HttpResponse
from .models import Dyname
from ipware.ip import get_ip
import subprocess
# Create your views here.


def index(request):
    return HttpResponse("ddns stuff")


def get_address(request, host_name):
    try:
        dyname = Dyname.objects.get(prefix=host_name)
    except Dyname.DoesNotExist:
        return HttpResponse('The hostname ' + host_name +
                            '.ddns.aszabados.eu has not been registered.')
    else:
        return HttpResponse(dyname.ip)


def set_hostname(request, host_name):
    ip = get_ip(request)
    if ip is not None:
        try:
            dyname = Dyname.objects.get(prefix=host_name)
        except Dyname.DoesNotExist:
            dyname = Dyname(prefix=host_name, ip=ip)
            dyname.save()
            subprocess.run('nsupdate',
                           input=str.encode("server ns1.aszabados.eu" +
                                            "\nzone aszabados.eu" +
                                            "\nupdate add " +
                                            host_name +
                                            ".ddns.aszabados.eu 60 A " +
                                            ip +
                                            "\nsend" +
                                            "\nquit"))
            return HttpResponse("Your IP " +
                                dyname.ip +
                                " is saved with hostname " +
                                host_name + ".ddns.aszabados.eu")
        else:
            dyname.ip = ip
            dyname.save()
            subprocess.run('nsupdate',
                           input=str.encode("server ns1.aszabados.eu" +
                                            "\nzone aszabados.eu" +
                                            "\nupdate del " +
                                            host_name +
                                            ".ddns.aszabados.eu A" +
                                            "\nupdate add " +
                                            host_name +
                                            ".ddns.aszabados.eu 60 A " +
                                            ip +
                                            "\nsend" +
                                            "\nquit"))
            return HttpResponse("Updated hostname " +
                                host_name + ".ddns.aszabados.eu" +
                                " with your IP " +
                                dyname.ip)
    else:
        return HttpResponse("Error: Couldn't get your IP.")
