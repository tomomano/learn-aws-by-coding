import unittest
import requests
import os, warnings, time, io, uuid
from datetime import datetime, timezone
import boto3

class TestApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>") 

        # get parameters from SSM
        ssm_client = boto3.client("ssm")
        ENDPOINT_URL = ssm_client.get_parameter(Name="ENDPOINT_URL")["Parameter"]["Value"]
        TABLE_NAME = ssm_client.get_parameter(Name="TABLE_NAME")["Parameter"]["Value"]

        # put some test data in DB
        ddb = boto3.resource("dynamodb")
        table = ddb.Table(TABLE_NAME)
        test_item_ids = []
        for i in range(2):
            new_id = uuid.uuid4().hex
            response = table.put_item(Item={
                "item_id": new_id,
                "username": "正岡子規",
                "first": "柿くへば",
                "second": "鐘が鳴るなり",
                "third": "法隆寺",
                "likes": 0,
                "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds")
            })
            test_item_ids.append(new_id)

        cls.ENDPOINT_URL = ENDPOINT_URL
        cls.TABLE_NAME = TABLE_NAME
        cls.test_item_ids = test_item_ids

    @classmethod
    def tearDownClass(cls):
        # delete test data
        ddb = boto3.resource("dynamodb")
        table = ddb.Table(cls.TABLE_NAME)
        for item_id in cls.test_item_ids:
            response = table.delete_item(
                Key={"item_id": item_id}
            )

    def test_get_haiku(self):
        """
        Test case for GET /haiku
        """
        resp = requests.get(
            self.ENDPOINT_URL + "/haiku"
        )
        self.assertEqual(200, resp.status_code)

        item = resp.json()[0]
        for key in ["item_id", "username", "first", "second", "third", "likes", "created_at"]:
            self.assertIn(key, item)

    def test_post_haiku(self):
        """
        Test case for POST /haiku
        """
        resp = requests.post(
            self.ENDPOINT_URL + "/haiku",
            json={
                "username": "松尾芭蕉",
                "first": "閑さや",
                "second": "岩にしみ入る",
                "third": "蝉の声"
            }
        )
        self.assertEqual(201, resp.status_code)

    def test_patch_haiku(self):
        """
        Test case for PATCH /haiku/{item_id}
        """
        resp = requests.patch(
            self.ENDPOINT_URL + f"/haiku/{self.test_item_ids[0]}"
        )
        self.assertEqual(200, resp.status_code)

    def test_delete_haiku(self):
        """
        Test case for DELETE /haiku/{item_id}
        """
        resp = requests.delete(
            self.ENDPOINT_URL + f"/haiku/{self.test_item_ids[1]}"
        )
        self.assertEqual(204, resp.status_code)
