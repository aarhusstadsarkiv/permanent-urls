# permanent-urls

This repository generates permanent URLs for the Aarhus City Archives.

The redirect URLs are placed in the [bin/redirects.csv](bin/redirects.csv) file.

The `File column` is the file name and the `URL column` is the URL where the client will be redirected.

You may add a new permanent URL by adding a new line to the file.

In order to generate files for all the URLs in the list, you will need install `csv-parser`. You can do this by running the following command:

    npm install

Generate and update existing files (from CSV) by running the following command:

    node bin/generate-files.js

And now you can `commit` and `push` the changes with the new files.

Your new permanent URL will be available at the following address:

    https://purl.aarhusstadsarkiv.dk/<file-name>.html

E.g.:

    https://purl.aarhusstadsarkiv.dk/0taceun.html

