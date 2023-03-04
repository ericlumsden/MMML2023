const puppeteer = require('puppeteer-extra');
const { DEFAULT_INTERCEPT_RESOLUTION_PRIORITY } = require('puppeteer');
const AdblockerPlugin = require('puppeteer-extra-plugin-adblocker');
puppeteer.use(
    AdblockerPlugin({
        interceptResolutionPriority: DEFAULT_INTERCEPT_RESOLUTION_PRIORITY
    })
);

async function scrapeTeamStates(team_url) {
    // Make a function to collect the team stats and save into database
    // ONLY TEAMS THAT ARE IN THE TOURNAMENT, NOT ALL TEAM STATS FROM THAT SEASON
}

const example_year = 2007;
async function scrapeTourney(year) {
    const url = `https://www.sports-reference.com/cbb/postseason/men/${year}-ncaa.html`;
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    page.setDefaultNavigationTimeout(0);
    await page.goto(url);
    const [el] = await page.$x('/html/body/div[2]/div[6]/div[2]/div');
    const txt = await el.getProperty('textContent');
    const rawTxt = await txt.jsonValue();
    console.log({rawTxt});
    browser.close();

    // Next steps: Iterate through regions and FF, collect outcomes from each matchup and team stats (only on first iteration), save team stats to one database, game scores in another
}

scrapeTourney(example_year);