from rest_framework.permissions import BasePermission

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to view or modify messages.
    """

    def has_permission(self, request, view):
        # Only authenticated users allowed
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Only participants of the conversation can access
        return request.user in obj.participants.all()