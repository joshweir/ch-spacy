docker build -t joshweir/ch-spacy-server .
docker push -t joshweir/ch-spacy-server

# run server: 
# docker run -it --rm -p "127.0.0.1:8080:80" joshweir/ch-spacy-server

# calling:
# curl -H "Content-Type:text/plain" --data-binary "Penguins are birds, they are great." 'http://localhost:8080' | jq

# optionally clean input and/or retrieve noun chunks
# curl -H "Content-Type:text/plain" --data-binary "Penguins are birds, they are great." 'http://localhost:8080?clean=1&nounchunks=1' | jq

# parses by paragraph:
# curl -H "Content-Type:text/plain" --data-binary "This is a paragraph.

# Penguins are a bird from antartica." 'http://localhost:8080' | jq