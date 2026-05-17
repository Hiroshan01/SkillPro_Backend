import os
from django.utils.crypto import get_random_string
from django.utils.deconstruct import deconstructible
from django.conf import settings

import boto3
from botocore.client import Config


@deconstructible
class UploadFile(object):
    """
    Helper for building randomized upload paths.

    Usage in models:
        image = models.ImageField(upload_to=UploadFile("images"))

    This will store files under:
        images/<32-char-random>.<ext>
    regardless of whether local storage or S3/Spaces is used.
    """

    def __init__(self, path: str):
        self.path = os.path.join(path, "%s%s")

    def __call__(self, instance, filename: str) -> str:
        extension = os.path.splitext(filename)[1]
        random_string = get_random_string(length=32)
        filename = self.path % (random_string, extension)
        return filename


def generate_signed_url(file_name: str, expiry: int = 3600):
    """
    Generate a signed URL for an object stored in S3 / DigitalOcean Spaces.

    Args:
        file_name (str): The name/path of the file (e.g. instance.image.name)
        expiry (int): URL expiration time in seconds

    Returns:
        str | None: Signed URL or None if an error occurs / not configured.
    """
    if not file_name:
        return None

    # Only attempt to sign if S3/Spaces is enabled
    if not getattr(settings, "USE_SPACES", False):
        return None

    try:
        # Create the client only once if it doesn't exist (cached on the function)
        if not hasattr(generate_signed_url, "_client"):
            session = boto3.session.Session()
            generate_signed_url._client = session.client(
                "s3",
                region_name=settings.AWS_S3_REGION_NAME,
                endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                config=Config(signature_version="s3v4"),
            )

        # Normalize the file path
        key = str(file_name)

        # Handle AWS_LOCATION prefix if defined
        aws_location = getattr(settings, "AWS_LOCATION", "")
        if aws_location and not key.startswith(aws_location):
            key = f"{aws_location.rstrip('/')}/{key.lstrip('/')}"

        # Generate the signed URL
        url = generate_signed_url._client.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
                "Key": key,
            },
            ExpiresIn=expiry,
        )

        return url

    except Exception as e:
        import logging

        logger = logging.getLogger(__name__)
        logger.error(f"Error generating signed URL for {file_name}: {e}")
        return None


