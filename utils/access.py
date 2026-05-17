from functools import wraps

import jwt
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from user.models import UserProfile


def permit(*perms):
    skip_permission_check = len(perms) == 1 and perms[0] is None

    required_perms = set()
    if not skip_permission_check:
        for perm in perms:
            if isinstance(perm, (list, tuple)):
                required_perms.update(perm)
            else:
                required_perms.add(perm)

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            def test_func(user):
                if skip_permission_check:
                    return True

                try:
                    cache_key = f"permissions_{user.id}"
                    cached_permissions = cache.get(cache_key)

                    if cached_permissions is None:
                        user_role = (
                            UserProfile.objects.select_related("role")
                            .get(user=user)
                            .role
                        )

                        if not user_role:
                            return False

                        cached_permissions = set(
                            user_role.permissions.values_list("name", flat=True)
                        )
                        cache.set(cache_key, list(cached_permissions), 3600)
                    else:
                        cached_permissions = set(cached_permissions)

                    has_permission = bool(required_perms & cached_permissions)

                    return has_permission

                except UserProfile.DoesNotExist:
                    return False
                except Exception as e:
                    return False

            # Test permissions
            if not test_func(request.user):
                raise PermissionDenied("Permission denied")

            # Token validation
            try:
                # Sector token
                sector_token = request.headers.get("X-Sector")

                if not sector_token:
                    raise PermissionDenied("Sector token missing")

                sector = jwt.decode(
                    sector_token,
                    settings.SECRET_KEY,
                    algorithms=["HS256"],
                )
                sid = sector["id"]
                sn = sector["name"]

                # Property token
                cache_key = f"properties_{request.user.id}"
                cached_properties = cache.get(cache_key)

                if cached_properties is None:
                    property_token = request.headers.get("X-Property")

                    if not property_token:
                        raise PermissionDenied("Property token missing")

                    property_data = jwt.decode(
                        property_token,
                        settings.SECRET_KEY,
                        algorithms=["HS256"],
                    )
                    ppt = property_data["properties"]

                    cache.set(cache_key, ppt, 3600)
                else:
                    ppt = cached_properties

                return view_func(request, sid, sn, ppt, *args, **kwargs)

            except jwt.InvalidTokenError as e:
                raise PermissionDenied("Invalid token")
            except KeyError as e:
                raise PermissionDenied("Invalid token format")
            except Exception as e:
                import traceback

                traceback.print_exc()
                raise

        return wrapper

    return decorator
