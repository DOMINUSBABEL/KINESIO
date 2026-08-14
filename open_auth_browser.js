const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());
const path = require('path');

const profileDir = "C:\\Users\\jegom\\VAREGO\\browser_profile\\youtube_shorts_profile";
const targetUrl = "https://studio.youtube.com/";

(async () => {
    console.log("==================================================");
    console.log("VAREGO - YouTube Authentication Session Window");
    console.log("==================================================");
    console.log(`Profile: ${profileDir}`);
    console.log(`Target: ${targetUrl}`);
    console.log("\nLaunching Chrome window...");
    
    try {
        const browser = await puppeteer.launch({
            executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
            headless: false,
            userDataDir: profileDir,
            ignoreDefaultArgs: ["--enable-automation"],
            args: [
                '--window-size=1280,900',
                '--disable-notifications',
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox'
            ]
        });
        
        const pages = await browser.pages();
        const page = pages.length > 0 ? pages[0] : await browser.newPage();
        await page.setViewport({ width: 1280, height: 900 });
        
        console.log("Opening YouTube Studio...");
        await page.goto(targetUrl, { waitUntil: 'domcontentloaded' });
        
        console.log("\n--------------------------------------------------");
        console.log("✅ BROWSER WINDOW IS NOW OPEN.");
        console.log("Please perform the login/verification inside Chrome.");
        console.log("Once done, simply close the Chrome browser window.");
        console.log("--------------------------------------------------");
        
        // Wait until the user closes the browser window
        await new Promise(resolve => browser.on('disconnected', resolve));
        console.log("\n[INFO] Browser window closed. Session saved successfully.");
        
    } catch (err) {
        console.error(`[ERROR] Failed to run auth browser: ${err.message}`);
    }
})();
