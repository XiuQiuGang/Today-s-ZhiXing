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
    
    response = client.get(
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

    response = client.get(
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

    response = client.get(
        '/login',
        data=json.dumps(dict(
            username='huzu',
	        password='1234'
        )),
        content_type='application/json',
    )
    data = json.loads(response.data.decode())
    assert 2 == data['status_code'] 

    response = client.get(
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


            basedir = os.path.abspath(os.path.dirname(__file__))
            data = {}
            data['image'] = (io.BytesIO(b"my file contents"), basedir+'/'+path)
            response = client.post(
                '/image', data=data, content_type='multipart/form-data'
            )
            url = response.data.decode()
            
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
        '/history_post?user_id=2',
        data={}
    )
    assert response.status_code == 200

