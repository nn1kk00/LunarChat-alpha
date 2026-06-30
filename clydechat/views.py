from django.shortcuts import render
from django.http import *
from django import forms
from django.middleware import *
from django.middleware.csrf import *
import json
from hashlib import sha256
from .db import load_json, save_json
from datetime import timezone
import datetime

# Create your views here.

def ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
  
class MsgForm(forms.Form):
    nick = forms.CharField(label="Логин", required=True, min_length=2, max_length=15)
    passww = forms.CharField(label="Пароль", required=True, max_length=200, min_length=8, widget=forms.PasswordInput)
    message = forms.CharField(label="Сообщение", required=True, max_length=200)
  
class MsgForm1(forms.Form):
    message = forms.CharField(label="Сообщение", required=True, max_length=200)
class LoginForm(forms.Form):
    nick = forms.CharField(label="Логин", required=True, min_length=2, max_length=15)
    passw = forms.CharField(label="Пароль", required=True, max_length=200, min_length=8, widget=forms.PasswordInput)
def err(req, e="LUNAR"):
  q = req.GET.get("q")
  e = req.GET.get("e", "LUNAR")
  return HttpResponse(f"<center><h1>Ой! Неизвестная ошибка!</h1><h3>Подробнее: {q}</h3><hr><h6><i><b>WITH LOVE, {e}</b><i></h6>")
def red(req):
  r = req.GET.get("link")
  if r == "нуэтоточнонетвойрулл34":
      return HttpResponse("ily <3")
  else:
      return HttpResponsePermanentRedirect("https://www.google.com/search?q=%D1%84%D1%83%D1%80%D1%80%D0%B8+%D0%BF%D0%BE%D1%80%D0%BD%D0%BE+%D0%B2+%D1%87%D1%83%D0%BB%D0%BA%D0%B0%D1%85+18%2B+%D0%BE%D0%BC%D0%B5%D0%B3%D0%B8&oq=%D1%84%D1%83%D1%80%D1%80%D0%B8+%D0%BF%D0%BE%D1%80%D0%BD%D0%BE+%D0%B2+%D1%87%D1%83%D0%BB%D0%BA%D0%B0%D1%85+18%2B+%D0%BE%D0%BC%D0%B5%D0%B3%D0%B8&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCDk0NDNqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8")
def conv(m):
    if m == 1:
        return "January"
    if m == 2:
        return "February"
    if m == 3:
        return "March"
    if m == 4:
        return "April"
    if m == 5:
        return "May"
    if m == 6:
        return "June"
    if m == 7:
        return "July"
    if m == 8:
        return "August"
    if m == 9:
        return "September"
    if m == 10:
        return "October"
    if m == 11:
        return "November"
    if m == 12:
        return "December"
