docker build -t joshweir/ch-spacy-server --build-arg CACHEBUST=$(date +%s) .
docker push -t joshweir/ch-spacy-server

docker build -t joshweir/ch-spacy-server:dev --build-arg CACHEBUST=$(date +%s) -f Dockerfile.dev .
docker push -t joshweir/ch-spacy-server:dev

# run server: 
# docker run -it --rm -p "127.0.0.1:8080:80" joshweir/ch-spacy-server

# calling:
# curl -H "Content-Type:text/plain" --data-binary "Penguins are birds, they are great." 'http://localhost:8080' | jq

# optionally clean input and/or retrieve noun chunks
# curl -H "Content-Type:text/plain" --data-binary "Penguins are birds, they are great." 'http://localhost:8080?clean=1&nounchunks=1' | jq

# parses by paragraph:
# curl -H "Content-Type:text/plain" --data-binary "This is a paragraph.

# Penguins are a bird from antartica." 'http://localhost:8080' | jq

# if using joshweir/ch-spacy-server:with-summarizer
# curl -H "Content-Type:text/plain" --data-binary "Recent progress in hardware and methodology for training neural networks has ushered in a new generation of large networks trained on abundant data. These models have obtained notable gains in accuracy across many NLP tasks. However, these accuracy improvements depend on the availability of exceptionally large computational resources that necessitate similarly substantial energy consumption. As a result these models are costly to train and develop, both financially, due to the cost of hardware and electricity or cloud compute time, and environmentally, due to the carbon footprint required to fuel modern tensor processing hardware. In this paper we bring this issue to the attention of NLP researchers by quantifying the approximate financial and environmental costs of training a variety of recently successful neural network models for NLP. Based on these findings, we propose actionable recommendations to reduce costs and improve equity in NLP research and practice." 'http://localhost:8080/summarize'