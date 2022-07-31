# Captcha Solver API

Title says it all

## Docs
No docs needed, check example folder for captcha (only one type of captcha supported for now). 

1. Make request 
2. Get solved captcha as json

Also try [Swagger UI Docs](https://captcha-solver-api2.herokuapp.com/docs) with captcha from [example](/example/) folder
## Example

#### JAVDB

[More captchas](/example/javdb/)

![captcha](./example/javdb/g.png)

```bash
# Request via cURL
curl -s -X 'POST' \
  'https://captcha-solver-api2.herokuapp.com/javdb' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@example/g.png;type=image/png' | jq . # "jq ." optional
```
```json
{
  "solved": "xiwlk"
}
```

#### Links
- [API / Site link](https://captcha-solver-api2.herokuapp.com/) (hosted on heroku free tier so 30sec delay is expected if dyno is sleeping otherwise takes avg 12sec to solve a captcha)

- [Model Storage](https://models.cloudflare-storage.workers.dev/) (Models are stored on google drive, using public google index to access)

- Inspired by [pythonlessons/CAPTCHA-solver](https://github.com/pythonlessons/CAPTCHA-solver)

---

<div align="center">
    <img src="https://img.shields.io/badge/Fastapi 0.78.0-lightblue?style=for-the-badge&logo=fastapi">
    <img src="https://img.shields.io/badge/Tensorflow 1.15.0-white?style=for-the-badge&logo=tensorflow">   
    <img src="https://img.shields.io/badge/OpenCV 4.6.0-blue?style=for-the-badge&logo=opencv">
</div>