def index(req):
    if req.method == "POST":
        ips = ip(req)
        form = MsgForm(req.POST)
        form1 = MsgForm1(req.POST)
        if form.is_valid():
            passww = form.cleaned_data["passww"]
            nick = form.cleaned_data['nick']
            msg = form.cleaned_data['message']
        elif form1.is_valid():
            msg = form1.cleaned_data["message"]
        n = load_json("nicks.json")
        block = load_json("block.json")
        acc = load_json("accounts.json")
        accip = load_json("accip.json")
        ipw = load_json("ip.json")
        if ips in accip["a"] and accip[ips] != "":
            if accip[ips] not in n["admins"]:
                pass
            if ips in ipw["banned"]:
                return HttpResponse("<center><h1>Извините, но</h1><h3>Вы были заблокированы по IP создателем. Приносим свои извинения за неудобство.</h2><hr><h6>With love, LunarChat ❤</h6></center>")
        else:
            if nick in block["block"]:
                return HttpResponse("<h1>Этот аккаунт заблокирован.</h1>")
            if nick not in n["users"]:
                pass
                return HttpResponsePermanentRedirect(f"/login/")               
            if nick not in n["admins"]:
                pass
        acc = load_json("accounts.json")
        ips = ip(req)
        accip = load_json("accip.json")
        if ips in accip["a"] and accip[ips] != "":
            if msg != "": 
                if accip[ips] in n["admins"]:
                    if msg == ";stop":
                        data = load_json("data.json")
                        data["chat"] = 0
                        save_json("data.json", data)
                        return HttpResponsePermanentRedirect("/")
                    if msg[0:3] == ";bc":
                        with open('data.txt', "a", encoding="utf-8") as f:
                            f.write(f"[<b>ОБЪЯВЛЕНИЕ</b>]<br><b>{msg[4:len(msg)]}</b>\n<br>")
                            f.close()
                        return HttpResponsePermanentRedirect("/")
                    if msg[0:6] == ";block":
                        block["block"].append(f"{str(msg[7:len(msg)])}")
                        save_json("block.json", block)
                        ipw = load_json("ip.json")
                        ipw["banned"].append(f'{accip[msg[7:len(msg)]]}')
                        save_json("ip.json", ipw)
                        return HttpResponsePermanentRedirect(f"/data?nm=Console&msg={str(msg[7:len(msg)])} blocked&passw=231fd3b5accaec45e197b708276b4a9f1f256cc0b33137546a4a99f6a2a4c048")
                    if msg[0:8] == ";unblock":
                        try:
                            block["block"].remove(f"{msg[9:len(msg)]}")
                        except ValueError:
                            pass
                        save_json("block.json", block)
                        ipw = load_json("ip.json")
                        try:
                            ipw["banned"].remove(f'{accip[msg[9:len(msg)]]}')
                        except ValueError:
                            pass
                        save_json("ip.json", ipw)
                        return HttpResponsePermanentRedirect(f"/data?nm=Console&msg={str(msg[7:len(msg)])} unblocked&passw=231fd3b5accaec45e197b708276b4a9f1f256cc0b33137546a4a99f6a2a4c048")
                    if msg == ";clear":
                        date = load_json("time.json")
                        with open("data.txt", "w", encoding="UTF-8") as f:
                            f.write(f"""Clyde: Приветствую вас в нашем простеньком чате LunarChat!
<br>{date["day"]} {conv(date["month"])}
<br>""")
                            f.close()
                        return HttpResponseRedirect("/")
                return HttpResponsePermanentRedirect(f"/data/?nm={accip[ips]}&msg={msg}&passw={acc[accip[ips]]}")
            else: return HttpResponsePermanentRedirect("/")
        else:
            passww = sha256(passww.encode()).hexdigest() 
            if passww == acc[nick]:
                a = load_json("avatars.json")
                try:
                    if a[nick] == 0 or a[nick] == 1: pass 
                except:
                    a[nick] = 0
                    save_json("avatars.json", a)
                accip[ips] = nick
                accip[nick] = ips
                accip["a"].append(ips)
                save_json("accip.json", accip)
                if msg != "": 
                    if nick in n["admins"]:
                        if msg == ";stop":
                            data = load_json("data.json")
                            data["chat"] = 0
                            save_json("data.json", data)
                            return HttpResponsePermanentRedirect("/")
                        if msg[0:3] == ";bc":
                            with open('data.txt', "a", encoding="utf-8") as f:
                                f.write(f"[<b>ОБЪЯВЛЕНИЕ</b>]<br><b>{msg[4:len(msg)]}</b>\n<br>")
                                f.close()
                            return HttpResponsePermanentRedirect("/")
                        if msg[0:6] == ";block":
                            block["block"].append(f"{str(msg[7:len(msg)])}")
                            save_json("block.json", block)
                            ipw = load_json("ip.json")
                            ipw["banned"].append(f'{accip[msg[7:len(msg)]]}')
                            save_json("ip.json", ipw)
                            return HttpResponsePermanentRedirect(f"/data?nm=Console&msg={str(msg[7:len(msg)])} blocked&passw=231fd3b5accaec45e197b708276b4a9f1f256cc0b33137546a4a99f6a2a4c048")
                        if msg == ";clear":
                            date = load_json("time.json")
                            with open("data.txt", "w", encoding="UTF-8") as f:
                                f.write(f"""Clyde: Приветствую вас в нашем простеньком чате LunarChat!
<br>{date["day"]} {conv(date["month"])}
<br>""")
                                f.close()
                            return HttpResponseRedirect("/")
                    return HttpResponsePermanentRedirect(f"/data/?nm={nick}&msg={msg}&passw={passww}")
                else: return HttpResponsePermanentRedirect('/')
            else: return HttpResponsePermanentRedirect('/')
    else:
        data = load_json("data.json")
        with open("data.txt", 'r', encoding='UTF-8') as f:
            text = f.read()
            f.close()
        frm = MsgForm()
        frm1 = MsgForm1()
        ips = ip(req)
        ipw = load_json("ip.json")
        ipq = load_json("accip.json")
        avatar = load_json("avatars.json")
        date = load_json("nt.json")
        if ips in ipw["banned"]:
            return HttpResponse("<center><h1>Извините, но</h1><h3>Вы были заблокированы по IP создателем. Приносим свои извинения за неудобство.</h2><hr><h6>With love, LunarChat ❤</h6></center>")
        if data["chat"] == 0:
            if ip(req) not in date["ip"]:
                return render(req, "index.html", {"text": "Сервера выключены"})
            else:
                return render(req, "NT/index.html", {"text": "Сервера отключены"}) 
        try:
            if avatar[ipq[ips]] == 0: avatars = 0
            else: avatars = 1   
        except: avatars = -1      
        if ips in ipq["a"]:
            if ip(req) not in date["ip"]:
                return render(req, "index.html", {"form": frm1, "text": text, "avatars": avatars, "nick": ipq[ips]}) 
            else:
                return render(req, "NT/index.html", {"form": frm1, "text": text, "avatars": avatars, "nick": ipq[ips]}) 
        elif data["chat"] == 1:
            if ip(req) not in date["ip"]:
                return render(req, "index.html", {"form": frm, "text": text, "avatars": avatars}) 
            else:
                return render(req, "NT/index.html", {"form": frm, "text": text, "avatars": avatars}) 
