from fastapi import FastAPI
from starlette.requests import Request
from cons_based_resource_alloc.cakespies import runExample
from pydantic import BaseModel
import aiohttp

app = FastAPI()

class InputModel(BaseModel):
    bakeryName: str
    periodInDays: float
    numOfBakers: float
    packerWorkingDays: float
    priceOfCake: float
    priceOfPie: float
    numOfPackers: float
    bakerEffortForCake: float
    bakerEffortForPie: float
    bakeTimeCake: float
    bakeTimePie: float
    numOfOvens: float
    packerEffortForCake:float
    packerEffortForPie: float


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/test")
async def test_me(req: Request):
    bod = await req.body()
    print(f'Raw Body:\b{bod}')
    return {"tested"}

@app.post("/example")
async def example(exampleInputs: InputModel, req: Request):
    bod = await req.json()
    print(f'received request:\n{bod}')
    results = runExample(exampleInputs.dict())

    await callout(pies=results['pies'], cakes=results['cakes'], revenue=results['max_profit'], bakery=exampleInputs.bakeryName)

    return results


async def callout(pies: float, cakes: float, revenue: float, bakery: str):
    app_sheet_id = "763b2d4c-483f-4402-95e8-e6ca570acc2b"
    app_sheet_table = "bakeriesdata"
    app_sheet_api = f"https://api.appsheet.com/api/v2/apps/{app_sheet_id}/tables/{app_sheet_table}/Action"
    heads = {"ApplicationAccessKey": "V2-61wJZ-XOPjD-hG4Om-nIkfD-LESYh-1Iv8P-oy0hO-iQCR4"}
    heads["Content-Type"] = "application/json"

    # app_sheet_api = "https://webhook.site/98e518a7-2b83-4f6f-a6a1-4bf2c6e213e3"


    payload = {
        "Action": "Edit",
        "Properties": { "Locale": "en-US" },
        "Rows": [
            {
                "Bakery Name": bakery,
                "Target revenue": revenue,
                "Target Pies per Month": pies,
                "Target Cakes per Month": cakes
            }
        ]
    }

    async with aiohttp.request(method="POST", url=app_sheet_api, json=payload, headers=heads) as resp:
        print(f"calling out to {app_sheet_api}")
        print(await resp.text())

