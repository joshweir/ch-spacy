docker build -t joshweir/ch-spacy-server .
docker push -t joshweir/ch-spacy-server

# run server: 
# docker run -it --rm -p "127.0.0.1:8080:80" joshweir/ch-spacy-server

# calling:
# curl -H "Content-Type:text/plain" --data-binary "Penguins are birds, they are great." http://localhost:8080 | jq