## Install

Prerequisites:
- `ruby`
- `bundler`

Install dependent libraries:

```bash
bundle install --path vendor/bundle
```

## Build the document
```bash
./generate.sh main.adoc
```

## Source structure

* `main.adoc`: Main document
* `/dist`: Output document (both HTML and PDF) will be generated here
* `/imgs`: Put image files here
