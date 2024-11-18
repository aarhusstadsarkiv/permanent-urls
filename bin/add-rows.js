// get first parameter 'url' from the command line
// get second parameter 'num_rows' from the command line
const url = process.argv[2];
const num_rows = process.argv[3];

// if not parameters passed, show error message
if (!url || !num_rows) {
    console.log('Please provide URL and number of rows.');
    process.exit(1);
}


function generateRandomString() {
    return Math.random().toString(36).substr(2, 7);
}

// Add rows to the CSV file in this format
// File,URL
// random-string.html,url
const fs = require('fs');

const rows = [];
for (let i = 0; i < num_rows; i++) {
    const randomString = generateRandomString();
    const fileName = randomString + '.html';
    rows.push(`${fileName},${url}`);
}

fs.appendFileSync('bin/redirects.csv', '\n' + rows.join('\n') );
console.log('Rows have been added successfully.');