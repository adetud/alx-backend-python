from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to access it.

    Assumes the model instance has an `owner` attribute, or `sender`/`recipient` - adapt as needed.
    """

    def has_object_permission(self, request, view, obj):
        # read/write allowed only if object's owner (or sender/recipient) is the request.user
        # Try common field names:
        owner_fields = ["owner", "user", "sender", "recipient"]
        for field in owner_fields:
            if hasattr(obj, field):
                attr = getattr(obj, field)
                # If recipient is a related object or a queryset, handle accordingly:
                try:
                    return attr == request.user
                except Exception:
                    pass

        # fallback deny
        return False
