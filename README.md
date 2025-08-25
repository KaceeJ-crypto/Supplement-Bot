# Supplemental-Bot

**Supplemental-Bot** is an automated content aggregator that curates the latest supplement news, deals, and product launches. It pulls content from RSS feeds, filters items by keywords (e.g., protein, creatine, pre-workout), adds your affiliate links, and publishes daily roundups to a static site via GitHub Pages.

---

##  Highlights

-  **Automated daily feed parsing & filtering** from trusted supplement websites.
-  **Affiliate integration** — supports Amazon, iHerb, MyProtein, Bodybuilding.com, and more.
-  **Auto-publishing** via GitHub Actions into a Jekyll static site (hosted on GitHub Pages).
-  **Email or Telegram alert support** (optional, via environment vars).
-  Lightweight Python dependencies, perfect for running on iSH or Linux environments.

---

##  Directory Overview

```text
Supplemental-Bot/              
├── bot.py                
├── requirements.txt      
├── sources.yaml          
├── data.json             
├── site/                 
│   ├── _config.yml       
│   ├── index.md          
│   └── _posts/           
│       └── .gitkeep      
└── .github/              
    └── workflows/        
        └── run.yml       

Getting Started

1. Clone the repository

git clone https://github.com/<your-username>/Supplemental-Bot.git
cd Supplemental-Bot
git checkout FanBoy69

2. Customize sources.yaml

Add your RSS feeds, keyword list, and affiliate entries:

domain_affiliates:
  amazon.com: "tag=YOUR_AMAZON_TAG"
  iherb.com: "affid=YOUR_IHERB_ID"

3. (Optional) Test locally in iSH

apk add python3 py3-pip
pip install -r requirements.txt
python bot.py

4. Commit changes and push

git commit -am "Update affiliate IDs"
git push

GitHub Actions will run nightly and publish your pages automatically to:

https://<your-username>.github.io/Supplemental-Bot/

Configuring GitHub Pages

On GitHub, go to Settings → Pages and configure:
	•	Branch: FanBoy69
	•	Folder: /site

After setup, your site will be live at:

https://<your-username>.github.io/Supplemental-Bot/

Telegram Alerts (Optional)

Set these secrets in your repository:
	•	TELEGRAM_BOT_TOKEN
	•	TELEGRAM_CHAT_ID

This enables the bot to also post daily roundups to your Telegram channel.

FAQ

Q: How does the bot know what to post?
It relies on sources.yaml for feed URLs and keywords—keep them updated to control content.

Q: Do I need to run the script manually?
Nope. GitHub Actions handles it automatically every day as configured in .github/workflows/run.yml.

Q: How can I add another affiliate?
Simply add it to the domain_affiliates section in sources.yaml.

License & Contributions

Feel free to use and modify this project! Pull Let me know if you’d like help 