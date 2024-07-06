# 논문 API
## GET /paper

paper 목록 리턴

```json
{
  "data": {
    "papers": [
      {
        "id": 1,
        "title": "title",
        "author": "author",
        "abstract": "abstract"
      }
    ]
  }
}
```

## POST /paper

pdf base64로 업로드

## GET /paper/:id

paper 상세 리턴

```json
{
  "data": {
    "paper": {
      "id": 1,
      "title": "title",
      "author": "author",
      "abstract": "abstract",
      "raw": "html"
    }
  }
}
```

## POST /paper/:id/kor

paper 번역

```json
{
  "data": {
    "paper": {
      "id": 1,
      "title": "title",
      "author": "author",
      "abstract": "abstract",
      "raw": "korean html"
    }
  }
}
```
# 챗봇 API
## POST /chat

AI 응답

request
```json
{
  "body": "user request",
  "refer": [1, 2, 3]
}
```

response
```json
{
  "data": {
    "body": "ai response"
  }
}
```