const cheerio = require("cheerio");
const axios = require("axios");
const fs = require('fs');
const readline = require('readline');
var output = "output" + Date.now() + ".txt";

async function performReadByLine() {
    const dosya = fs.createReadStream('input.txt');

    const oku = readline.createInterface({
        input: dosya,
        crlfDelay: Infinity
    });

    for await(const satir of oku) {
        performScraping(satir);
    }
}
 
async function performScraping(url) {

    const axiosResponse = await axios.request({
        method: "GET",
        url: url,
        headers: {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        }
    });

    const $ = cheerio.load(axiosResponse.data);

    var fframe = $("iframe").attr("src");
	
	var titleA = $("title").text();
	var titleB = titleA.split(". Bölüm");
	var title = (titleB[0]).slice(0,-2).trim();
	
    var bolumadi = $("h1.fw-light").text();
    var bolumnoA = (url).split("/");
    var bolumno = bolumnoA[6];

    if (fframe != "" && fframe != undefined)

        var url2 = fframe;

        const axiosResponse2 = await axios.request({
            method: "GET",
            url: url2,
            headers: {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
            }
        });
 

        var video = $("#video_html5_wrapper_html5_api").attr("src");

        let text = JSON.stringify(axiosResponse2.data);
        let baslangic = text.search("/v/");

        let result = text.substring(baslangic);
        son = result.split(".mp4");
        idd = (son[0]).split("/");

        if (son[0] != "" && idd[3] != "" && son[0] != undefined && idd[3] != undefined) {
            var url3 = "https://video.sibnet.ru" + son[0] + ".mp4";
            const axiosResponse3 = await axios.request({
                method: "GET",
                url: url3,
                maxRedirects: 0,
                headers: {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
                    "Accept-Encoding": "identity;q=1, *;q=0",
                    "Connection": "keep-alive",
                    "Accept": "*/*",
                    "Referer": "https://video.sibnet.ru/shell.php?videoid=" + idd[3],
                    "Host": "video.sibnet.ru",
                    "Content-Type": "application/json",
                    "Range": "bytes=0-"
                }
            }).then(response => {})
                .catch(error => {
                    // console.log("Çıktı:>>> https:" + error.response.headers.location + ";" + title + "-" + bolumadi.replace("/", "_"));

                    fs.appendFile(output, "https:" + error.response.headers.location + ";" + title + "-" + bolumadi.replace("/", "_"), function (err) {
                        // if (err) throw err;
                    });
                });
                console.log("Tamamlandı");
        }

    }

performReadByLine();
