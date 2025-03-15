import importlib
from pathlib import Path
from typing import List, Type

from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient


from app.core.config import settings
from app.common import setup_logger

logger = setup_logger('Core::DB')

def init_document_models() -> List[Type[Document]]:
    """Automatically loads all Document models from the 'models' directory."""

    base_dir = (
        Path(__file__).resolve().parent.parent
    )  # Get the parent directory of this `core` dir
    models_dir = base_dir / "models"  # Path to the 'models' directory
    document_models = []

    # Iterate through all Python files in the 'models' directory
    for model_file in models_dir.glob("*.py"):
        if model_file.name == "__init__.py":
            continue

        module_name = f"app.models.{model_file.stem}"  # Convert filename to module name
        module = importlib.import_module(module_name)

        # Collect all classes that subclass Document
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)
            if (
                isinstance(attribute, type)
                and issubclass(attribute, Document)
                and attribute is not Document
            ):
                document_models.append(attribute)

    return document_models


async def init_mongodb():
  try:
    client = AsyncIOMotorClient(
      settings.MONGO_DB_URI
    )
    db = client[settings.MONGO_DB_NAME]
    await init_beanie(database=db, document_models=init_document_models())
    logger.info("MongoDB Database initialized")
  except Exception as e:
    logger.error(f"Error initializing MongoDB Database: {e}")
    raise e