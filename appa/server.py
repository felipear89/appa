import json
from datetime import datetime

import requests
from fastapi import FastAPI, Body
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from appa.database import find_feature_by_name, insert_scenario_log
from appa.database import find_scenario_log_by_id, update_scenario_log
from appa.events import *
from appa.models import TestCommand
from triggers.events import get_webhook_id, validate_webhook, get_initial_id

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    add_event("get_initial_id", get_initial_id)
    add_event("get_webhook_id", get_webhook_id)
    add_event("validate_webhook", validate_webhook)


def ResponseModel(data: dict, message="ok", code=200):
    return {
        "data": data,
        "code": code,
        "message": message,
    }


def ErrorResponseModel(error, code, message=""):
    return {"error": error, "code": code, "message": message}


@app.post("/test", status_code=status.HTTP_200_OK)
async def execute_test(test_command: TestCommand = Body(...)):
    test_command = jsonable_encoder(test_command)
    feature = await find_feature_by_name(test_command['feature_name'])
    if feature is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=ErrorResponseModel("FEATURE_NOT_FOUND", 404, "Feature not found"))

    responses = []
    for scenario in feature["scenarios"]:
        r = requests.post(scenario["url"], data=json.dumps(scenario["payload"]), headers=scenario["headers"])
        payload = r.json()
        responses.append(payload)
        get_id = get_action("get_initial_id")
        _id = get_id(payload)
        await insert_scenario_log(_id, datetime.utcnow(), datetime.utcnow(), payload, scenario)

    return ResponseModel({
        "scenarios_responses": responses
    })


@app.post("/webhook", status_code=status.HTTP_200_OK)
async def execute_test(payload=Body(...)):
    _id = get_action("get_webhook_id")(payload)
    scenario_log = await find_scenario_log_by_id(_id)
    messages = scenario_log.get("webhook_messages", [])
    messages.append(payload)
    scenario_log["webhook_messages"] = messages
    await update_scenario_log(scenario_log)
    get_action("validate_webhook")(scenario_log, payload)
