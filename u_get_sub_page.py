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
    page = client.get_block(url[:-1])

    print("페이지 제목",page.title)
    # 텍스트 생성
