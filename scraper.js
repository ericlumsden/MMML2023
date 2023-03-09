const puppeteer = require('puppeteer-extra');
const { DEFAULT_INTERCEPT_RESOLUTION_PRIORITY } = require('puppeteer');
const AdblockerPlugin = require('puppeteer-extra-plugin-adblocker');
puppeteer.use(
    AdblockerPlugin({
        interceptResolutionPriority: DEFAULT_INTERCEPT_RESOLUTION_PRIORITY
    })
);
// Set up database to which data will be saved
const sqlite3 = requre("sqlite3").verbose();
const db = new.sqlite3.Database("./ncaa.db", sqlite3.OPEN_READWRITE, (err) => {
    if (err) return console.error(err.message);
    console.log("db connection successful");
});

// Function for finding the number of games in the currently investigated round
// Based on both the current bracket and round
const num_brackets = 5;
function find_num_games(bracket, round) {
    if (bracket < num_brackets) {
        return (8 / (2**(round-1)));
    } else {
        return  (2 / (2**(round-1)));
    }
}

const example_year = 2022;
async function scrapeTourney(year) {
    // First, establish new table for this tournament and make a sql_tourney to insert values once looked up
    db.run(
        `CREATE TABLE tourney${year}(year, bracket, round, game, team_1, score_1, url_1, team_2, score_2, url_2)`
    );
    const sql_tourney = `INSERT INTO tourney${year} (year, bracket, round, game, team1, url1, score1, team2, url2, score2) VALUES(?,?,?,?,?,?,?,?,?,?)`;

    const url = `https://www.sports-reference.com/cbb/postseason/men/${year}-ncaa.html`;
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    page.setDefaultNavigationTimeout(0);
    await page.goto(url, {waitUntil: 'networkidle0',});

    for (let bracket = 1; bracket <= num_brackets; bracket++) {
        // Number of rounds depends on which bracket we're in...
        let num_rounds;
        if (bracket === num_brackets) {
            num_rounds = 2;
        } else {
            num_rounds = 4;
        }

        for (let round = 1; round <= num_rounds; round++) {
            // Number of games in the round is dependent on both bracket and round
            // See above function for how we calculate number of games in the round
            let num_games = find_num_games(bracket, round);

            for (let game = 1; game <= num_games; game++) {
                let team1, score1, url1, team2, score2, url2;

                for (let team = 1; team <= 2; team++) {

                    const [team_name] = await page.$x(`/html/body/div[2]/div[5]/div[3]/div[${bracket}]/div/div[${round}]/div[${game}]/div[${team}]/a[1]`);
                    const name_txt = await team_name.getProperty('textContent');
                    const name_url = await team_name.getProperty('href');

                    // Also need score for the team in the round
                    const [team_score] = await page.$x(`/html/body/div[2]/div[5]/div[3]/div[${bracket}]/div/div[${round}]/div[${game}]/div[${team}]/a[2]`);
                    const score_txt = await team_score.getProperty('textContent');

                    if (team === 1) {
                        team1 = await name_txt.jsonValue();
                        url1 = await name_url.jsonValue();
                        score1 = await score_txt.jsonValue();
                    } else {
                        team2 = await name_txt.jsonValue();
                        url2 = await name_url.jsonValue();
                        score2 = await score_txt.jsonValue();
                    }

                    console.log({team1, url1, score1, team2, url2, score2});
                }
                
                db.run(sql_tourney, [year, bracket, round, game, team1, score1, url1, team2, score2, url2]);

            }
        }
    }
    browser.close();
}

scrapeTourney(example_year);

// Finally, close database
db.close((err) => {
    if (err) return console.error(err.message);
});