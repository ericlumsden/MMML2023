const puppeteer = require('puppeteer-extra');
const { DEFAULT_INTERCEPT_RESOLUTION_PRIORITY } = require('puppeteer');
const AdblockerPlugin = require('puppeteer-extra-plugin-adblocker');
puppeteer.use(
    AdblockerPlugin({
        interceptResolutionPriority: DEFAULT_INTERCEPT_RESOLUTION_PRIORITY
    })
);

/*
/html/body/div[2]/div[6]/div[3]/div[1]/div/div[1]/div[1]/div[1]/a[1]
/html/body/div[2]/div[6]/div[3]/div[1]/div/div[1]/div[1]/div[1]/a[2]
/html/body/div[2]/div[6]/div[3]/div[4]/div/div[1]/div[4]/div[1]/a[1]
/html/body/div[2]/div[6]/div[3]/div[4]/div/div[1]/div[5]/div[1]/a[1]
/html/body/div[2]/div[6]/div[3]/div[1]/div/div[1]/div[1]/div[2]/a[1]
/html/body/div[2]/div[6]/div[3]/div[1]/div/div[2]/div[1]/div[1]/a[1]
/html/body/div[2]/div[6]/div[3]/div[1]/div/div[1]/div[1]/div[2]/a[1]
html/body/div[2]/div[6]/div[3]/div[2]/div/div[1]/div[1]/div[1]/a[1]/
*/

async function scrapeTeamStates(team_url) {
    // Make a function to collect the team stats and save into database
    // ONLY TEAMS THAT ARE IN THE TOURNAMENT, NOT ALL TEAM STATS FROM THAT SEASON
}

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

const example_year = 2007;
async function scrapeTourney(year) {
    const url = `https://www.sports-reference.com/cbb/postseason/men/${year}-ncaa.html`;
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    page.setDefaultNavigationTimeout(0);
    await page.goto(url);

    /*
    We need to iterate over the following:
    i. Bracket division (e.g. East, Midwest, Southeast, West, FF)
    ii. Round in that division
    iii. Games in that round
    iv. Teams in that game
    Indexing will start at one to coincide with div elements on the page
    */
    for (let bracket=1; bracket<=num_brackets; bracket++) {
        let num_rounds;
        if (bracket < num_brackets) {
            num_rounds = 4;
        } else {
            num_rounds = 2;
        }

        for (let round=1; round<=num_rounds; round++) {

            let num_games = find_num_games(bracket, round);
            for (let game=1; game<=num_games; game++) {
                for (let team=1; team<=2; team++) {
                    const [team_name] = await page.$x(`/html/body/div[2]/div[6]/div[3]/div[${bracket}]/div/div[${round}]/div[${game}]/div[${team}]/a[1]`);
                    const [team_score] = await page.$x(`/html/body/div[2]/div[6]/div[3]/div[${bracket}]/div/div[${round}]/div[${game}]/div[${team}]/a[2]`);
                    const temp_txt = await (await team_name.getProperty('textContent')).jsonValue();
                    const temp_link = await (await team_name.getProperty('href')).jsonValue();
                    const temp_score = await (await team_score.getProperty('textContent')).jsonValue();
                    console.log({temp_txt, temp_score, temp_link});
                }
            }
        }
    }
    browser.close();

    // Next steps: Iterate through regions and FF, collect outcomes from each matchup and team stats (only on first iteration), save team stats to one database, game scores in another
}

// Want to collect data from 1985 to 2019 (tournament cancelled in 2020 due to COVID-19) 
let tourney_years = Array.from(Array(2020-1985).keys(), n => n + 1985);
let missing_years = [2021, 2022];
tourney_years = tourney_years.concat(missing_years);

/*
for (let year=0; year < tourney_years.length; year++) {
    scrapeTourney(year);
}*/