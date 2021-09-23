from notion.client import NotionClient
from notion.block import PageBlock, TextBlock, TodoBlock
_NOTION_TOKEN_FILE = "./notion_token.txt"
_NOTION_URL_FILE = "./notion_url.txt"
"""
페이지를 가져올 수 있는 기능을 수행
"""
if __name__ == '__main__':
    f = open(_NOTION_TOKEN_FILE, 'r+')
    token = f.readline()
    f.close()

    f = open(_NOTION_URL_FILE, 'r+')
    url = f.readline()
    f.close()
    client = NotionClient(token_v2 =token )
    page = client.get_block(url)

    print("페이지 제목",page.title)
    page.title="new title"
    # 텍스트 생성
    text = page.children.add_new(TextBlock)
    text.title = "안녕하세요, 반갑습니다 🤞"
    # 체크박스 생성
    todo1 = page.children.add_new(TodoBlock)
    todo1.title = "아침 먹기"
    todo1.checked = True
    todo2 = page.children.add_new(TodoBlock)
    todo2.title = "점심 먹기"
    # 새로운 페이지 생성
    new_page = page.children.add_new(PageBlock)
    today = datetime.now().strftime('%Y-%m-%d')
    new_page.title = '{}에 생성된 페이지'.format(today)