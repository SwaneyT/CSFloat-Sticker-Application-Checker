This tool is written in Python and uses undetected Chromedriver to automatically check for sticker application data on CSFloat, previously known as CSGOFloat. It is impossible to run the selenium session headless, as it results in Cloudflare turnstile errors.

The tool requires logging in via cmd, and currently only supports Steam mobile app login confirmation (2FA code log-in would work, but hasn't been implemented).

The python file takes a JSON input (through a .bat file or cmd line argument), and requires sticker names and sticker IDs (any sticker name can be provided), in the format of `name:sticker_id`. The tool will automatically search through all 5x sticker crafts, 4x sticker crafts, 3x sticker crafts, 2x sticker crafts, and 1x sticker crafts, and then output a total number of applications to cmd and a file named the datetime of starting the tool.

Due to CSFloat limitations, stickers with around >35k applications will give vastly incorrect results, and so, a generic weighting was also created for the tool, which will ensure every search attempt is under 35k applications, guaranteeing accurate results.

Any questions? Please contact my Discord: **shockkkk**
