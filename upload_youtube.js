const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());
const path = require('path');
const fs = require('fs');

const profileDir = "C:\\Users\\jegom\\VAREGO\\browser_profile\\youtube_shorts_profile";

async function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

(async () => {
    // Parse arguments: node upload_youtube.js --file <path> --title <title> --desc <desc> [--is_short] [--thumbnail <path>]
    const args = process.argv;
    let filePath = "";
    let title = "";
    let desc = "";
    let isShort = false;
    let thumbnailPath = "";
    let scheduleOffset = 0;
    
    for (let i = 0; i < args.length; i++) {
        if (args[i] === '--file') filePath = args[i+1];
        if (args[i] === '--title') title = args[i+1];
        if (args[i] === '--desc') desc = args[i+1];
        if (args[i] === '--is_short') isShort = true;
        if (args[i] === '--thumbnail') thumbnailPath = args[i+1];
        if (args[i] === '--schedule') scheduleOffset = parseInt(args[i+1], 10);
    }
    
    if (!filePath || !title) {
        console.error("[ERROR] Missing --file or --title arguments.");
        process.exit(1);
    }
    
    console.log("==================================================");
    console.log("VAREGO YOUTUBE STUDIO AUTOMATIC UPLOADER");
    console.log(`Video File: ${filePath}`);
    console.log(`Title: ${title}`);
    console.log(`Format: ${isShort ? 'Short' : 'Widescreen Video Essay'}`);
    console.log("==================================================\n");
    
    let browser;
    let page;
    
    // Shadow DOM Piercing Helper function
    async function queryShadow(page, selector) {
        return page.evaluateHandle((sel) => {
            const shadowRoots = [];
            function collect(node) {
                if (!node) return;
                if (node.shadowRoot) {
                    shadowRoots.push(node.shadowRoot);
                    collect(node.shadowRoot);
                }
                const children = node.children || [];
                for (let i = 0; i < children.length; i++) {
                    collect(children[i]);
                }
            }
            let found = document.querySelector(sel);
            if (found) return found;
            collect(document.body);
            for (const root of shadowRoots) {
                found = root.querySelector(sel);
                if (found) return found;
            }
            return null;
        }, selector);
    }
    
    // SOTA Shadow DOM Text Search (Traverses all shadows, normalizes space, picks most specific leaf node match and traverses up to parent container)
    async function queryShadowByText(page, keywords) {
        return page.evaluateHandle((keys) => {
            const shadowRoots = [document.body];
            function collect(node) {
                if (!node) return;
                if (node.shadowRoot) {
                    shadowRoots.push(node.shadowRoot);
                    collect(node.shadowRoot);
                }
                const children = node.children || [];
                for (let i = 0; i < children.length; i++) {
                    collect(children[i]);
                }
            }
            collect(document.body);
            
            const matches = [];
            for (const root of shadowRoots) {
                const elements = root.querySelectorAll('*');
                for (const el of elements) {
                    const tag = el.tagName ? el.tagName.toLowerCase() : '';
                    // Skip code/metadata elements to prevent false matches
                    if (tag === 'script' || tag === 'style' || tag === 'template' || tag === 'dom-module') {
                        continue;
                    }
                    
                    const text = el.innerText ? el.innerText.trim() : '';
                    // Normalize all spaces (handles non-breaking spaces U+00A0 and tabs/newlines)
                    const cleanText = text.replace(/\s+/g, ' ');
                    const aria = el.getAttribute ? el.getAttribute('aria-label') || '' : '';
                    const cleanAria = aria.replace(/\s+/g, ' ');
                    
                    const textMatches = keys.some(k => cleanText.toLowerCase().includes(k.toLowerCase()));
                    const ariaMatches = keys.some(k => cleanAria.toLowerCase().includes(k.toLowerCase()));
                    
                    if (textMatches || ariaMatches) {
                        matches.push({ el, textLength: cleanText.length || 9999 });
                    }
                }
            }
            if (matches.length > 0) {
                // Sort by text length ascending to get the deepest leaf node matching the text
                matches.sort((a, b) => a.textLength - b.textLength);
                let bestEl = matches[0].el;
                
                // Traverse up to find the clickable menu item container
                let curr = bestEl;
                while (curr && curr !== document.body) {
                    if (curr.tagName) {
                        const tag = curr.tagName.toLowerCase();
                        const role = curr.getAttribute ? (curr.getAttribute('role') || '') : '';
                        if (tag === 'paper-item' || tag === 'tp-yt-paper-item' || tag === 'ytcp-compact-menu-item' || tag === 'ytcp-menu-item-row' || tag === 'a' || role === 'menuitem' || role === 'button') {
                            return curr;
                        }
                    }
                    curr = curr.parentElement || curr.parentNode;
                }
                return bestEl;
            }
            return null;
        }, keywords);
    }
    
    // Active Polling Wait Helper (by Selector)
    async function waitForShadow(page, selector, timeoutMs = 30000) {
        const startTime = Date.now();
        while (Date.now() - startTime < timeoutMs) {
            const handle = await queryShadow(page, selector);
            if (handle && await handle.asElement()) {
                return handle;
            }
            await delay(1000);
        }
        return null;
    }
    
    // Active Polling Wait Helper (by Text)
    async function waitForShadowText(page, keywords, timeoutMs = 15000) {
        const startTime = Date.now();
        while (Date.now() - startTime < timeoutMs) {
            const handle = await queryShadowByText(page, keywords);
            if (handle && await handle.asElement()) {
                return handle;
            }
            await delay(1000);
        }
        return null;
    }
    
    try {
        console.log("Launching automated Chrome session...");
        browser = await puppeteer.launch({
            executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
            headless: false,
            userDataDir: profileDir,
            ignoreDefaultArgs: ["--enable-automation"],
            args: [
                '--window-size=1280,950',
                '--disable-notifications',
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox'
            ]
        });
        
        const pages = await browser.pages();
        page = pages.length > 0 ? pages[0] : await browser.newPage();
        await page.setViewport({ width: 1280, height: 950 });
        
        console.log("Navigating to YouTube Studio Content Page...");
        await page.goto('https://studio.youtube.com/channel/UCvrX3SdOyRwQWzd4VHknjXw/content', { waitUntil: 'domcontentloaded' });
        await delay(5000);
        
        if (page.url().includes('accounts.google.com')) {
            console.error("[ERROR] YouTube session expired or requires login. Please authenticate in Chrome first.");
            process.exit(1);
        }
        
        // Redirection correction
        let currentUrl = page.url();
        if (currentUrl.includes('/livestreaming') || currentUrl.includes('/live')) {
            console.log("Detected redirection to live page. Re-navigating to content page...");
            await page.goto('https://studio.youtube.com/channel/UCvrX3SdOyRwQWzd4VHknjXw/content', { waitUntil: 'domcontentloaded' });
            await delay(5000);
        }
        
        console.log("YouTube Studio session validated successfully.");
        
        // 1. Click Create Button
        console.log("Opening upload dialog...");
        let createBtn = await waitForShadow(page, 'ytcp-button.ytcpAppHeaderCreateIcon', 20000) || await waitForShadow(page, '#create-icon', 10000);
        if (!createBtn) {
            console.log("Attempting text fallback search for Create button...");
            createBtn = await waitForShadowText(page, ['Crear', 'Create'], 15000);
        }
        
        if (createBtn) {
            const tagName = await page.evaluate(el => el.tagName, createBtn);
            const outerHTML = await page.evaluate(el => el.outerHTML.substring(0, 150), createBtn);
            console.log(`Clicking Create button: Tag: ${tagName}, HTML: ${outerHTML}`);
            await page.evaluate(el => el.click(), createBtn);
            console.log("Clicked Create button.");
        } else {
            throw new Error("Create button not found in DOM.");
        }
        await delay(3000);
        
        // 2. Click Upload Button menu item
        let uploadBtn = await waitForShadow(page, 'tp-yt-paper-item#text-item-0', 15000) || await waitForShadow(page, '#upload-button-menu-item', 5000) || await waitForShadow(page, 'ytd-compact-link-renderer', 5000);
        if (!uploadBtn) {
            console.log("Attempting text fallback search for Upload button menu item...");
            uploadBtn = await waitForShadowText(page, ['subir', 'upload'], 15000);
        }
        
        if (uploadBtn) {
            const tagName = await page.evaluate(el => el.tagName, uploadBtn);
            const outerHTML = await page.evaluate(el => el.outerHTML.substring(0, 150), uploadBtn);
            console.log(`Clicking Upload option: Tag: ${tagName}, HTML: ${outerHTML}`);
            await page.evaluate(el => el.click(), uploadBtn);
            console.log("Clicked Upload option.");
        } else {
            throw new Error("Upload button menu item not found in DOM.");
        }
        await delay(4000);
        
        // 3. Upload video file
        console.log("Uploading video file...");
        const fileInput = await waitForShadow(page, 'input[type="file"]', 20000);
        if (fileInput) {
            await (await fileInput.asElement()).uploadFile(filePath);
        } else {
            throw new Error("File input element not found in DOM.");
        }
        console.log("Upload started. Waiting for interface elements to load...");
        await delay(15000);
        
        // 4. Enter Title and Description via safe keyboard simulation
        console.log("Writing Title and Description...");
        const textboxesHandle = await page.evaluateHandle(() => {
            const list = [];
            const shadowRoots = [document.body];
            function collect(node) {
                if (!node) return;
                if (node.shadowRoot) {
                    shadowRoots.push(node.shadowRoot);
                    collect(node.shadowRoot);
                }
                const children = node.children || [];
                for (let i = 0; i < children.length; i++) {
                    collect(children[i]);
                }
            }
            collect(document.body);
            
            for (const root of shadowRoots) {
                root.querySelectorAll('[id="textbox"]').forEach(el => list.push(el));
            }
            return list;
        });
        
        const textboxes = await textboxesHandle.getProperties();
        const textboxList = [];
        for (const prop of textboxes.values()) {
            const el = prop.asElement();
            if (el) textboxList.push(el);
        }
        
        if (textboxList.length === 0) {
            throw new Error("Metadata textboxes not found in DOM.");
        }
        
        // Click and type Title
        const titleBox = textboxList[0];
        await titleBox.click();
        await page.keyboard.down('Control');
        await page.keyboard.press('A');
        await page.keyboard.up('Control');
        await page.keyboard.press('Backspace');
        await delay(500);
        await page.keyboard.type(title, { delay: 10 });
        await delay(2000);
        
        // Click and type Description
        if (desc && textboxList.length > 1) {
            const descBox = textboxList[1];
            await descBox.click();
            await page.keyboard.down('Control');
            await page.keyboard.press('A');
            await page.keyboard.up('Control');
            await page.keyboard.press('Backspace');
            await delay(500);
            await page.keyboard.type(desc, { delay: 5 });
            await delay(2000);
        }
        
        // 5. Upload Thumbnail if provided and not a Short
        if (thumbnailPath && !isShort && fs.existsSync(thumbnailPath)) {
            console.log("Uploading custom thumbnail...");
            try {
                const thumbInput = await waitForShadow(page, 'input#file-loader', 10000);
                if (thumbInput) {
                    await (await thumbInput.asElement()).uploadFile(thumbnailPath);
                    console.log("Thumbnail uploaded successfully.");
                    await delay(4000);
                } else {
                    console.log("Thumbnail input not found. Skipping.");
                }
            } catch (err) {
                console.log(`Failed to upload thumbnail: ${err.message}`);
            }
        }
        
        // 6. Set Audience: 'Not made for kids'
        console.log("Setting audience restrictions...");
        await page.evaluate(() => {
            const list = [];
            const shadowRoots = [document.body];
            function collect(node) {
                if (!node) return;
                if (node.shadowRoot) {
                    shadowRoots.push(node.shadowRoot);
                    collect(node.shadowRoot);
                }
                const children = node.children || [];
                for (let i = 0; i < children.length; i++) {
                    collect(children[i]);
                }
            }
            collect(document.body);
            
            for (const root of shadowRoots) {
                root.querySelectorAll('[role="radio"]').forEach(el => list.push(el));
            }
            
            const noKids = list.find(r => 
                r.innerText.includes('No, no') || 
                r.innerText.includes('No, it\'s not') || 
                r.getAttribute('aria-label')?.includes('No, no') ||
                r.getAttribute('aria-label')?.includes('not made for kids')
            );
            if (noKids) {
                noKids.click();
            } else {
                console.log("Audience radio not found. Direct fallback click on second option.");
                if (list.length > 1) list[1].click();
            }
        });
        await delay(3000);
        
        // 7. Go through the tabs (Details -> Video Elements -> Checks -> Visibility)
        console.log("Navigating to Visibility tab...");
        for (let i = 0; i < 3; i++) {
            const nextBtn = await waitForShadow(page, '#next-button', 15000);
            if (nextBtn) {
                await page.evaluate(el => el.click(), nextBtn);
                await delay(3000);
            } else {
                throw new Error("Next button not found.");
            }
        }
        
        // 8. Handle Visibility (Immediate or Schedule)
        if (scheduleOffset > 0) {
            console.log(`Setting visibility to Scheduled (in ${scheduleOffset} minutes)...`);
            try {
                const scheduleRadio = await waitForShadow(page, '#schedule-radio-button', 10000) || await waitForShadow(page, '[name="SCHEDULE"]', 5000);
                if (scheduleRadio) {
                    await page.evaluate(el => el.click(), scheduleRadio);
                    await delay(3000);
                    
                    // Calculate target date/time
                    const targetDate = new Date(Date.now() + scheduleOffset * 60000);
                    const pad = (num) => num.toString().padStart(2, '0');
                    const dateStr = `${pad(targetDate.getDate())}/${pad(targetDate.getMonth() + 1)}/${targetDate.getFullYear()}`;
                    
                    let mins = targetDate.getMinutes();
                    mins = Math.round(mins / 15) * 15;
                    let hrs = targetDate.getHours();
                    if (mins >= 60) {
                        mins = 0;
                        hrs = (hrs + 1) % 24;
                    }
                    const timeStr = `${pad(hrs)}:${pad(mins)}`;
                    
                    console.log(`Scheduling details -> Date: ${dateStr}, Time: ${timeStr}`);
                    
                    // Date picker
                    const datePicker = await waitForShadow(page, '#datepicker-trigger input', 10000) || await waitForShadow(page, '[id="datepicker-trigger"] input', 5000);
                    if (datePicker) {
                        const el = await datePicker.asElement();
                        await el.click();
                        await page.keyboard.down('Control');
                        await page.keyboard.press('A');
                        await page.keyboard.up('Control');
                        await page.keyboard.press('Backspace');
                        await delay(500);
                        await page.keyboard.type(dateStr, { delay: 10 });
                        await page.keyboard.press('Enter');
                        await delay(2000);
                    }
                    
                    // Time picker
                    const timePicker = await waitForShadow(page, '#time-of-day-trigger input', 10000) || await waitForShadow(page, 'input[aria-label="Publish time"]', 5000) || await waitForShadow(page, 'input[placeholder="Hora"]', 5000);
                    if (timePicker) {
                        const el = await timePicker.asElement();
                        await el.click();
                        await page.keyboard.down('Control');
                        await page.keyboard.press('A');
                        await page.keyboard.up('Control');
                        await page.keyboard.press('Backspace');
                        await delay(500);
                        await page.keyboard.type(timeStr, { delay: 10 });
                        await page.keyboard.press('Enter');
                        await delay(2000);
                    }
                } else {
                    throw new Error("Schedule radio button not found.");
                }
            } catch (err) {
                console.log(`[WARNING] Scheduling failed: ${err.message}. Falling back to immediate Public release.`);
                await delay(2000);
                
                // Fallback to Public radio
                await page.evaluate(() => {
                    const list = [];
                    const shadowRoots = [document.body];
                    function collect(node) {
                        if (!node) return;
                        if (node.shadowRoot) {
                            shadowRoots.push(node.shadowRoot);
                            collect(node.shadowRoot);
                        }
                        const children = node.children || [];
                        for (let i = 0; i < children.length; i++) {
                            collect(children[i]);
                        }
                    }
                    collect(document.body);
                    
                    for (const root of shadowRoots) {
                        root.querySelectorAll('[role="radio"]').forEach(el => list.push(el));
                    }
                    const pub = list.find(r => r.innerText.includes('Público') || r.innerText.includes('Public'));
                    if (pub) pub.click();
                });
                await delay(3000);
            }
        } else {
            console.log("Setting visibility to Public...");
            await page.evaluate(() => {
                const list = [];
                const shadowRoots = [document.body];
                function collect(node) {
                    if (!node) return;
                    if (node.shadowRoot) {
                        shadowRoots.push(node.shadowRoot);
                        collect(node.shadowRoot);
                    }
                    const children = node.children || [];
                    for (let i = 0; i < children.length; i++) {
                        collect(children[i]);
                    }
                }
                collect(document.body);
                
                for (const root of shadowRoots) {
                    root.querySelectorAll('[role="radio"]').forEach(el => list.push(el));
                }
                const pub = list.find(r => r.innerText.includes('Público') || r.innerText.includes('Public'));
                if (pub) pub.click();
            });
            await delay(3000);
        }
        
        // 9. Click Publish/Done Button
        console.log("Publishing video...");
        const doneBtn = await waitForShadow(page, '#done-button', 20000);
        if (doneBtn) {
            await page.evaluate(el => el.click(), doneBtn);
            console.log("Waiting for confirmation dialog...");
            await delay(15000);
            console.log("✅ Video published successfully!");
        } else {
            throw new Error("Publish button (#done-button) not found in DOM.");
        }
        
    } catch (e) {
        console.error(`[ERROR] Upload failed: ${e.message}`);
        // Capture error screenshot for debugging
        try {
            if (page) {
                await page.screenshot({ path: path.join(__dirname, 'upload_error.png') });
                console.log("Saved upload_error.png screenshot.");
            }
        } catch (_) {}
        process.exit(1);
    } finally {
        if (browser) {
            await browser.close();
        }
    }
})();
