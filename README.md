# permanent-urls

This repository has a online form to generate a file name and add html file content for a permanent URL.

You can also use a node js script to generate the filename and the html content.

The permanent URL will just redirect to another URL.

Here is an example of the code which is produced by the form: [k1o0rod.html](k1o0rod.html)

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

This is then the permanent URL that redirects to another URL: 

[https://purl.aarhusstadsarkiv.dk/k1o0rod.html](https://purl.aarhusstadsarkiv.dk/k1o0rod.html)

## Creating new permanent URLs

Using a html form:

https://aarhusstadsarkiv.github.io/permanent-urls

Enter a URL and generate a file name and generate html content (that redirects). 

Add this to the repository and commit and push.

Or easier (I think) using a node js script: 

    node generate.js  https://somesite.com/somepage.html

This will generate a file name and generate html content (that redirects).

Then commit and push.

## Note

In order to alter these redirecting pages when stadsarkiv.aarhus.dk changes homepage we will be able to 
alter https://stadsarkiv.aarhus.dk to the new homepage.


