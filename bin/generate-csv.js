const fs = require('fs');
const path = require('path');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;

// Get all HTML files except index.html and template.html
const files = fs.readdirSync(process.cwd());
const htmlFiles = files.filter(file => path.extname(file) === '.html' && !['index.html', 'template.html'].includes(file));

// Create a CSV writer instance
const csvWriter = createCsvWriter({
    path: 'list/links.csv',
    header: [
        {id: 'file', title: 'File'},
        {id: 'url', title: 'URL'}
    ]
});

// Prepare data for CSV
const csvData = htmlFiles.map(file => {
    const data = fs.readFileSync(file, 'utf8');
    const regex = /https:\/\/[^\s"]+/;
    const match = data.match(regex);
    return { file: file, url: match ? match[0] : 'No URL found' };
});

// Write data to CSV file
csvWriter
    .writeRecords(csvData)
    .then(() => console.log('The CSV file was written successfully.'));
