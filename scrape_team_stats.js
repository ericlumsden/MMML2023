
async function find_team_stats(url) {
    const browser2 = await puppeteer.launch();
    const page2 = await browser2.newPage();
    page2.setDefaultNavigationTimeout(0);
    await page2.goto(url, {waitUntil: 'networkidle0',});
    let [stats_labels] = await page2.$x('/html/body/div[2]/div[6]/div[5]/div[4]/div[1]/table/thead/tr');
    let [team_stats] = await page2.$x('/html/body/div[2]/div[6]/div[5]/div[4]/div[1]/table/tbody/tr[1]');
    let [opp_stats] = await page2.$x('/html/body/div[2]/div[6]/div[5]/div[4]/div[1]/table/tbody/tr[3]');
}