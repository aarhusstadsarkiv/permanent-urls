const fs = require("fs")


/**
 * @param length {number}
 * @param base {number}
 * @returns {string}
 */
const randomName = (length = 6, base= 36) => {
  const min = length > 1 ? Math.pow(base, length - 1) : 0;
  const max = Math.pow(base, length);
  return Math.floor((Math.random() * (max - min)) + min).toString(base);
}


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