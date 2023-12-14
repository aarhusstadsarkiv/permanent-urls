const fs = require("fs")


/**
 * @returns {string}
 */
const randomName = () => Math.random().toString(36).substring(2, 7);


/**
 * @param url {string}
 * @returns {`<meta http-equiv="Refresh" content="0; URL=${string}"/>`}
 */
const metaRedirect = (url) => `<meta http-equiv="Refresh" content="0; URL=${url}"/>`


/**
 * @param url {string}
 * @returns {`<script>window.location.href = "${string}";</script>`}
 */
const jsRedirect = (url) => `<script>window.location.href = "${url}";</script>`


// noinspection HtmlRequiredLangAttribute,HtmlRequiredTitleElement
/**
 * @param url {string}
 * @param meta {boolean}
 * @returns {string}
 */
const template = (url, meta = true) => `<!DOCTYPE html>
<html>
<head>
<meta name="robots" content="noindex, nofollow">
${meta ? metaRedirect(url) : jsRedirect(url)}
</head>
</html>`.replace(/\n/g, "")


process.argv
    .slice(2)
    .map(u => u.trim())
    .filter(u => !!u)
    .forEach((url) => {
        const name = randomName()
        console.log(url)
        console.log(`https://purl.aarhusstadsarkiv.dk/${name}.html\n`)
        fs.writeFileSync(`${name}.html`, template(url))
    })