def rules(req):
    date = load_json("nt.json")
    if ip(req) not in date["ip"]:
        return render(req, "rules.html")
    else: 
        return render(req, "NT/rules.html")
def delete(req, passw="na"):
    passw = req.GET.get("passw", "na")
    if passw == "thatgirlwilldefinitelylovealexsovi140704@!":
        date = load_json("time.json")
        with open("data.txt", "w", encoding="UTF-8") as f:
            f.write(f"""Clyde: Приветствую вас в нашем простеньком чате LunarChat!
/{date["day"]} {conv(date["month"])}
/""")
            f.close()
        return HttpResponseRedirect("/")
    else:
        return HttpResponseForbidden("403")
def data(req, msg=False, name="Bot", passw="N/a"):
    s = load_json("data.json")
    if s["chat"] == 0: return HttpResponseServerError("<h1>Server Error (500)</h1>")
    msg = req.GET.get("msg", "")
    import html
    msg = html.escape(msg)
    name = req.GET.get("nm", "")
    passww = req.GET.get("passw", "")
    q = req.GET.get("q", "")
    token = req.GET.get("token", "")
    data = load_json("data.json")
    if token == "NeverGonnaGiveYouUpClyde2@!":
        data["chat"] = 1
        save_json("data.json", data)
    if data['chat'] == 0 and q != "69420e":
        return HttpResponseServerError("<h1>Server Error (500)</h1>")
    acc = load_json("nicks.json")
    if name not in acc["users"]:
        return HttpResponsePermanentRedirect(f"/login/")
    else:
        acc = load_json("accounts.json")
        nick = load_json("nicks.json")
        if passww == acc[name]:
            if msg != "":
                with open('data1.txt', 'r', encoding="utf-8") as file:
                    data1 = int(file.readline())
                    file.close()
                if data1 == 100:
                    date = load_json("time.json")
                    with open("data.txt", "w", encoding="UTF-8") as f:
                       f.write(f"""Clyde: Приветствую вас в нашем простеньком чате LunarChat!
/{date["day"]} {conv(date["month"])}
/""")
                       f.close()
                    with open("data1.txt", "w", encoding="UTF-8") as f:
                       f.write('1')
                       f.close()
                else:
                    with open("data1.txt", "w", encoding="UTF-8") as f:
                       f.write(str(data1+1))
                       f.close()
                date = load_json("time.json")
                if date["day"] < datetime.datetime.now().day or date["month"] < datetime.datetime.now().month or date["day"] > datetime.datetime.now().day or date["month"] > datetime.datetime.now().month:
                    if date["day"] < datetime.datetime.now().day or date["day"] > datetime.datetime.now().day:
                        date["day"] = datetime.datetime.now().day
                        save_json("time.json", date)
                    if date["month"] < datetime.datetime.now().month or date["month"] > datetime.datetime.now().month:
                        date["month"] = datetime.datetime.now().month
                        save_json("time.json", date)
                    with open("data.txt", 'a', encoding='UTF-8') as f:
                        f.write(f"<hr>{date['day']} {conv(date['month'])}\n<br>")
                        f.close()
                if len(str(datetime.datetime.now().hour)) == 1:
                    d = "0"
                else:
                    d = ''
                if len(str(datetime.datetime.now().minute)) == 1:
                    t = "0" 
                else:
                    t = ''
                avatar = load_json("avatars.json")
                if avatar[name] == 0:
                    avatars = "defuser"
                else:
                    avatars = name
                if name in nick["admins"]:
                    with open("data.txt", 'a', encoding='UTF-8') as f:
                        f.write("<p>"+f"<img src='static\images\{avatars}.png' width=30px height=30px>"+" {admin} "+f'{name} [{d}{datetime.datetime.now().hour}:{t}{datetime.datetime.now().minute}] <br>{msg}\n'+"</p>")
                        f.close()
                elif name in nick["verifed"]:
                    with open("data.txt", 'a', encoding='UTF-8') as f:
                        f.write("<p>"+f"<img src='static\images\{avatars}.png' width=30px height=30px>"+" {verifed} "+f'{name} [{d}{datetime.datetime.now().hour}:{t}{datetime.datetime.now().minute}] <br>{msg}\n'+"</p>")
                        f.close()
                else:
                    with open("data.txt", 'a', encoding='UTF-8') as f:
                        f.write("<p>"+f"<img src='static\images\{avatars}.png' width=30px height=30px>"+f' {name} [{d}{datetime.datetime.now().hour}:{t}{datetime.datetime.now().minute}] <br>{msg}\n'+"</p>")
                        f.close()
    return HttpResponseRedirect("/")
