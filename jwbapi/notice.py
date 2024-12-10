from lxml import html
import requests

def getNotice():
    # 设置请求头
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    # 发送请求
    response = requests.get("https://jwb.xujc.com/tzgg/list1.htm", headers=headers)
    response.encoding = 'utf-8'  # 设置编码

    # 创建 lxml 树
    tree = html.fromstring(response.text)
    # 使用 XPath 查找所有的 <li> 元素
    li_elements = tree.xpath('//*[@id="wp_news_w7"]/ul/li')

    # 创建一个字典来存储结果
    articles_list = []

    # 遍历每个 <li> 元素
    for index, li_element in enumerate(li_elements, start=1):
        # 找到 <a> 标签
        href = li_element.xpath('div[1]/span/a/@href')[0]
        if href[:1] == "/":
            href = "https://jwb.xujc.com" + href
        title = li_element.xpath('div[1]/span/a/@title')[0]
        date = li_element.xpath('div[2]/span/text()')[0]
        
        # 将结果存入字典
        articles_list.append({
            'title': title,
            'href': href,
            'date': date
        })

    return articles_list
