from functools import wraps
from datetime import datetime
from django.core import signing
from django.http import JsonResponse
from django.conf import settings


# Generate level one reference keys
def generate_level_one_ref_key(model_name, prefix):

    # Find the maximum index currently in use
    today_date = datetime.today().strftime("%y%m%d")
    latest_ref_key = model_name.objects.values("ref_key").order_by("-id").first()

    if latest_ref_key:
        # Extract the last number and increment it
        last_number = int(latest_ref_key["ref_key"].rsplit("-", 1)[1])
        new_number = last_number + 1
    else:
        new_number = 1

    return f"{today_date}-{prefix}-{new_number}"


def generate_level_two_ref_key(model_name, prefix, base_model, base_id):
    """
    Generates a reference key for a model based on its base model (branch) and a running counter
    """
    # Get the base ref_key
    base_res = base_model.objects.filter(id=base_id).values("ref_key").get()
    base_ref_key = base_res["ref_key"]
    
    # If base_ref_key contains hyphen, get the last part, otherwise use the whole key
    try:
        base_index = base_ref_key.rsplit("-", 1)[1]
    except IndexError:
        # If no hyphen found, use the entire ref_key as base_index
        base_index = base_ref_key

    # Find the maximum index currently in use for the base model
    latest_ref_key = (
        model_name.objects.filter(branch=base_id)
        .values("ref_key")
        .order_by("-id")
        .first()
    )

    if latest_ref_key:
        try:
            # Extract the last number and increment it
            last_number = int(latest_ref_key["ref_key"].rsplit("-", 1)[1])
            new_number = last_number + 1
        except (IndexError, ValueError):
            # If parsing fails, start with 1
            new_number = 1
    else:
        new_number = 1

    # Format: {branch_ref}-{prefix}-{number}
    return f"{base_index}-{prefix}-{new_number}"


# Validate register link
def signing_token_validate(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Authentication logic here
        token = request.headers.get("Authorization")
        if not token:
            return JsonResponse({"error": "Authentication required"}, status=401)

        try:
            payload = signing.loads(token, key=settings.SECRET_KEY, max_age=600)
            # Call user view with payload data
            return view_func(request, payload, *args, **kwargs)
        except signing.SignatureExpired:
            return JsonResponse({"error": "Token expired"}, status=401)
        except signing.BadSignature:
            return JsonResponse({"error": "Invalid token signature"}, status=401)

    return wrapper
