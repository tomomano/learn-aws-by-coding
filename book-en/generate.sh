file=$1

echo generating html... "${file%.*}"
bundler exec asciidoctor -o "dist/index.html" $file
cp -r imgs dist/

echo Green generating pdf by asciidoctor-pdf with thema ...
bundler exec asciidoctor -o "dist/${file%.*}.pdf" \
-r asciidoctor-pdf -d book -a "data-uri!" $file
