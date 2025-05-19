from src.fastapi_app.utils.db_operations import (get_by_id, retrieve_all_data,
                                                 get_hazardous_objs, get_top_n_largest, search_asteroids,
                                                 asteroids_stats)
from src.classes.query_classes import IdQuery, SearchQuery, LargestQuery
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
import json

router = APIRouter()


@router.get('')
def get_all_objs():
    """
    Retrieve all asteroid objects from the database.

    Returns:
        200 OK: A list of all asteroid objects as JSON.
        500 Internal Server Error: If a database or server error occurs.
    """
    try:
        json_obj = retrieve_all_data()
        return JSONResponse(content=json.loads(json.dumps(json_obj, ensure_ascii=False)))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/id')
def get_asteroid_by_id(query: IdQuery):
    """
    Retrieve a specific asteroid by its ID.

    Parameters:
        query (IdQuery): JSON body containing the 'id' of the asteroid.

    Returns:
        200 OK: A list with the matching asteroid object (if found).
        500 Internal Server Error: If a database or server error occurs.
    """
    try:
        json_obj = get_by_id(query.id)
        return JSONResponse(content=json.loads(json.dumps(json_obj, ensure_ascii=False)))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search")
def get_asteroid_by_search(query: SearchQuery):
    """
    Search for asteroids based on multiple filter criteria.

    Parameters:
        query (SearchQuery): JSON body with optional search filters:
            - name (str): Partial match for the asteroid name.
            - abs_mag_min / abs_mag_max (float): Range for absolute magnitude.
            - diameter_min / diameter_max (float): Range for asteroid diameter.
            - inclination_min / inclination_max (float): Range for inclination angle.

    Returns:
        200 OK: A list of asteroid objects matching the search criteria.
        500 Internal Server Error: If a database or server error occurs.
    """
    try:
        json_obj = search_asteroids(query)
        return JSONResponse(content=json.loads(json.dumps(json_obj, ensure_ascii=False)))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    pass


@router.post("/largest")
def get_largest_asteroids(query: LargestQuery):
    """
    Retrieve the top N largest asteroids by maximum diameter.

    Parameters:
       query (LargestQuery): JSON body with:
           - top_n (int): Number of largest asteroids to return.

    Returns:
        200 OK: A list of the top N largest asteroids.
        500 Internal Server Error: If a database or server error occurs.
    """
    try:
        json_obj = get_top_n_largest(query.top_n)
        return JSONResponse(content=json.loads(json.dumps(json_obj, ensure_ascii=False)))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/hazardous')
def get_hazardous_asteroids():
    """
    Retrieve all asteroids flagged as hazardous.

    Returns:
        200 OK: A list of hazardous asteroid objects.
        500 Internal Server Error: If a database or server error occurs.
    """
    try:
        json_obj = get_hazardous_objs()
        return JSONResponse(content=json.loads(json.dumps(json_obj, ensure_ascii=False)))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/stats')
def get_asteroid_stats():
    """
    Generate statistics about the asteroid dataset.

    Returns:
        200 OK: A JSON object with summary statistics including:
            - General info (count, hazardous percentage)
            - Brightness (min/max/mean/std of absolute magnitude)
            - Dimensions (min/max/mean/std of diameter)
            - Orbit details (eccentricity metrics, extreme orbits)

        500 Internal Server Error: If a database or server error occurs.
    """
    try:
        json_obj = asteroids_stats()
        return JSONResponse(content=json.loads(json.dumps(json_obj, ensure_ascii=False)))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
