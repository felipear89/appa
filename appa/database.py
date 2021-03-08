import motor.motor_asyncio

from appa.config import MONGO_URI, DATABASE_NAME

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)

database = client[DATABASE_NAME]

features_coll = database["features"]
scenario_log_coll = database["scenario_log"]


async def find_feature_by_name(name: str) -> dict:
    feature = await features_coll.find_one({"name": name})
    return feature


async def find_scenario_log_by_id(_id: str) -> dict:
    scenario_log = await scenario_log_coll.find_one({"_id": _id})
    return scenario_log


async def update_scenario_log(scenario_log) -> dict:
    scenario_log = await scenario_log_coll.replace_one({
        "_id": scenario_log["_id"]
    }, scenario_log)
    return scenario_log


async def insert_scenario_log(_id, created_at, updated_at, payload, scenario) -> dict:
    feature = await scenario_log_coll.insert_one({
        "_id": _id,
        "created_at": created_at,
        "updated_at": updated_at,
        "initial_response": payload,
        "scenario": scenario
    })
    return feature
