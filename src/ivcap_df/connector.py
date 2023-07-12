from __future__ import annotations ## needs to come first
from typing import IO, TYPE_CHECKING, Optional, Sequence
if TYPE_CHECKING:
    from .schema import Schema

import pandas as pd
from abc import ABC, abstractmethod

from ivcap_client import Artifact
from sys import maxsize as MAXSIZE

def _create_ivcap_connector(**kwargs):
    from .ivcap import IvcapConnector
    return IvcapConnector(**kwargs)
    #return IvcapConnector

def _create_cozo_connector(**kwargs):
    from .cozo import CozoConnector
    return CozoConnector.create(**kwargs)

def _create_db_connector(**kwargs):
    from .sql import SqlConnector
    return SqlConnector(**kwargs)

type2klass = {
    "ivcap": _create_ivcap_connector,
    "cozo": _create_cozo_connector,
    "db": _create_db_connector,
}

class Connector(ABC):

    def __new__(cls, *args, **kwargs):
        if kwargs.get('__recursive__') == True:
            obj = super().__new__(cls)
            return obj

        type = kwargs.get('type')
        if not type:
            raise Exception(f"Missing 'type' declaration for connector - {kwargs}")
        klass = type2klass.get(type)
        if not klass:
            raise Exception(f"Unsupported connector type {type} - [{', '.join(list(type2klass.keys()))}]")
        try:
            kwargs['__recursive__'] = True
            obj = klass(**kwargs)
            return obj
        except Exception as e:
            raise Exception(f"Failed to create connector of type {type} - {e}")
     
    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def insert_data_frame(self, df: pd.DataFrame, schema: Schema, ignoreDuplicateRecords = True):
        """Insert content of 'df' into table represented by 'schema'. If 'ignoreDuplicateRecords'
        is set, quietly drop any records in 'df' which have an identical 'record-id' to what is already
        stored in the table."""
        pass
    
    @abstractmethod
    def get_all_for_schema(self, schema: Schema) -> pd.DataFrame:
        """Get all accessible entities of type `Schema`.
        
        This query is primarily used for schemas representing 'controlled vocabulary'.

        Args:
            schema (Schema): Schema of elements queried.

        Returns:
            pd.DataFrame: A dataframe holding all accessible entities
        """
        pass

    @abstractmethod
    def query_to_df(self, query: str) -> pd.DataFrame:
        """Execute 'query' (connector specific) and return result as dataframe."""
        pass

    @abstractmethod
    def register_schema(self, schema: Schema, failQuietly = False, verbose=False):
        """Register the 'schema' in the metadata registry."""
        pass

    @abstractmethod
    def get_schema(self, name: str, verbose=False) -> Schema:
        pass

    @abstractmethod
    def get_all_schemas_for_namespace(self, name: str, verbose=False) -> Sequence[Schema]:
        pass

    @abstractmethod 
    def upload_artifact(self,
        *,
        name: Optional[str] = None,
        file_path: Optional[str] = None,
        io_stream: Optional[IO] = None,
        content_type:  Optional[str] = None, 
        content_size: Optional[int] = -1, 
        chunk_size: Optional[int] = MAXSIZE, 
        retries: Optional[int] = 0, 
        retry_delay: Optional[int] = 30
    ) -> Artifact:
        """Uploads content which is either identified as a `file_path` or `io_stream`. In the
        latter case, content type need to be provided.

        Args:
            file_path (Optional[str]): File to upload
            io_stream (Optional[IO]): Content as IO stream. 
            content_type (Optional[str]): Content type - needs to be declared for `io_stream`.
            content_size (Optional[int]): Overall size of content to be uploaded. Defaults to -1 (don't know).
            chunk_size (Optional[int]): Chunk size to use for each individual upload. Defaults to MAXSIZE.
            retries (Optional[int]): The number of attempts should be made in the case of a failed upload. Defaults to 0.
            retry_delay (Optional[int], optional): How long (in seconds) should we wait before retrying a failed upload attempt. Defaults to 30.
        """
        pass

def create_connector(**kwargs) -> Connector:
    type = kwargs.get('type')
    if not type:
        raise Exception(f"Missing 'type' declaration for connector - {kwargs}")
    klass = type2klass.get(type)
    if not klass:
        raise Exception(f"Unsupported connector type {type} - [{', '.join(list(type2klass.keys()))}]")
    return klass(**kwargs)



