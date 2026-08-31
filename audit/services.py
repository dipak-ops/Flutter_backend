from audit.models import AuditLog


def get_client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def log_action(*, user, action, target_type="", target_id="", taluka=None, ip_address=None, metadata=None):
    return AuditLog.objects.create(
        user=user if getattr(user, "is_authenticated", False) or getattr(user, "pk", None) else None,
        action=action,
        target_type=target_type,
        target_id=str(target_id) if target_id not in (None, "") else "",
        taluka=taluka,
        ip_address=ip_address,
        metadata=metadata or {},
    )
