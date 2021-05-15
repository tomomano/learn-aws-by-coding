import json, os, uuid, decimal
from datetime import datetime, timezone
import boto3

ddb = boto3.resource("dynamodb")
table = ddb.Table(os.environ["TABLE_NAME"])

HEADERS = {
    "Access-Control-Allow-Origin": "*",
}

# this custom class is to handle decimal.Decimal objects in json.dumps()
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

def get_haiku(event, context):
    """
    handler for GET /haiku
    """
    try:
        response = table.scan()

        status_code = 200
        resp = response.get("Items")
    except Exception as e:
        status_code = 500
        resp = {"description": f"Internal server error. {str(e)}"}
    return {
        "statusCode": status_code,
        "headers": HEADERS,
        "body": json.dumps(resp, cls=DecimalEncoder)
    }

def post_haiku(event, context):
    """
    handler for POST /haiku
    """
    try:
        body = event.get("body")
        if not body:
            raise ValueError("Invalid request. The request body is missing!")
        body = json.loads(body)

        for key in ["username", "first", "second", "third"]:
            if not body.get(key):
                raise ValueError(f"{key} is empty")

        item = {
            "item_id": uuid.uuid4().hex,
            "username": body["username"],
            "first": body["first"],
            "second": body["second"],
            "third": body["third"],
            "likes": 0,
            "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds")
        }
        response = table.put_item(Item=item)

        status_code = 201
        resp = {"description": "Successfully added a new haiku"}
    except ValueError as e:
        status_code = 400
        resp = {"description": f"Bad request. {str(e)}"}
    except Exception as e:
        status_code = 500
        resp = {"description": str(e)}
    return {
        "statusCode": status_code,
        "headers": HEADERS,
        "body": json.dumps(resp)
    }

def patch_haiku(event, context):
    """
    handler for PATCH /haiku/{item_id}
    """
    try:
        path_params = event.get("pathParameters", {})
        item_id = path_params.get("item_id", "")
        if not item_id:
            raise ValueError("Invalid request. The path parameter 'item_id' is missing")
        
        response = table.update_item(
            Key={"item_id": item_id},
            UpdateExpression=f"SET likes = likes + :inc",
            ExpressionAttributeValues={
                ':inc': 1,
            }
        )

        status_code = 200
        resp = {"description": "OK"}
    except ValueError as e:
        status_code = 400
        resp = {"description": f"Bad request. {str(e)}"}
    except Exception as e:
        status_code = 500
        resp = {"description": str(e)}
    return {
        "statusCode": status_code,
        "headers": HEADERS,
        "body": json.dumps(resp)
    }

def delete_haiku(event, context):
    """
    handler for DELETE /haiku/{item_id}
    """
    try:
        path_params = event.get("pathParameters", {})
        item_id = path_params.get("item_id", "")
        if not item_id:
            raise ValueError("Invalid request. The path parameter 'item_id' is missing")
        
        response = table.delete_item(
            Key={"item_id": item_id}
        )

        status_code = 204
        resp = {"description": "Successfully deleted."}
    except ValueError as e:
        status_code = 400
        resp = {"description": f"Bad request. {str(e)}"}
    except Exception as e:
        status_code = 500
        resp = {"description": str(e)}
    return {
        "statusCode": status_code,
        "headers": HEADERS,
        "body": json.dumps(resp)
    }
