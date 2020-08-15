
from src.es.restAPIs.idxAPIs.idxManagement import DeleteIdxAPI


def delete_youtora_idx():
    """
    delete the index
    """
    DeleteIdxAPI.delete_idx(index="youtora")
