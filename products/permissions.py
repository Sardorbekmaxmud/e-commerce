from rest_framework import permissions


# Create your custom permissions
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # request metodi GET, HEAD or OPTION bo'lsa, faqat o'qishga ruxsat beradi.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Aks holda, qolgan request metodlarida egasi bo'lsagina ruxsat beradi.
        # Egasi bo'lmasa ruxsat bermaydi.
        return obj.customer == request.user


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Custom permission. request user staff member bo'lsa,
    productlarni edit va delete qila oladi.

    Boshqa userlar faqat productlarni o'qiy oladi.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.is_staff
