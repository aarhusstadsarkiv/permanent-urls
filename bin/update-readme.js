import fs from 'fs';
import csv from 'csv-parser';
import path from 'path';

// File paths
const readmePath = path.join('README.md');
const csvPath = path.join('bin', 'redirects.csv');

// Read the README.md file
let readmeContent = fs.readFileSync(readmePath, 'utf8');

// Placeholder for PURLs
const purls = [];

// Read and parse the CSV file
fs.createReadStream(csvPath)
  .pipe(csv())
  .on('data', (row) => {
    if (row.File && row.URL) {
      const purlLink = `[https://purl.aarhusstadsarkiv.dk/${row.File}](https://purl.aarhusstadsarkiv.dk/${row.File})`
      const realURL = `[${row.URL}](${row.URL})`
      purls.push(`* ${purlLink} ->  `);
      purls.push(`${realURL}`);

    }
  })
  .on('end', () => {
    console.log('CSV file successfully processed.');

    // Generate the new PURLs list
    const purlsList = purls.join('\n');

    console.log(purlsList);

    // Replace the <!-- Existing PURLs --> section in README.md
    const updatedReadme = readmeContent.replace(
      /<!-- Existing PURLs -->[\s\S]*<!-- End PURLs -->/,
      `<!-- Existing PURLs -->\n${purlsList}\n<!-- End PURLs -->`
    );

    // Write the updated README.md file
    fs.writeFileSync(readmePath, updatedReadme, 'utf8');
    console.log('README.md successfully updated.');
  });
