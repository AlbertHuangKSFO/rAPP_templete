import asyncio
from urllib.parse import urlencode, unquote
from authlib.integrations.httpx_client import AsyncOAuth2Client
from httpx import HTTPStatusError
from .logging import logger
from .config import get_config
from eiid_access_id import network_configuration_url_helper
from eiid_access_id.network_configuration_url_helper import DataStoreType

async def get_attribute_for_source_id(client: AsyncOAuth2Client, source_id: str, attribute_path: str) -> dict:
    """
    Generic function to retrieve a specific attribute for a given source ID from Network Configuration.

    Args:
        client: An authenticated AsyncOAuth2Client.
        source_id: The unique identifier for the network element (e.g., from Topology & Inventory).
        attribute_path: The YANG path to the desired attribute (e.g., 'attributes/operationalState').

    Returns:
        A dictionary containing the result or an error.
    """
    logger.info(f"Reading attribute '{attribute_path}' for source ID '{source_id}'")
    
    # TODO: Adjust DataStoreType if you need to read from a different datastore (e.g., RUNNING).
    ncmp_url_obj = network_configuration_url_helper.url_data_from_prefixed_fdn(
        source_id,
        get_config()["iam_base_url"],
        DataStoreType.PASSTHROUGH_OPERATIONAL,
    )
    
    base_url, params_str = ncmp_url_obj.get_network_configuration_url().split("?", 1)
    resource_key, resource_val = params_str.split("=", 1)

    params = {
        resource_key: unquote(resource_val),
        "options": f"(fields={attribute_path})",
    }
    
    try:
        response = await client.get(base_url, params=urlencode(params, safe='[]()'))
        response.raise_for_status()
        logger.debug(f"Successfully retrieved attribute for {source_id}")
        return response.json()
    except HTTPStatusError as e:
        logger.error(f"Failed to get attribute for '{source_id}': {e.response.status_code} {e.response.text}")
        return {"error": str(e), "status_code": e.response.status_code}
    except Exception as e:
        logger.error(f"An unexpected error occurred while getting attribute for '{source_id}': {e}")
        return {"error": str(e)}