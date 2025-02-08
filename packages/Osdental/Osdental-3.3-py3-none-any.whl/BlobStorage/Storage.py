from azure.storage.blob.aio import BlobServiceClient
from Handlers.CatalogData import CatalogData
from Exception.ControlledException import AzureException
from Utils.Message import UNEXPECTED_ERROR
from Utils.Code import APP_ERROR
from typing import Any

class BlobStorage: 

    def __init__(self):
        self.catalog_handler = CatalogData()

    async def _get_blob_client(self, file_path: str) -> Any:
        try:
            catalog = await self.catalog_handler.get_data('BlobStorage')
            blob_service_client = BlobServiceClient.from_connection_string(catalog.get('connectionString'))
            container_client = blob_service_client.get_container_client(catalog.get('containerName'))
            blob_client = container_client.get_blob_client(file_path)
            return blob_client
        except Exception as e:
            raise AzureException(message=UNEXPECTED_ERROR, error=str(e), status_code=APP_ERROR)

    async def get_file(self, file_path: str) -> bytes:
        """ Download a file from blob storage """
        try:
            blob_client = await self._get_blob_client(file_path)
            blob_data = await blob_client.download_blob()
            file_bytes = await blob_data.readall()
            return file_bytes
        except Exception as e:
            raise AzureException(message=UNEXPECTED_ERROR, error=str(e), status_code=APP_ERROR) 

    async def store_file(self, file_bytes: bytes, file_path: str) -> None:
        """ Upload a file to blob storage """
        try:
            blob_client = await self._get_blob_client(file_path)
            await blob_client.upload_blob(file_bytes, overwrite=True)
        except Exception as e:
            raise AzureException(message=UNEXPECTED_ERROR, error=str(e), status_code=APP_ERROR) 

    async def delete_file(self, file_path: str) -> None:
        """ Delete a file from blob storage """
        try:
            blob_client = await self._get_blob_client(file_path)
            await blob_client.delete_blob()
        except Exception as e:
            raise AzureException(message=UNEXPECTED_ERROR, error=str(e), status_code=APP_ERROR) 
