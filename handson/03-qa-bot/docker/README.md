### Building docker

```bash
docker build -t transformer .
```

### Running docker

```bash
$ docker run transformer \
"Pipeline have been included in the huggingface/transformers repository" \
"What is the name of the repository ?" \
"randomstringxxxx" \
--no_save
```

Expected output
```bash
{'score': 0.5135614620774795, 'start': 35, 'end': 59, 'answer': 'huggingface/transformers'}
```
