from rest_framework import permissions


class ReadOnly(permissions.BasePermission):
    """
    ArticleCategory-level permission for read only methods.
    """

    def has_permission(self, request, _):
        """Override has_permission to allow only read methods."""
        return request.method in permissions.SAFE_METHODS


class CreateOrReadOnly(permissions.BasePermission):
    """
    Article-level permission to block deletion and update of an article.
    """

    def has_permission(self, request, _):
        """Override has_permission to allow only read and create methods."""
        return request.method in (permissions.SAFE_METHODS + ('POST',))


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Sale-level permission to only allow author of an object to edit it.
    """

    def has_object_permission(self, request, _, obj):
        """Override has_permission to allow update/delete for sale's author."""
        # If request is read only, allow it
        if request.method in permissions.SAFE_METHODS:
            return True
        # Else check that the user is the author of the sale
        return obj.author == request.user
