# permanent-urls

This repository contains and generates permanent URLs for the Aarhus City Archives.

Usage could be QR codes. The QR code could be printed on a physical object, e.g. a bridge, a building, a statue, a sign, etc. The QR code could be scanned by a mobile device, which would take the user to the permanent URL - and then this URL would redirect the user to the real URL. This way, the real URL could be changed without having to change the QR code.


    QR code -> permanent URL -> real URL

## URL generation and update

The redirect URLs should be placed in the [bin/redirects.csv](bin/redirects.csv) file.

The `File column` is the filename of the permanent URL. The `URL column` is the URL where the client will be redirected.

You may add a new permanent URL by adding a new line to this CSV file.

In order to generate the HTML files that do the redirects, you will need to install `csv-parser`:

    npm install

Generate and update existing files (from CSV) by running the following command:

    node bin/generate-files.js

Now you can `commit` and `push` the changes with the new and updated files.

Your new permanent URL will be available at an address like the following:

    https://purl.aarhusstadsarkiv.dk/<file-name>

E.g.:

https://purl.aarhusstadsarkiv.dk/0taceun.html

In order to generate a QR for a permanent URL, you can use a service like [qr.io](https://qr.io/)

## Random

Generate a random file name following the existing pattern by running the following command:

    node bin/random.js

## Add multiple rows

You may add rows manually to the CSV file. 

But if need to add a lot of rows, you can use the following command:

    node bin/add-rows.js https://example.com 20

This will add 20 rows to the CSV file with the URL `https://example.com` and random file names.

You can then give the file names to the person who will print the QR codes.

<!-- Existing PURLs -->
* [https://purl.aarhusstadsarkiv.dk/0taceun.html](https://purl.aarhusstadsarkiv.dk/0taceun.html) ->  
[https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-broer/gangbroen-ved-brabrandstien/?utm_source=qr&utm_campaign=byens-broer](https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-broer/gangbroen-ved-brabrandstien/?utm_source=qr&utm_campaign=byens-broer)
* [https://purl.aarhusstadsarkiv.dk/0zkjy.html](https://purl.aarhusstadsarkiv.dk/0zkjy.html) ->  
[https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-lystbaadehavn/p-clausens-fiskehandel/?utm_source=qr&utm_campaign=byens-lystbaadehavn](https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-lystbaadehavn/p-clausens-fiskehandel/?utm_source=qr&utm_campaign=byens-lystbaadehavn)
* [https://purl.aarhusstadsarkiv.dk/3l4s2w3j.html](https://purl.aarhusstadsarkiv.dk/3l4s2w3j.html) ->  
[https://aarhuswiki.dk](https://aarhuswiki.dk)
* [https://purl.aarhusstadsarkiv.dk/3sr261g.html](https://purl.aarhusstadsarkiv.dk/3sr261g.html) ->  
[https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-broer/europaplads/?utm_source=qr&utm_campaign=byens-broer](https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-broer/europaplads/?utm_source=qr&utm_campaign=byens-broer)
* [https://purl.aarhusstadsarkiv.dk/4yu37i1.html](https://purl.aarhusstadsarkiv.dk/4yu37i1.html) ->  
[https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-broer/fiskerbroen/?utm_source=qr&utm_campaign=byens-broer](https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-broer/fiskerbroen/?utm_source=qr&utm_campaign=byens-broer)
* [https://purl.aarhusstadsarkiv.dk/5ubkc.html](https://purl.aarhusstadsarkiv.dk/5ubkc.html) ->  
[https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-lystbaadehavn/kapsejlads/?utm_source=qr&utm_campaign=byens-lystbaadehavn](https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-lystbaadehavn/kapsejlads/?utm_source=qr&utm_campaign=byens-lystbaadehavn)
* [https://purl.aarhusstadsarkiv.dk/7guvr.html](https://purl.aarhusstadsarkiv.dk/7guvr.html) ->  
[https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-lystbaadehavn/lystsejlads/?utm_source=qr&utm_campaign=byens-lystbaadehavn](https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-lystbaadehavn/lystsejlads/?utm_source=qr&utm_campaign=byens-lystbaadehavn)
* [https://purl.aarhusstadsarkiv.dk/cewq8sx.html](https://purl.aarhusstadsarkiv.dk/cewq8sx.html) ->  
[https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-broer/christians-bro/?utm_source=qr&utm_campaign=byens-broer](https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-broer/christians-bro/?utm_source=qr&utm_campaign=byens-broer)
* [https://purl.aarhusstadsarkiv.dk/ekc1j.html](https://purl.aarhusstadsarkiv.dk/ekc1j.html) ->  
[https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-lystbaadehavn/kranen/?utm_source=qr&utm_campaign=byens-lystbaadehavn](https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-lystbaadehavn/kranen/?utm_source=qr&utm_campaign=byens-lystbaadehavn)
* [https://purl.aarhusstadsarkiv.dk/gmp57.html](https://purl.aarhusstadsarkiv.dk/gmp57.html) ->  
[https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-lystbaadehavn/vestre-daekmole/?utm_source=qr&utm_campaign=byens-lystbaadehavn](https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-lystbaadehavn/vestre-daekmole/?utm_source=qr&utm_campaign=byens-lystbaadehavn)
* [https://purl.aarhusstadsarkiv.dk/hwp0g.html](https://purl.aarhusstadsarkiv.dk/hwp0g.html) ->  
[https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-lystbaadehavn/kystpromenaden/?utm_source=qr&utm_campaign=byens-lystbaadehavn](https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-lystbaadehavn/kystpromenaden/?utm_source=qr&utm_campaign=byens-lystbaadehavn)
* [https://purl.aarhusstadsarkiv.dk/j5y1gnt.html](https://purl.aarhusstadsarkiv.dk/j5y1gnt.html) ->  
[https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-broer/smedens-bro/?utm_source=qr&utm_campaign=byens-broer](https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-broer/smedens-bro/?utm_source=qr&utm_campaign=byens-broer)
* [https://purl.aarhusstadsarkiv.dk/j6k7faa2.html](https://purl.aarhusstadsarkiv.dk/j6k7faa2.html) ->  
[https://aarhuswiki.dk](https://aarhuswiki.dk)
* [https://purl.aarhusstadsarkiv.dk/k1o0rod.html](https://purl.aarhusstadsarkiv.dk/k1o0rod.html) ->  
[https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-broer/museumsbroen/?utm_source=qr&utm_campaign=byens-broer](https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-broer/museumsbroen/?utm_source=qr&utm_campaign=byens-broer)
* [https://purl.aarhusstadsarkiv.dk/kllgk.html](https://purl.aarhusstadsarkiv.dk/kllgk.html) ->  
[https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-lystbaadehavn/oestre-daekmole/?utm_source=qr&utm_campaign=byens-lystbaadehavn](https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-lystbaadehavn/oestre-daekmole/?utm_source=qr&utm_campaign=byens-lystbaadehavn)
* [https://purl.aarhusstadsarkiv.dk/lr6gy4f.html](https://purl.aarhusstadsarkiv.dk/lr6gy4f.html) ->  
[https://aarhuswiki.dk/wiki/%C3%85rhus_Markjorder](https://aarhuswiki.dk/wiki/%C3%85rhus_Markjorder)
* [https://purl.aarhusstadsarkiv.dk/m3p6y.html](https://purl.aarhusstadsarkiv.dk/m3p6y.html) ->  
[https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-lystbaadehavn/traeskibshavnen/?utm_source=qr&utm_campaign=byens-lystbaadehavn](https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-lystbaadehavn/traeskibshavnen/?utm_source=qr&utm_campaign=byens-lystbaadehavn)
* [https://purl.aarhusstadsarkiv.dk/ndvgn.html](https://purl.aarhusstadsarkiv.dk/ndvgn.html) ->  
[https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-lystbaadehavn/slaebestedet/?utm_source=qr&utm_campaign=byens-lystbaadehavn](https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-lystbaadehavn/slaebestedet/?utm_source=qr&utm_campaign=byens-lystbaadehavn)
* [https://purl.aarhusstadsarkiv.dk/nny7kws.html](https://purl.aarhusstadsarkiv.dk/nny7kws.html) ->  
[https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-broer/skt-clemens-bro/?utm_source=qr&utm_campaign=byens-broer](https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-broer/skt-clemens-bro/?utm_source=qr&utm_campaign=byens-broer)
* [https://purl.aarhusstadsarkiv.dk/ogfxsqy.html](https://purl.aarhusstadsarkiv.dk/ogfxsqy.html) ->  
[https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-broer/frederiksbroen/?utm_source=qr&utm_campaign=byens-broer](https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-broer/frederiksbroen/?utm_source=qr&utm_campaign=byens-broer)
* [https://purl.aarhusstadsarkiv.dk/olom8.html](https://purl.aarhusstadsarkiv.dk/olom8.html) ->  
[https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-lystbaadehavn/auktionskajen/?utm_source=qr&utm_campaign=byens-lystbaadehavn](https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-lystbaadehavn/auktionskajen/?utm_source=qr&utm_campaign=byens-lystbaadehavn)
* [https://purl.aarhusstadsarkiv.dk/q31utzb.html](https://purl.aarhusstadsarkiv.dk/q31utzb.html) ->  
[https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-broer/vester-alle/?utm_source=qr&utm_campaign=byens-broer](https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-broer/vester-alle/?utm_source=qr&utm_campaign=byens-broer)
* [https://purl.aarhusstadsarkiv.dk/r8sfx.html](https://purl.aarhusstadsarkiv.dk/r8sfx.html) ->  
[https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-lystbaadehavn/aarhus-roklub/?utm_source=qr&utm_campaign=byens-lystbaadehavn](https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-lystbaadehavn/aarhus-roklub/?utm_source=qr&utm_campaign=byens-lystbaadehavn)
* [https://purl.aarhusstadsarkiv.dk/ryuq7cj.html](https://purl.aarhusstadsarkiv.dk/ryuq7cj.html) ->  
[https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-broer/mindebroen/?utm_source=qr&utm_campaign=byens-broer](https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-broer/mindebroen/?utm_source=qr&utm_campaign=byens-broer)
* [https://purl.aarhusstadsarkiv.dk/uw058ty.html](https://purl.aarhusstadsarkiv.dk/uw058ty.html) ->  
[https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-broer/letbanebroen/?utm_source=qr&utm_campaign=byens-broer](https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-broer/letbanebroen/?utm_source=qr&utm_campaign=byens-broer)
* [https://purl.aarhusstadsarkiv.dk/w1q0y.html](https://purl.aarhusstadsarkiv.dk/w1q0y.html) ->  
[https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-lystbaadehavn/soesporten/?utm_source=qr&utm_campaign=byens-lystbaadehavn](https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-lystbaadehavn/soesporten/?utm_source=qr&utm_campaign=byens-lystbaadehavn)
* [https://purl.aarhusstadsarkiv.dk/z4eq3.html](https://purl.aarhusstadsarkiv.dk/z4eq3.html) ->  
[https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-lystbaadehavn/beddinghuset/?utm_source=qr&utm_campaign=byens-lystbaadehavn](https://stadsarkiv.aarhus.dk/byhistorie/digitale-byvandringer-og-byrumsformidling/byens-lystbaadehavn/beddinghuset/?utm_source=qr&utm_campaign=byens-lystbaadehavn)
* [https://purl.aarhusstadsarkiv.dk/z3ixlvx.html](https://purl.aarhusstadsarkiv.dk/z3ixlvx.html) ->  
[https://stadsarkiv.aarhus.dk](https://stadsarkiv.aarhus.dk)
* [https://purl.aarhusstadsarkiv.dk/5w3dnom.html](https://purl.aarhusstadsarkiv.dk/5w3dnom.html) ->  
[https://stadsarkiv.aarhus.dk](https://stadsarkiv.aarhus.dk)
* [https://purl.aarhusstadsarkiv.dk/5yrrbys.html](https://purl.aarhusstadsarkiv.dk/5yrrbys.html) ->  
[https://stadsarkiv.aarhus.dk](https://stadsarkiv.aarhus.dk)
* [https://purl.aarhusstadsarkiv.dk/mcue6q0.html](https://purl.aarhusstadsarkiv.dk/mcue6q0.html) ->  
[https://stadsarkiv.aarhus.dk](https://stadsarkiv.aarhus.dk)
* [https://purl.aarhusstadsarkiv.dk/4qruxw9.html](https://purl.aarhusstadsarkiv.dk/4qruxw9.html) ->  
[https://stadsarkiv.aarhus.dk](https://stadsarkiv.aarhus.dk)
* [https://purl.aarhusstadsarkiv.dk/t6x7ngd.html](https://purl.aarhusstadsarkiv.dk/t6x7ngd.html) ->  
[https://stadsarkiv.aarhus.dk](https://stadsarkiv.aarhus.dk)
* [https://purl.aarhusstadsarkiv.dk/252v1mi.html](https://purl.aarhusstadsarkiv.dk/252v1mi.html) ->  
[https://stadsarkiv.aarhus.dk](https://stadsarkiv.aarhus.dk)
* [https://purl.aarhusstadsarkiv.dk/9ujz61y.html](https://purl.aarhusstadsarkiv.dk/9ujz61y.html) ->  
[https://stadsarkiv.aarhus.dk](https://stadsarkiv.aarhus.dk)
* [https://purl.aarhusstadsarkiv.dk/irh9brx.html](https://purl.aarhusstadsarkiv.dk/irh9brx.html) ->  
[https://stadsarkiv.aarhus.dk](https://stadsarkiv.aarhus.dk)
* [https://purl.aarhusstadsarkiv.dk/fv48yjx.html](https://purl.aarhusstadsarkiv.dk/fv48yjx.html) ->  
[https://stadsarkiv.aarhus.dk](https://stadsarkiv.aarhus.dk)
* [https://purl.aarhusstadsarkiv.dk/9fzu4g9.html](https://purl.aarhusstadsarkiv.dk/9fzu4g9.html) ->  
[https://stadsarkiv.aarhus.dk](https://stadsarkiv.aarhus.dk)
* [https://purl.aarhusstadsarkiv.dk/6socgb9.html](https://purl.aarhusstadsarkiv.dk/6socgb9.html) ->  
[https://stadsarkiv.aarhus.dk](https://stadsarkiv.aarhus.dk)
* [https://purl.aarhusstadsarkiv.dk/1btee1u.html](https://purl.aarhusstadsarkiv.dk/1btee1u.html) ->  
[https://stadsarkiv.aarhus.dk](https://stadsarkiv.aarhus.dk)
* [https://purl.aarhusstadsarkiv.dk/bdt3b6u.html](https://purl.aarhusstadsarkiv.dk/bdt3b6u.html) ->  
[https://stadsarkiv.aarhus.dk](https://stadsarkiv.aarhus.dk)
* [https://purl.aarhusstadsarkiv.dk/464ahit.html](https://purl.aarhusstadsarkiv.dk/464ahit.html) ->  
[https://stadsarkiv.aarhus.dk](https://stadsarkiv.aarhus.dk)
* [https://purl.aarhusstadsarkiv.dk/wsjfk1t.html](https://purl.aarhusstadsarkiv.dk/wsjfk1t.html) ->  
[https://stadsarkiv.aarhus.dk](https://stadsarkiv.aarhus.dk)
* [https://purl.aarhusstadsarkiv.dk/96nwhdu.html](https://purl.aarhusstadsarkiv.dk/96nwhdu.html) ->  
[https://stadsarkiv.aarhus.dk](https://stadsarkiv.aarhus.dk)
* [https://purl.aarhusstadsarkiv.dk/to70i97.html](https://purl.aarhusstadsarkiv.dk/to70i97.html) ->  
[https://stadsarkiv.aarhus.dk](https://stadsarkiv.aarhus.dk)
<!-- End PURLs -->

