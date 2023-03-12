const puppeteer = require('puppeteer-extra');
const { DEFAULT_INTERCEPT_RESOLUTION_PRIORITY } = require('puppeteer');
const AdblockerPlugin = require('puppeteer-extra-plugin-adblocker');
puppeteer.use(
    AdblockerPlugin({
        interceptResolutionPriority: DEFAULT_INTERCEPT_RESOLUTION_PRIORITY
    })
);

// Set up database to which data will be saved
const sqlite3 = require("sqlite3").verbose();
const db = new sqlite3.Database("./ncaa.db", sqlite3.OPEN_READWRITE, (err) => {
    if (err) return console.error(err.message);
    console.log("db connection successful");
});

// First establish the find_team_stats function; take in a team's season page url and scrape their season stats
let ex_url = "https://www.sports-reference.com/cbb/schools/boston-college/men/1989.html";
async function find_team_stats(url) {
    const browser2 = await puppeteer.launch();
    const page2 = await browser2.newPage();
    page2.setDefaultNavigationTimeout(0);
    await page2.goto(url, {waitUntil: 'networkidle0',});
    //html/body/div[2]/div[5]/div[4]/div[4]/div[1]/table/tbody/tr[1]/td[4]
    //let [stats_labels] = await page2.$x('/html/body/div[2]/div[6]/div[5]/div[4]/div[1]/table/thead/tr');
    let [team_stats] = await page2.$x('/html/body/div[2]/div[6]/div[5]/div[4]/div[1]/table/tbody/tr[1]');
    let team_stats_text = team_stats.innerText();
    console.log(team_stats_text);
    //let [opp_stats] = await page2.$x('/html/body/div[2]/div[6]/div[5]/div[4]/div[1]/table/tbody/tr[3]');
}

find_team_stats(ex_url);
// The first thing is to establish a connection to the ncaa.db database and upload the men's or women's tourney table
/*async function selectRows(table) {
    let teamIDs = new Set([]);
    db.each(`SELECT * FROM ${table}`, (error, row) => {
        if (error) {
            console.error(error.message);
        }
        //console.log(row['team_1ID']);
        for (let team_num = 1; team_num <= 2; team_num++) {
            let team_id = row[`team_${team_num}ID`]
            if teamIDs.has(`${table}_${team_id}`) {
                continue;
            } else {
                teamIDs.add(`${table}_${team_id}`)
                await find_team_stats(row[`url_${team_num}`]);
            }
        }
    });
}
*/

//selectRows("menstourney")

find_team_stats(ex_url);