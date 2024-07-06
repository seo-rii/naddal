## GET /paper

paper 목록 리턴

```json
{
  "papers": [
    {
      "id": 1,
      "title": "title",
      "author": "author",
      "abstract": "abstract"
    }
  ]
}
```

## POST /paper

pdf base64로 업로드

## GET /paper/:id

paper 상세 리턴

```json
{
  "paper": {
    "id": 1,
    "title": "title",
    "author": "author",
    "abstract": "abstract",
    "raw": "html"
  }
}
```

## POST /paper/:id/kor

paper 번역

```json
{
  "paper": {
    "id": 1,
    "title": "title",
    "author": "author",
    "abstract": "abstract",
    "raw": "korean html"
  }
}
```
