from notion.client import NotionClient
from notion.block import PageBlock, TextBlock, TodoBlock
from datetime import datetime
_NOTION_TOKEN_FILE = "./notion_interface/notion_token.txt"
_NOTION_URL_FILE = "./notion_interface/notion_account_tables.txt"
"""
"""
if __name__ == '__main__':
    f = open(_NOTION_TOKEN_FILE, 'r+')
    token = f.readline()
    f.close()

    f = open(_NOTION_URL_FILE, 'r+')
    url = f.readline()
    f.close()
    client = NotionClient(token[:-1])
    page = client.get_collection_view(url[:-1])
    """
        for row in page.collection.get_rows():
            print("name: {}".format(row))
        print("end")
        result = page.default_query().execute()
        for row in result:
            print(row)
    """
    aggregations = [{
        "property": "estimated_value",
        "aggregator": "sum",
        "id": "total_value",
    }]
