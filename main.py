from pprint import pprint

import httpx


def main():
    url = 'http://localhost:8000/api/token/'
    data = {
        'username': 'admin',
        'password': 'Qazasd@123',
    }
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMxNTE2MjQ3LCJpYXQiOjE3MzE1MTU5NDcsImp0aSI6Ijg3NGU0YzZkZTQzMzQ5M2U4Y2YyMmNmNDYzNjhmNmQ0IiwidXNlcl9pZCI6MX0.fSCkCDgXozD0BDg8a7T3pf88IpU3dGaKgu4c6e1Ymio"
    }
    # response = httpx.get(
    #     "http://localhost:8000/api/cities/",
    #     headers=headers, 
    #     follow_redirects=True
    # )
    response = httpx.post(
        "http://localhost:8000/api/cities/",
        headers=headers, 
        json={
            "name": "Test City",
            "description": "Test Description",
        }
    )
    # response = httpx.post(url, data=data)
    pprint(response.json())


if __name__ == '__main__':
    main()