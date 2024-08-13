# permanent-urls

This repository generates permanent URLs for the Aarhus City Archives.

The redirect URLs should be placed in the [bin/redirects.csv](bin/redirects.csv) file.

The `File column` is the file name and the `URL column` is the URL where the client will be redirected.

You may add a new permanent URL by adding a new line to this CSV file.

In order to generate the HTML files that do the redirects, you will need to install `csv-parser`:

    npm install

Generate and update existing files (from CSV) by running the following command:

    node bin/generate-files.js

Now you can `commit` and `push` the changes with the new and updated files.

Your new permanent URL will be available at the following address:

    https://purl.aarhusstadsarkiv.dk/<file-name>.html

E.g.:

    https://purl.aarhusstadsarkiv.dk/0taceun.html

## Random

Generate a random file name following the existing pattern by running the following command:

    node bin/random.js

