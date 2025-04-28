import { existingUrls } from './utils.js';
import { config } from './config.js';
import { logger } from './logging.js';

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function checkUrls() {
    const failedUrls = [];

    for (const url of existingUrls) {
        try {
            const response = await fetch(url);
            if (!response.ok) {
                logger.error(`URL check failed for ${url}: ${response.statusText}`);
                failedUrls.push(url);
            }
        } catch (err) {
            logger.error(`URL check threw error for ${url}: ${err.message}`);
            failedUrls.push(url);
        }

        await sleep(1000);
    }

    return failedUrls;
}

async function sendMattermostMessage(message) {
    const mattermostWebhookUrl = config.mattermostWebhookUrl;
    const payload = { text: message };
    const headers = { 'Content-Type': 'application/json' };

    try {
        const response = await fetch(mattermostWebhookUrl, {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            throw new Error(`Failed to send message: ${response.statusText}`);
        }
    } catch (error) {
        console.error(`Failed to send message: ${error}`);
    }
}

try {

    logger.info('Checking URLs...');
    const failedUrls = await checkUrls();

    if (failedUrls.length > 0) {
        logger.error('URLs failed. Sending Mattermost message...');
        const message = `The following URLs failed:\n${failedUrls.join('\n')}`;
        await sendMattermostMessage(message);
    }

} catch (error) {
    logger.error(`An error occurred while checking URLs : ${error}`);
}
