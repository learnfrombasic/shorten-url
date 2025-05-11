"""
Sending files, including: images, videos, etc.
"""

import io
import os

import requests
from minio import Minio
from minio.error import S3Error
from PIL import Image
from tqdm import tqdm

from app.common.logging_config import setup_logger
from app.core.config import settings

logger = setup_logger("network")


class Progress:
    def __init__(self, total_size, progress_callback):
        self.total_size = total_size
        self.progress_callback = progress_callback
        self.current_size = 0

    def update(self, bytes_downloaded):
        self.current_size += bytes_downloaded
        self.progress_callback(self.current_size)

    def set_meta(self, object_name, total_length):
        pass  # You can implement this if needed


class MinioHandler(object):
    def __init__(self):
        self.bucket = settings.MINIO_BUCKET
        minio_host = settings.MINIO_HOST
        minio_url = settings.MINIO_URL
        minio_access_key = settings.MINIO_ACCESS_KEY
        minio_secret_key = settings.MINIO_SECRET_KEY
        secure = True if minio_url.startswith("https") else False

        self.client = Minio(
            endpoint=minio_host,
            access_key=minio_access_key,
            secret_key=minio_secret_key,
            secure=secure,
        )
        self.minio_url = settings.MINIO_URL

    def upload_file(self, source_file: str, destination_file: str, bucket: str = None):
        logger.info(f"Source file to upload: {source_file}")
        if bucket is None:
            bucket = self.bucket
        try:
            self.client.fput_object(bucket, destination_file, source_file)
            return {
                "success": True,
                "info": f"{self.minio_url}/{bucket}/{destination_file}",
            }
        except Exception as e:
            logger.error(f"Error upload_file: {e}")
            return {"success": False, "info": f"Error upload_file: {e}"}

    def upload_image(self, image, destination_file: str, bucket: str = None) -> dict:
        """Upload image in-memory to MinIO Server as a WebP image."""
        if bucket is None:
            bucket = self.bucket

        img_name = f"{bucket}/{destination_file}"

        # Make bucket if not exist.
        found = self.client.bucket_exists(self.bucket)
        if not found:
            self.client.make_bucket(self.bucket)
        else:
            logger.info("[MINIO] Bucket already exists")

        try:
            image_pil = Image.fromarray(image)

            # Convert image to bytes object
            out_img = io.BytesIO()
            image_pil.save(out_img, quality=100, format="WEBP")  # Save as WebP
            out_img.seek(0)

            self.client.put_object(
                self.bucket,
                img_name,
                out_img,
                length=out_img.getbuffer().nbytes,
                content_type="image/webp",
            )

            return {
                "success": True,
                "info": f"{self.minio_url}/{self.bucket}/{img_name}",
            }

        except Exception as e:
            logger.error(f"Error uploading image: {e}")
            return {"success": False, "info": f"Error uploading image: {e}"}

    def delete_file(self, file_name: str, bucket=None):
        if bucket is None:
            bucket = self.bucket
        try:
            self.client.remove_object(bucket, file_name)
            return True
        except Exception as e:
            logger.debug(e)
            return {"success": False, "info": f"Error delete: {e}"}

    def __download_with_progress(self, bucket, object_name, local_filename):
        # Get the size of the object
        stat = self.client.stat_object(bucket, object_name)
        total_size = stat.size

        # Initialize the progress bar
        with tqdm(
            total=total_size,
            unit="iB",
            unit_scale=True,
            unit_divisor=1024,
            desc=local_filename,
        ) as bar:

            def progress_callback(bytes_downloaded):
                bar.update(bytes_downloaded - bar.n)

            # Initialize progress and download the object with progress callback
            progress = Progress(total_size, progress_callback)
            self.client.fget_object(
                bucket, object_name, local_filename, progress=progress
            )

    def download_video(self, url, local_filename):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            if response.headers.get("server") == "MinIO Console":
                try:
                    _, bucket, object_name = response.url.split("/")[-3:]
                    logger.info(f"Downloading: {url}")
                    self.__download_with_progress(
                        self.client, bucket, object_name, local_filename
                    )
                    return {"success": True, "info": local_filename}
                except S3Error as exc:
                    logger.info(f"MinIO error: {exc}")
            else:
                total_size = int(response.headers.get("content-length", 0))
                if total_size == 0:
                    msg = "Error: Content-Length header is missing or zero."
                    logger.info(msg)
                    return {"success": False, "info": msg}

                logger.info(
                    f"Starting download: {local_filename} (size: {total_size} bytes)"
                )

                with (
                    open(local_filename, "wb") as f,
                    tqdm(
                        desc=local_filename,
                        total=total_size if total_size > 0 else None,
                        unit="iB",
                        unit_scale=True,
                        unit_divisor=1024,
                    ) as bar,
                ):
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            bar.update(len(chunk))

                # Verify the downloaded file size
                downloaded_size = os.path.getsize(local_filename)
                if downloaded_size != total_size:
                    logger.warning(
                        f"Warning: Downloaded file size ({downloaded_size}) does not match expected size ({total_size})."
                    )
                else:
                    logger.info(f"Download completed successfully: {local_filename}")
                    return {"success": True, "info": local_filename}

        except requests.exceptions.RequestException as e:
            logger.info(f"Error downloading video: {e}")
            if os.path.exists(local_filename):
                os.remove(local_filename)
            return None

    # ! Not recommended => Depracated soon.
    def upload_frame_with_templfile(self, frame, filename) -> str:
        "Note: Using tempfile save dev from store image at local machine"
        import tempfile

        logger.warning(
            "This feature will not save image locally. The data is discard right after the image is upload successfully"
        )
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                temp_file.write(frame)
                temp_file_path = temp_file.name

            # Upload the temporary file to MinIO
            image_url = self.upload_file(
                source_file=temp_file_path, destionation_file=f"{filename}"
            )
            if image_url.get("success"):
                return image_url.get("info")
        except Exception:
            logger.exception("upload_with_templfile not running successfully")
            raise RuntimeError("upload_with_templfile not running successfully")
        finally:
            logger.info("Remove data from tempfile")
            # Ensure the temporary file is deleted
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)


minio_handler = MinioHandler()
