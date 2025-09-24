from fastapi import APIRouter
from .logging import logger
from . import network_configuration as ncmp
from .clients import oauth_manager

api_router = APIRouter(prefix="/api/v1")

@api_router.get("/hello")
async def hello_world():
    """An example endpoint."""
    logger.info("Hello world endpoint was called.")
    return {"message": "Hello, rApp developer!"}

@api_router.get("/network-configuration/{source_id}")
async def get_network_config(source_id: str, attribute: str = "operationalState"):
    """Example endpoint to get a specific attribute from a network element."""
    logger.info(f"Getting attribute '{attribute}' for source ID '{source_id}'")
    client = await oauth_manager.get_async_client()
    # TODO: You might want to add more robust error handling here
    return await ncmp.get_attribute_for_source_id(client, source_id, attribute)