def login(req):
    if req.method == "POST":
        frm = LoginForm(req.POST)
        if frm.is_valid():
            nick = frm.cleaned_data["nick"]
            passw = frm.cleaned_data["passw"]
        passw = sha256(passw.encode()).hexdigest() 
        return HttpResponsePermanentRedirect(f"/logindata/?log={nick}&passw={passw}")
    else:
        frm = LoginForm()
        data = load_json("data.json")
        data1 = load_json("nt.json")
        if data["chat"] == 0:
            if str(ip(req)) not in data1["ip"]:
                return render(req, "login.html")
            else: 
                return render(req, "NT/login.html")
        elif data["chat"] == 1:
            if str(ip(req)) not in data1["ip"]:
                return render(req, "login.html", {"form": frm})
            else: 
                return render(req, "NT/login.html", {"form": frm})
def logindata(req, log="N/a", passw="N/a"):
    log = req.GET.get("log", "N/a")
    passw = req.GET.get("passw", "N/a")
    q = req.GET.get("q", 0)
    data = load_json("data.json")
    if data['chat'] == 0 and q != "69420e":
      return HttpResponseServerError("<h1>Server Error (500)</h1>")
    acc = load_json("nicks.json")
    if log in acc["users"] or log[0::6] == "{admin}" or log[0::6] == "{verifed}":
        return HttpResponsePermanentRedirect("/login/")
    else:
        acc = load_json("accounts.json")
        acc[log] = passw
        save_json("accounts.json", acc)
        acc_nicks = load_json("nicks.json")
        acc_nicks["users"].append(log)
        save_json("nicks.json", acc_nicks)
        return HttpResponsePermanentRedirect("/")
def logout(req):
    try: 
        temp = load_json("accip.json")
        temp1 = temp[ip(req)]
        del temp[temp1]
        temp["a"].remove(ip(req))
        del temp[ip(req)]
        save_json("accip.json", temp)
        return HttpResponsePermanentRedirect("/")
    except: return HttpResponsePermanentRedirect("/")
def j0b(req):
    ips = ip(req)
    accip = load_json("accip.json")
    if ips not in accip["a"]:
        return HttpResponsePermanentRedirect("/login/")
    nick = accip[ips]
    if req.method == "POST":
        import os
        from django.conf import settings
        avatar_file = req.FILES.get("avatar")
        if avatar_file:
            path = os.path.join(settings.BASE_DIR, "static", "images", f"{nick}.png")
            with open(path, "wb+") as f:
                for chunk in avatar_file.chunks():
                    f.write(chunk)
            avatars = load_json("avatars.json")
            avatars[nick] = 1
            save_json("avatars.json", avatars)
        return HttpResponseRedirect("/")
    else:
        nt_data = load_json("nt.json")
        if ips in nt_data["ip"]:
            return render(req, "NT/settings.html", {"nick": nick})
        else:
            return render(req, "settings.html", {"nick": nick})
class NT:
    def on(req):
        temp = load_json("nt.json")
        temp["ip"].append(str(ip(req)))
        save_json("nt.json", temp)
        return HttpResponseRedirect("/")
    def off(req):
        temp = load_json("nt.json")
        try:
            temp["ip"].remove(str(ip(req)))
        except ValueError:
            pass
        save_json("nt.json", temp)
        return HttpResponseRedirect("/")
def ipp(req):
    ipw = ip(req)
    print(ipw)
    return HttpResponse(f"{ipw}")
