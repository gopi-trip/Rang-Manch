from fastapi.responses import JSONResponse
from fastapi import Response, Request

class NoReviewsFound(Exception):
    def __init__(self, play_name:str,id:int):
        self.play_name = play_name

class NoReviewFound(Exception):
    def __init__(self, id:int):
        self.id = id


# Creating Handlers
async def no_reviews_found_handler(request: Request, exception:NoReviewsFound):
    return JSONResponse(
        status_code=404,
        content={
            "Error":"There are no reviews for the play: {exception.play_name}"
        }
    )

async def no_review_found_handler(request:Request,exception:NoReviewFound):
    return JSONResponse(
        status_code=404,
        content={
            "Error":"There is no review with the id: {exception.id}"
        }
    )