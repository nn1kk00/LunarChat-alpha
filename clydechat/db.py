import datetime
from .models import User, ActiveSession, BannedIPAddress, NtIP, GlobalSetting

def load_json(filename):
    if filename == "nicks.json":
        users = list(User.objects.values_list('name', flat=True))
        users = [u for u in users if u]
        verifed = list(User.objects.filter(role=1).values_list('name', flat=True))
        admins = list(User.objects.filter(role=2).values_list('name', flat=True))
        return {
            "users": users,
            "verifed": verifed,
            "admins": admins
        }
    
    elif filename == "accounts.json":
        return {u.name: u.password_hash or "" for u in User.objects.all() if u.name}
    
    elif filename == "block.json":
        return {"block": list(User.objects.filter(block=1).values_list('name', flat=True))}
    
    elif filename == "avatars.json":
        return {u.name: u.avatar_status for u in User.objects.all() if u.name}
    
    elif filename == "accip.json":
        res = {"a": []}
        for session in ActiveSession.objects.all():
            res["a"].append(session.ip_address)
            res[session.ip_address] = session.username
            res[session.username] = session.ip_address
        return res
    
    elif filename == "ip.json":
        return {"banned": list(BannedIPAddress.objects.values_list('ip_address', flat=True))}
    
    elif filename == "nt.json":
        return {"ip": list(NtIP.objects.values_list('ip_address', flat=True))}
    
    elif filename == "data.json":
        setting = GlobalSetting.objects.filter(key='chat_enabled').first()
        chat_val = int(setting.value) if setting else 1
        return {"chat": chat_val}
    
    elif filename == "time.json":
        day_setting = GlobalSetting.objects.filter(key='last_activity_day').first()
        month_setting = GlobalSetting.objects.filter(key='last_activity_month').first()
        day = int(day_setting.value) if day_setting else datetime.datetime.now().day
        month = int(month_setting.value) if month_setting else datetime.datetime.now().month
        return {"day": day, "month": month}
    
    else:
        raise ValueError(f"Unknown database file: {filename}")

def save_json(filename, data):
    if filename == "nicks.json":
        new_names = set(data.get("users", []))
        for name in new_names:
            role = 0
            if name in data.get("admins", []):
                role = 2
            elif name in data.get("verifed", []):
                role = 1
            
            user, created = User.objects.get_or_create(
                name=name,
                defaults={"role": role, "mute": 0, "block": 0}
            )
            if not created and user.role != role:
                user.role = role
                user.save()
        existing_names = set(User.objects.values_list('name', flat=True))
        User.objects.filter(name__in=existing_names - new_names).delete()
        
    elif filename == "accounts.json":
        for name, pwd in data.items():
            user, created = User.objects.get_or_create(
                name=name,
                defaults={"password_hash": pwd, "mute": 0, "block": 0}
            )
            if not created and user.password_hash != pwd:
                user.password_hash = pwd
                user.save()
        
    elif filename == "block.json":
        blocked_names = set(data.get("block", []))
        for name in blocked_names:
            User.objects.update_or_create(
                name=name,
                defaults={"block": 1, "mute": 0}
            )
        User.objects.exclude(name__in=blocked_names).update(block=0)
        
    elif filename == "avatars.json":
        for name, status in data.items():
            user, created = User.objects.get_or_create(
                name=name,
                defaults={"avatar_status": status, "mute": 0, "block": 0}
            )
            if not created and user.avatar_status != status:
                user.avatar_status = status
                user.save()
                
    elif filename == "accip.json":
        active_ips = set(data.get("a", []))
        for ip_val in active_ips:
            username = data.get(ip_val)
            if username:
                ActiveSession.objects.update_or_create(
                    ip_address=ip_val,
                    defaults={"username": username}
                )
        ActiveSession.objects.exclude(ip_address__in=active_ips).delete()
        
    elif filename == "ip.json":
        banned_ips = set(data.get("banned", []))
        for ip_val in banned_ips:
            BannedIPAddress.objects.get_or_create(ip_address=ip_val)
        BannedIPAddress.objects.exclude(ip_address__in=banned_ips).delete()
        
    elif filename == "nt.json":
        nt_ips = set(data.get("ip", []))
        for ip_val in nt_ips:
            NtIP.objects.get_or_create(ip_address=ip_val)
        NtIP.objects.exclude(ip_address__in=nt_ips).delete()
        
    elif filename == "data.json":
        chat_val = data.get("chat", 1)
        GlobalSetting.objects.update_or_create(
            key='chat_enabled',
            defaults={'value': str(chat_val)}
        )
        
    elif filename == "time.json":
        day = data.get("day", datetime.datetime.now().day)
        month = data.get("month", datetime.datetime.now().month)
        GlobalSetting.objects.update_or_create(
            key='last_activity_day',
            defaults={'value': str(day)}
        )
        GlobalSetting.objects.update_or_create(
            key='last_activity_month',
            defaults={'value': str(month)}
        )
    else:
        raise ValueError(f"Unknown database file: {filename}")
