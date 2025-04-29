import { redirects } from './utils.js';
import { config } from './config.js';
import { logger } from './logging.js';
import fs from 'fs';

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function readFileAsString(filePath) {


    
}


async function checkUrls() {
    const failedUrls = [];

    for (const redirect of redirects) {

        // Read the file content
        // const fileContent = await readFileAsString(fileName);
        // console.log(fileContent);

        const fileName = redirect.fileName;
        const url = redirect.url;
        
        const fileStr = fs.readFileSync(fileName).toString()
        
        // Check if the URL is present in the file content
        if (!fileStr.includes(url)) {
            logger.error(`URL ${url} not found in file ${fileName}`);
            failedUrls.push(url);
        }


        // console.log(fileName)
        // try {
        //     const response = await fetch(fileName);
        //     if (!response.ok) {
        //         logger.error(`URL check failed for ${fileName}: ${response.statusText}`);
        //         failedUrls.push(fileName);
        //     }
        // } catch (err) {
        //     logger.error(`URL check threw error for ${fileName}: ${err.message}`);
        //     failedUrls.push(fileName);
        // }

        // await sleep(1000);
    }

    return failedUrls;
}


try {

    logger.info('Checking URLs...');
    const failedUrls = await checkUrls();

    if (failedUrls.length > 0) {
        logger.error('URLs failed. Sending Mattermost message...');
        const message = `The following URLs failed:\n${failedUrls.join('\n')}`;
    }

} catch (error) {
    logger.error(`An error occurred while checking URLs : ${error}`);
}
