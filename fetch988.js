import puppeteer from "puppeteer";
import fs from "fs";

(async () => {
  console.log("🚀 Launching Puppeteer...");
  const browser = await puppeteer.launch({ headless: true, args: ["--no-sandbox"] });
  const page = await browser.newPage();

  await page.goto("https://988.com.my/on-air/", { waitUntil: "networkidle2", timeout: 0 });
  await page.waitForTimeout(3000); // wait for page JS to load

  // extract all text nodes related to 已播歌曲
  const songs = await page.evaluate(() => {
    const sections = Array.from(document.querySelectorAll("div, li, p, span"));
    const texts = sections.map(el => el.innerText.trim()).filter(t => t);
    // try to find the section after 已播歌曲
    const idx = texts.findIndex(t => t.includes("已播歌曲"));
    if (idx === -1) return [];
    return texts.slice(idx + 1, idx + 11); // next 10 lines after “已播歌曲”
  });

  console.log("🎵 Extracted songs:", songs);

  const html = `<!DOCTYPE html>
  <html lang="zh-Hans">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1280, initial-scale=1.0">
    <title>Playlist 988 FM</title>
    <style>
      body { margin:0; background:#000; color:#ddd; font-family:"Microsoft YaHei",Arial,sans-serif; display:flex; justify-content:center; align-items:center; height:100vh; }
      .screen { width:1280px; height:520px; background:#111; border:4px solid #777; border-radius:16px; padding:20px; box-shadow:0 0 25px rgba(0,0,0,0.6); }
      .logo { width:150px; }
      h2 { text-align:right; margin-top:-40px; margin-right:40px; color:#ccc; }
      table { width:100%; border-collapse:collapse; margin-top:30px; }
      td { padding:10px; border-bottom:1px solid #444; }
      td.song { color:#eee; font-size:18px; }
    </style>
  </head>
  <body>
    <div class="screen">
      <img src="https://raw.githubusercontent.com/SGolden58/svg/main/Logo/988.png" class="logo" alt="988">
      <h2>已播歌曲</h2>
      <table>
        ${songs.length === 0 
          ? "<tr><td>未找到播放列表 / No songs found</td></tr>" 
          : songs.map(s => `<tr><td class="song">${s}</td></tr>`).join("")}
      </table>
    </div>
  </body>
  </html>`;

  fs.writeFileSync("988songslist.html", html, "utf8");
  console.log("✅ Saved 988songslist.html");

  await browser.close();
})();
