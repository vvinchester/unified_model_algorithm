import json
import unittest
import datetime

with open("./data-1.json", "r") as f:
    jsonData1 = json.load(f)
with open("./data-2.json", "r") as f:
    jsonData2 = json.load(f)
with open("./data-result.json", "r") as f:
    jsonExpectedResult = json.load(f)


def convertFromFormat1(jsonObject):
    result = {
        "deviceID": jsonObject["deviceID"],
        "deviceType": jsonObject["deviceType"],
        "timestamp": jsonObject["timestamp"],
        "location": {
            "country": jsonObject["location"].split("/")[0],
            "city": jsonObject["location"].split("/")[1],
            "area": jsonObject["location"].split("/")[2],
            "factory": jsonObject["location"].split("/")[3],
            "section": jsonObject["location"].split("/")[4],
        },
        "data": {
            "status": jsonObject["operationStatus"],
            "temperature": jsonObject["temp"],
        },
    }
    return result


def convertFromFormat2(jsonObject):

    timestamp_str = jsonObject["timestamp"]
    timestamp = datetime.datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp() * 1000

    result = {
        "deviceID": jsonObject["device"]["id"],
        "deviceType": jsonObject["device"]["type"],
        "timestamp": timestamp,
        "location": {
            "country": jsonObject["country"],
            "city": jsonObject["city"],
            "area": jsonObject["area"],
            "factory": jsonObject["factory"],
            "section": jsonObject["section"],
        },
        "data": {
            "status": jsonObject["data"]["status"],
            "temperature": jsonObject["data"]["temperature"],
        },
    }
  
    return result


def main(jsonObject):
    result = {}

    if jsonObject.get("device") is None:
        result = convertFromFormat1(jsonObject)
    else:
        result = convertFromFormat2(jsonObject)

    return result


class TestSolution(unittest.TestCase):
    def test_sanity(self):
        result = main(jsonData1)
        self.assertEqual(result, jsonExpectedResult)

    def test_dataType1(self):
        result = main(jsonData1)
        self.assertEqual(
            result, jsonExpectedResult, "Converting from Type 1 failed"
        )

    def test_dataType2(self):
        result = main(jsonData2)
        self.assertEqual(
            result, jsonExpectedResult, "Converting from Type 2 failed"
        )


if __name__ == "__main__":
    unittest.main()
