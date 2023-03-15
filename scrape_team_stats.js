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
let ex_url = "https://www.sports-reference.com/cbb/schools/boston-college/men/1990.html";
async function find_team_stats(team_id, url) {
    db.run(
        `CREATE TABLE IF NOT EXISTS mensteamstats (team_id, games, FG, FGA, FGper, twoP, twoPA, twoPper, thrP, thrPA, thrPper, FT, FTA, FTper, TRB, AST, STL, BLK, TOV, PF, PTS, oppFG, oppFGA, oppFGper, opp2P, opp2PA, opp2Pper, opp3P, opp3PA, opp3Pper, oppFT, oppFTA, oppFTper, oppTRB, oppAST, oppSTL, oppBLK, oppTOV, oppPF, oppPTS, url)`
    );
    const stats = `INSERT INTO mensteamstats (team_id, games, FG, FGA, FGper, twoP, twoPA, twoPper, thrP, thrPA, thrPper, FT, FTA, FTper, TRB, AST, STL, BLK, TOV, PF, PTS, oppFG, oppFGA, oppFGper, opp2P, opp2PA, opp2Pper, opp3P, opp3pA, opp3Pper, oppFT, oppFTA, oppFTper, oppTRB, oppAST, oppSTL, oppBLK, oppTOV, oppPF, oppPTS, url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`;

    console.log(`Scraping from ${url}`);
    const browser2 = await puppeteer.launch();
    const page2 = await browser2.newPage();
    page2.setDefaultNavigationTimeout(0);
    await page2.goto(url, {waitUntil: 'networkidle0',});
    //html/body/div[2]/div[5]/div[4]/div[4]/div[1]/table/tbody/tr[1]/td[4]
    //let [stats_labels] = await page2.$x('/html/body/div[2]/div[6]/div[5]/div[4]/div[1]/table/thead/tr');
    //let [team_stats] = await page2.$x('/html/body/div[2]/div[6]/div[5]/div[4]/div[1]/table/tbody/tr[1]');
    //let team_stats_text = team_stats.innerText();

    const result = await page2.$$eval('#season-total_per_game tr', rows => {
        return Array.from(rows, row => {
            const columns = row.querySelectorAll('td');
            return Array.from(columns, column => column.innerText);
        });
    });

    await db.run(stats, [team_id, result[1][0], result[1][2], result[1][3], result[1][4], result[1][5], result[1][6], result[1][7], result[1][8], result[1][9], result[1][10], result[1][11], result[1][12], result[1][13], result[1][16], result[1][17], result[1][18], result[1][19], result[1][20], result[1][21], result[1][22], result[2][2], result[2][3], result[2][4], result[2][5], result[2][6], result[2][7], result[2][8], result[2][9], result[2][10], result[2][11], result[2][12], result[2][13], result[2][16], result[2][17], result[2][18], result[2][19], result[2][20], result[2][21], result[2][22], url])
    
    await browser2.close(console.log('browser closed'));
}

// The first thing is to establish a connection to the ncaa.db database and upload the men's or women's tourney table
select_ids = () => {
    let teamIDs = new Set([]);
    db.each('SELECT * FROM menstourney', (error, row) => {
        if (error) {
            console.error(error.message);
        }
        for (let team_num = 1; team_num <= 2; team_num++) {
            teamIDs.add([row[`team_${team_num}ID`], row[`url_${team_num}`]]);
            console.log(`current set: ${teamIDs}`);
        }
    });
    return teamIDs;
}


//find_team_stats('1990BostonCollege', ex_url);
teamIDs = select_ids();
console.log(teamIDs);