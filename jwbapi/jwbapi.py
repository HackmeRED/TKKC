from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
import requests
import uvicorn
from datetime import datetime
from notice import getNotice

app = FastAPI()


# 定义请求模型
class NoticeRequest(BaseModel):
    token: str


# 定义响应模型
class NoticeResponse(BaseModel):
    id: str
    status: str
    msg: str


def generate_token():
    return str(uuid.uuid4())


TOKEN = generate_token()
# Slack Webhook 地址
SLACK_HOOK = ""

old_notices = []


# 教务系统API
@app.get("/jwb")
async def getJw():
    return getNotice()


# Slack Webhook
@app.post("/notice", response_model=NoticeResponse)
async def generate_token_endpoint(req: NoticeRequest):
    # 获取 Token
    access_token = req.token
    # 生成随机 token
    id = generate_token()

    if not access_token:
        raise HTTPException(status_code=400, detail="Token cannot be empty")
    if access_token != TOKEN:
        return NoticeResponse(id=id, status="failed", msg="access_token Incorrect")
    tmp_notices = getNotice()
    notices = []
    global old_notices
    for i in tmp_notices:
        new = True
        for j in old_notices:
            if i["title"] == j["title"]:
                new = False
                break
        if new:
            notices.append(i)

    old_notices = tmp_notices
    content = id
    content += "\n"
    if len(notices) > 0:
        for index, i in enumerate(notices):
            print(i)
            content += ">*{} {}*\n".format(index + 1, i["title"])
            content += "{}\n".format(i["href"])
            content += "{}\n".format(i["date"])
    else:
        return NoticeResponse(id=id, status="success", msg="Notices Not Change.")

    data = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":ghost: *{}*".format(datetime.now()),
                },
            },
            {"type": "section", "text": {"type": "mrkdwn", "text": content}},
        ]
    }

    try:
        r = requests.post(SLACK_HOOK, json=data)
        if r.text == "ok":
            return NoticeResponse(id=id, status="success", msg="")
    except:
        return NoticeResponse(id=id, status="failed", msg="Webhook Request Failed")

    return NoticeResponse(id=id, status="failed", msg="")


# 运行 FastAPI 应用
if __name__ == "__main__":
    print("Access Token:", TOKEN)

    uvicorn.run(app, host="0.0.0.0", port=8000)
