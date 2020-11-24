""" Dynamodb Delete Data."""
import json
from boto3.session import Session

REGION_NAME = "ap-northeast-1"
TABLE_NAME = "hoge"


def lambda_handler(event, context):
    # 手元で叩けるようにSessionを使う（credentialsが正しく設定されているなら必要ない）
    session = Session(
        aws_access_key_id="XXXXXXXXX",
        aws_secret_access_key="XXXXXXXXXXXXXXXXXXXXXX",
        region_name=TABLE_NAME,
    )
    dynamodb = session.resource("dynamodb", region_name=REGION_NAME)
    table = dynamodb.Table(TABLE_NAME)

    delete_items = []
    parameters = {}
    # 削除するときには余分なキーを含めないようにする必要がある
    key_names = [x["AttributeName"] for x in table.key_schema]
    sum = 0
    # 一度のscanで全件取れない場合、取った件数を削除→LastEvaluatedKeyを使用して再取得……を繰り返す
    while True:
        resp = table.scan(**parameters)
        delete_items = resp["Items"]
        delete_keys = [{k: v for k, v in x.items() if k in key_names} for x in delete_items]
        with table.batch_writer() as batch:
            for key in delete_keys:
                batch.delete_item(Key=key)
        sum = sum + len(delete_items)
        print(sum)  # 進捗確認用
        if "LastEvaluatedKey" in resp:
            parameters["ExclusiveStartKey"] = resp["LastEvaluatedKey"]
        else:
            break

    return {"statusCode": 200, "body": json.dumps("delete data count: {}".format(sum))}


if __name__ == "__main__":
    lambda_handler({}, ())
