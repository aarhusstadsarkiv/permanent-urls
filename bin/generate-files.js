import fs from 'fs';
import csv from 'csv-parser';

// Function to generate HTML file
function generateHtml(file, url) {
    const htmlContent = `<!DOCTYPE html>
<html lang="da">
    <head>
        <meta charset="utf-8">
        <script>window.location.href = "${url}";</script>
        <meta name="robots" content="noindex, nofollow">
    </head>
    <body>
        <noscript>
            <meta http-equiv="refresh" content="0;url=${url}">
        </noscript>
    </body>
</html>`;
    fs.writeFileSync(file, htmlContent);
}

// Read the CSV and generate HTML files
fs.createReadStream('bin/redirects.csv')
    .pipe(csv())
    .on('data', (row) => {
        const fileName = row['File'];
        const url = row['URL'];
        generateHtml(fileName, url);
    })
    .on('end', () => {
        console.log('HTML files have been generated successfully.');
    });
