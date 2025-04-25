import fs from 'fs';
import { generateRandomString, getUrlsFromCsv, existingUrls, existingFileNames } from './utils.js';

if (process.argv.length < 4) {
    console.log('Please provide the CSV file name and the column name to read URLs from.');
    console.log('Example: node bin/add-csv.js redirects.csv column_name');
    process.exit(1);
}

const inputFileName = process.argv[2];
const urlColumn = process.argv[3];

// New Get new URLs to be added. importsUrls is an array of URLs
const importUrls = await getUrlsFromCsv(inputFileName, urlColumn);

// Output CSV file
const outputCsv = 'bin/redirects.csv';

// Output CSV file has the following format:
// 
// File,URL
// 0taceun.html,https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-broer/gangbroen-ved-brabrandstien/?utm_source=qr&utm_campaign=byens-broer
// 0zkjy.html,https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-lystbaadehavn/p-clausens-fiskehandel/?utm_source=qr&utm_campaign=byens-lystbaadehavn
// ...

// Only add new URLs that are not already in 'existingFileNames'
const newUrls = importUrls.filter(url => !existingUrls.includes(url));
const newFileNames = newUrls.map(() => generateRandomString() + '.html');
const newRedirects = newUrls.map((url, index) => ({
    fileName: newFileNames[index],
    url: url
}));

const csvLines = newRedirects.map(redirect => `${redirect.fileName},${redirect.url}`);
fs.appendFileSync(outputCsv, csvLines.join('\n'), 'utf8');

console.log('New URLs have been added to the CSV file.');
