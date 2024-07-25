# 논문 API
## GET /paper Done

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

## POST /paper Done

pdf base64로 업로드

## PATCH /paper/:id
paper HTML 수정

## GET /paper/:id Done

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
## GET /chat

채팅 목록 반환
response
```json
{
  "data": [
    {
      "id": 1,
      "title": "chat1"
    },
    {
      "id": 2,
      "title": "chat2"
    }
  ]
}
```
## POST /chat

AI 응답

request
```json
{
  "id": 1
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

# 마킹 API

## GET /mark

모든 논문 마킹 리스트

```json
{
  "mark": [
    {
      "start": 0,
      "end": 10,
      "preview": "HTML"
    },
    {
      "start": 20,
      "end": 24,
      "preview": "HTML 2"
    }
  ]
}
```

## PATCH /mark/:id

id번 논문 마킹 수정(없으면 생성)

reqest
```json
{
  "mark": [
    {
      "start": 0,
      "end": 10,
      "preview": "HTML"
    },
    {
      "start": 20,
      "end": 24,
      "preview": "HTML 2"
    }
  ]
}
```
