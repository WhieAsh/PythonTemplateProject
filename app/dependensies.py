from fastapi import Response, HTTPException
import time


start_time = None
rate_interval = 10
rate_limit = 20
count = 0


def rete_limit_check(response:Response) -> Response:

    global start_time
    global count

    response.headers["X-app-rete-limit"]=f"{count}:{rate_limit}"

    if start_time is None:
        start_time = time.time()

    if start_time + rate_interval < time.time():
        count = 0
        start_time = time.time()

    if count >= rate_limit:
        raise HTTPException(status_code=429, detail={"rate_limit":rate_limit, "message":"You exceeded rate limit, please, wait "+ str(round(start_time + rate_interval - time.time(),2) + 0.01) + " sec"})

    count += 1

    return response
