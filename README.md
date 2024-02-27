# permanent-urls

This repository has an online form that will generate a file name and some html content for a permanent URL.

You may also use a node js script to generate the filename and the html content.

The permanent URL will just redirect to another URL.

Here is an example of the code which is produced by the form [k1o0rod.html](k1o0rod.html)

```html
<!DOCTYPE html>
<html lang="da">
    <head>
        <meta charset="utf-8">
        <script>window.location.href = "https://stadsarkiv.aarhus.dk/byhistorie/byens-broer/museumsbroen/?utm_source=qr&utm_campaign=byens-broer";</script>
        <meta name="robots" content="noindex, nofollow">
    </head>
</html>

<!--
k1o0rod.html
-->
```

Visiting the permanent URL that redirects: 

[https://purl.aarhusstadsarkiv.dk/k1o0rod.html](https://purl.aarhusstadsarkiv.dk/k1o0rod.html)

## Creating new permanent URLs

Using a html form:

https://aarhusstadsarkiv.github.io/permanent-urls

Enter a URL and generate a file name and some html content (that redirects). 

Add the generated file to the repository and `commit` and `push`.

Or easier (I think) using a node js script: 

    node generate.js https://somesite.com/somepage.html

This will generate a random file name and generate the html content (that redirects).

Then `commit` and `push`.

## Note

When stadsarkiv.aarhus.dk changes name to e.g. aarhus.dk/stadsarkiv, 
then we should alter https://stadsarkiv.aarhus.dk to the name of the new homepage.

## Existing list

See [list/README.md](list/README.md) for a list of existing permanent URLs.
