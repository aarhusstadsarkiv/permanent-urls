# permanent-urls

This repository contains and generates permanent URLs for the Aarhus City Archives.

Usage could be QR codes. The QR code could be printed on a physical object, e.g. a bridge, a building, a statue, a sign, etc. The QR code could be scanned by a mobile device, which would take the user to the permanent URL - and then this URL would redirect the user to the real URL. This way, the real URL could be changed without having to change the QR code.

    QR code -> permanent URL -> real URL

## Installation

    git clone git@github.com:aarhusstadsarkiv/permanent-urls.git
    cd permanent-urls
    npm install

## URL generation and update

The redirect URLs should be placed in the [bin/redirects.csv](bin/redirects.csv) file.

The `File` column is the filename of the permanent URL. The `URL` column is the URL where the client will be redirected.

You may add a new permanent URL by adding a new line to this CSV file.

The following can generate a random file name:

    node bin/random.js

Insert the generated file name in the [bin/redirects.csv](bin/redirects.csv) file. 
Add the generated html string in the `File` column and add a URL (where to redirect to) in the `URL` column.

Generate and update existing files (from CSV) by running the following command:

    node bin/generate-files.js

Now you can `commit` and `push` the changes with the new and updated files.

Your new permanent URLs will be available at an address like the following:

    https://purl.aarhusstadsarkiv.dk/<file-name>

E.g.:

https://purl.aarhusstadsarkiv.dk/0taceun.html

In order to generate a QR for a permanent URL, you may use a service like [qr.io](https://qr.io/)

## Adding multiple line

If you need to add multiple lines you may use a `csv` file in order to add multiple new lines. 
The following command will add `URL`s (and generate `File` names ) based on the column with index 2 
of the `bin/import.csv` file. 

    node bin/add-from-csv.js bin/import.csv 2

## Check URLs

Check all URLs by using the following command.

    node bin/check-urls.js

If no response or non 2xx reponse then the URL will be printed in the console.
