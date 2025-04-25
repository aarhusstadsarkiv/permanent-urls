import { existingUrls } from './utils.js';

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function checkUrls () {
    const failedUrls = [];

    for (const url of existingUrls) {
        try {
            const response = await fetch(url);
            if (response.ok) {
                console.log(`${url}: OK`);
            } else {
                console.log(`${url}: Error (${response.status})`);
                failedUrls.push(url);
            }
        } catch {
            console.log(`${url}: Error (Network Error)`);
            failedUrls.push(url);
        }

        await sleep(1000);
    }

    console.log('\nFailed URLs:', failedUrls);
    return failedUrls;
};

const failedUrls = await checkUrls();