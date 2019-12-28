sudo docker rm test-flask-1 -f
sudo docker run -d -p 80:80 --name test-flask-1 testflask

