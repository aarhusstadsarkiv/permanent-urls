import csv from 'csv-parser';
import fs from 'fs';


/**
 * Get URLs from a CSV file
 * @param {*} fileName 
 * @param {*} urlColumnIndex 
 * @returns a promise that resolves to an array of URLs
 */
async function getUrlsFromCsv(fileName, urlColumnIndex) {
    return new Promise((resolve, reject) => {
        const urls = [];
        fs.createReadStream(fileName, { encoding: 'utf8' })
            .pipe(csv({ separator: ';', headers: false }))
            .on('data', (row) => {
                const url = row[urlColumnIndex];
                if (url && url.startsWith('http')) {
                    urls.push(url);
                }
            })
            .on('end', () => {
                resolve(urls);
            })
            .on('error', (error) => {
                reject(error);
            });
    });
}


/**
 * Read the ./bin/redirects.csv file
 * @returns a promise that resolves to an array of objects with fileName and url properties
 */
async function getRedirectsCsv() {
    return new Promise((resolve, reject) => {
        const redirects = [];
        fs.createReadStream('./bin/redirects.csv')
            .pipe(csv())
            .on('data', (row) => {
                const fileName = row['File'];
                const url = row['URL'];
                redirects.push({ fileName, url });
            })
            .on('end', () => {
                resolve(redirects);
            })
            .on('error', (error) => {
                reject(error);
            });
    });
}

const redirects = await getRedirectsCsv()

// Get existing URLs from redirects.csv

const existingUrls = redirects.map(redirect => redirect.url);

// Get existing file names from redirects.csv
const existingFileNames = redirects.map(redirect => redirect.fileName);

function generateRandomString() {

    // Ensure no duplicate random strings are generated
    const existingFiles = redirects.map(redirect => redirect.fileName);
    let randomString;
    do {
        randomString = Math.random().toString(36).substr(2, 7);
    } while (existingFiles.includes(randomString + '.html'));
    return randomString;
}

export { generateRandomString, getUrlsFromCsv, existingUrls, existingFileNames };