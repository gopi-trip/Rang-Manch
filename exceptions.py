from fastapi.responses import JSONResponse
from fastapi import Response, Request

class NoReviewsFound(Exception):
    def __init__(self, play_name:str):
        self.play_name = play_name

# Creating Handlers
async def no_reviews_found_handler(request: Request, exception:NoReviewsFound):
    return JSONResponse(
        status_code=404,
        content={
            "Error":"There are no reviews for the play: {exception.play_name}"
        }
    )
