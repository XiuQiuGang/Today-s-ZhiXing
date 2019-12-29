import os
import tempfile
import pytest
from project import create_app
import json
import io

app = create_app()
os.system("sh init_db.sh")

@pytest.fixture
def client():
    #os.system("sh init_db.sh")
    yield app.test_client()


def test_ping(client):
    """Start with a blank database."""

    response = client.get('/Hello')

    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert "Hello, World!" == data['message']


def test_register(client):
    
    response = client.post(
        '/register',
        data=json.dumps(dict(
            username='huzujun',
	        password='1234',
            email='17301095@bjtu.edu.cn'
        )),
        content_type='application/json',
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert 0 == data['status_code']    

    response = client.post(
        '/register',
        data=json.dumps(dict(
            username='huzujun',
	        password='1234',
            email='17301095@bjtu.edu.cn'
        )),
        content_type='application/json',
    )
    data = json.loads(response.data.decode())
    assert 1 == data['status_code'] 

    response = client.post(
        '/register',
        data=json.dumps(dict(
            username='abc',
	        password='1234',
            email='17301095@bjtu.edu.cn'
        )),
        content_type='application/json',
    )
    data = json.loads(response.data.decode())
    assert 2 == data['status_code']          
    
    response = client.post(
        '/register',
        data=json.dumps(dict(
            username='abc',
	        password='1234',
            email='17301095@163.com'
        )),
        content_type='application/json',
    )
    data = json.loads(response.data.decode())
    assert 3 == data['status_code']    

    response = client.post(
        '/register',
        data=json.dumps(dict(
            username='gang',
	        password='1234',
            email='17301094@bjtu.edu.cn'
        )),
        content_type='application/json',
    )
    data = json.loads(response.data.decode())
    assert 0 == data['status_code']    


def test_modify_information(client):
    response = client.put(
        '/edit_user_info',
        data=json.dumps(dict(
            user_id=1,
	        nick_name='Master',
            intro="balabala",
            profile= "http://120.27.247.14/static/5.png",
        )),
        content_type='application/json',
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 200


def test_login(client):
    
    response = client.post(
        '/login',
        data=json.dumps(dict(
            username='huzujun',
	        password='1234'
        )),
        content_type='application/json',
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert 0 == data['status_code']    
    assert 1 == data['user_id'] 

    response = client.post(
        '/login',
        data=json.dumps(dict(
            username='gang',
	        password='1234'
        )),
        content_type='application/json',
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert 1 == data['status_code']    
    assert 2 == data['user_id']      

    response = client.post(
        '/login',
        data=json.dumps(dict(
            username='huzu',
	        password='1234'
        )),
        content_type='application/json',
    )
    data = json.loads(response.data.decode())
    assert 2 == data['status_code'] 

    response = client.post(
        '/login',
        data=json.dumps(dict(
            username='huzujun',
	        password='12345'
        )),
        content_type='application/json',
    )
    data = json.loads(response.data.decode())
    assert 3 == data['status_code']          


def test_view_user_info(client):
    
    response = client.get(
        '/view_user_info?user_id=1',
        data={}
    )

    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert "Master" == data['nick_name'] 


def test_post(client):
    for i in range(1, 21):
        with open("some_posts/{}.txt".format(i), "r") as f:
            lines = f.readlines()
            s = ""
            for line in lines:
                s += line + '\n'
            assert s != ""
            path = ""
            if os.path.exists("some_posts/{}.jpg".format(i)):
                path = "some_posts/{}.jpg".format(i)
            elif os.path.exists("some_posts/{}.mp4".format(i)):
                path = "some_posts/{}.mp4".format(i)
            else:
                path = "some_posts/blog-author.jpg"

            #basedir = os.path.abspath(os.path.dirname(__file__))
            with open(path, 'rb') as img1:
                img1StringIO = io.BytesIO(img1.read())
            data = dict(image=(img1StringIO, path))
            response = client.post(
                '/image', data=data,
                follow_redirects=True
            )
            url = json.loads(response.data.decode())
            
            data = {
                "img": url,
                "content": s,
                "circle_id": 1,
                "user_id": 1
            }

            data = {key: str(value) for key, value in data.items()}

            response = client.post(
                '/post', data=data, content_type='multipart/form-data'
            )
            assert response.status_code == 200
                

def test_history_post(client):
    
    response = client.get(
        '/history_post?user_id=1',
        data={}
    )
    assert response.status_code == 200


def test_comment(client):
    response = client.post(
        '/comment?post_id=1&user_id=1&content=hA'
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 200

    response = client.post(
        '/comment?post_id=1&user_id=2&content=emmmm'
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 200


def test_view_comment(client):
    response = client.get(
        '/comment?post_id=1'
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    print(data)
    assert len(data) == 2


def test_like(client):
    response = client.post(
        '/like_post?post_id=1&user_id=1'
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    print(data)

    response = client.post(
        '/like_post?post_id=1&user_id=1'
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    print(data)

    response = client.post(
        '/like_post?post_id=1&user_id=2'
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    print(data)


def test_favorite(client):
    response = client.post(
        '/favorite?post_id=1&user_id=1'
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    print(data)

    response = client.post(
        '/favorite?post_id=1&user_id=1'
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert 'message' in data

    response = client.post(
        '/favorite?post_id=1&user_id=2'
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    print(data)


def test_get_by_circle(client):
    response = client.get(
        '/get_by_circle?circle_id=1&user_id=2&start=1&end=5'
    )
    data = json.loads(response.data.decode())
    print(data[0])
    assert response.status_code == 200
    assert len(data) == 5
    assert data[0]['likes'] == 2


def test_join_circle(client):
    response = client.post(
        '/join_circle?circle_name=魔方&user_id=1'
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 200

    response = client.post(
        '/join_circle?circle_name=学习&user_id=1'
    )
    data = json.loads(response.data.decode())
    print(data)
    assert response.status_code == 200


def test_view_circles(client):
    response = client.get(
        '/view_circles'
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert len(data) == 2


def test_view_circles(client):
    response = client.post(
        '/block_post?post_id=1&user_id=1'
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 200

    response = client.get(
        '/get_by_circle?circle_id=1&user_id=1&start=1&end=5'
    )
    data = json.loads(response.data.decode())
    print(data[0])
    assert data[0]['post_id'] != 1
    assert response.status_code == 200
    print(data)