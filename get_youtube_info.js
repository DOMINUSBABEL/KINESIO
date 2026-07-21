const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());
const path = require('path');
const fs = require('fs');

const profileDir = "C:\\Users\\jegom\\VAREGO\\browser_profile\\youtube_shorts_profile";
const url = "https://www.youtube.com/watch?v=Va4IMljkMdY";

(async () => {
    let browser;
    try {
        browser = await puppeteer.launch({
            executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
            headless: true, // Headless is fine since the profile is pre-authenticated
            userDataDir: profileDir,
            args: ['--window-size=1280,900', '--no-sandbox']
        });
        
        const page = await browser.newPage();
        await page.setViewport({ width: 1280, height: 900 });
        
        console.log(`Navigating to: ${url}`);
        await page.goto(url, { waitUntil: 'networkidle2', timeout: 60000 });
        
        // Wait for title element or fallback
        await page.waitForSelector('h1.ytd-watch-metadata', { timeout: 15000 }).catch(() => {});
        
        const info = await page.evaluate(() => {
            const titleEl = document.querySelector('h1.ytd-watch-metadata') || document.querySelector('yt-formatted-string.ytd-video-primary-info-renderer');
            const title = titleEl ? titleEl.innerText : document.title;
            
            const descEl = document.querySelector('#description-inline-expander') || document.querySelector('#description');
            const desc = descEl ? descEl.innerText : "No description found.";
            
            const channelEl = document.querySelector('#owner-sub-count') || document.querySelector('#channel-name');
            const channel = channelEl ? channelEl.innerText : "Unknown Channel";
            
            return { title, channel, desc };
        });
        
        console.log("\n==================================================");
        console.log("SUCCESSFULLY RETRIEVED YOUTUBE VIDEO METADATA:");
        console.log("==================================================");
        console.log(`Title: ${info.title}`);
        console.log(`Channel: ${info.channel}`);
        console.log(`Description:\n${info.desc.substring(0, 1000)}...`);
        console.log("==================================================\n");
        
        // Save to temporary file
        fs.writeFileSync(path.join(__dirname, 'reference_video_info.json'), JSON.stringify(info, null, 2), 'utf-8');
        
    } catch (e) {
        console.error(`[ERROR] Failed to fetch video info: ${e.message}`);
    } finally {
        if (browser) await browser.close();
    }
})();
