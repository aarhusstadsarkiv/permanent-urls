# permanent-urls

This repository contains and generates permanent URLs for the Aarhus City Archives.

Usage could be QR codes. The QR code could be printed on a physical object, e.g. a bridge, a building, a statue, a sign, etc. The QR code could be scanned by a mobile device, which would take the user to the permanent URL - and then this URL would redirect the user to the real URL. This way, the real URL could be changed without having to change the QR code.


    QR code -> permanent URL -> real URL

## URL generation and update

The redirect URLs should be placed in the [bin/redirects.csv](bin/redirects.csv) file.

The `File column` is the filename of the permanent URL. The `URL column` is the URL where the client will be redirected.

You may add a new permanent URL by adding a new line to this CSV file.

In order to generate the HTML files that do the redirects, you will need to install `csv-parser`:

    npm install

Generate and update existing files (from CSV) by running the following command:

    node bin/generate-files.js

Now you can `commit` and `push` the changes with the new and updated files.

Your new permanent URL will be available at an address like the following:

    https://purl.aarhusstadsarkiv.dk/<file-name>

E.g.:

https://purl.aarhusstadsarkiv.dk/0taceun.html

In order to generate a QR for a permanent URL, you can use a service like [qr.io](https://qr.io/)

## Random

Generate a random file name following the existing pattern by running the following command:

    node bin/random.js
