tag=$(docker container ls | grep chat_demo | awk '{print $1}')
echo $tag
docker container stop $tag
docker container rm $tag
cd /home/works/yangte/chat_demo/
docker build -t manbug/chat_demo:v1 -f dockerfile-dev .
docker run -p 8646:8646 -d manbug/chat_demo:v1
