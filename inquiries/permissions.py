from rest_framework import permissions


class IsAdminOrInstructor(permissions.BasePermission):
    """
    Allow access to users with role 'admin' OR 'instructor'
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (
                getattr(request.user, "role", None) in ("admin", "instructor")
                or request.user.is_staff  # (Optional: also allow django staff)
            )
        )
