// Get a list of all files in the current directory ending with .html
const fs = require('fs');
const path = require('path');

const files = fs.readdirSync(process.cwd());
let htmlFiles = files.filter(file => path.extname(file) === '.html');

// Remove index.html and template.html from the list
const removeFiles = ['index.html', 'template.html'];
htmlFiles = htmlFiles.filter(file => !removeFiles.includes(file));

// Read each html file and extract first https link
let mdStringOfLinks = '';
htmlFiles.forEach(file => {
  const data = fs.readFileSync(file, 'utf8');
    const regex = /https:\/\/[^\s"]+/;
    const match = data.match(regex);
    console.log(`${file}: ${match[0]}`);

    const url = match[0];
    mdStringOfLinks += `[${file}](${url})\n\n`;

});

// Write the list to a markdown file
fs.writeFileSync('list/README.md', mdStringOfLinks);
