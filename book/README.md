The source of the main text is here, written with [asciidoctor](https://asciidoctor.org/).

If you want to build the document from the source, follow these steps.

## Install

Prerequisites:
- `ruby`
- `bundler`

Install ruby libraries:

```bash
bundle install --path vendor/bundle
```

## Build the document

```bash
./generate.sh main.adoc
```

This will generate HTML and PDF documents in the directory named `dist/`.

## Source structure

* `main.adoc`: Main document
* `dist/`: Output document (both HTML and PDF) will be generated here
* `imgs/`: Put image files here
* `fonts/`, `pdf-style/`: Fonts and styles for PDF generation. Do not touch!
* `XXX.adoc`: One section per file
