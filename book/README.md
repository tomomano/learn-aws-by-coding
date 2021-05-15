The source of the main text, written with [asciidoctor](https://asciidoctor.org/).

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
* `dist/`: Output document (both HTML and PDF) will be generated here
* `imgs/`: Put image files here
* `fonts/`, `pdf-style/`: Fonts and styles for PDF generation. Do not touch!
* `XXX.adoc`: One section per file
