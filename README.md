# CSFloat-Sticker-Application-Checker
This tool is written in Python and uses headless Firefox Selenium to automatically check for sticker application data on CSFloat, previously known as CSGOFloat. It requires logging in via cmd, and currently only supports Steam mobile app login confirmation (made for my own personal use), however code log-in would absolutely work, just haven't implemented it.

The software can be ran with headless OFF, with the browser visible, by commenting out the "options.add_argument("-headless")" line.

The tool takes an input of sticker names (optional) and IDs (mandatory) and scans through CSFloat collecting their application data. Depending on how many stickers you want to check, there may be a 30 minute cooldown enforced by CSFloat.

Recaptcha errors are unavoidable, however, from my own testing they never last long and will always clear up. Recaptcha errors appear to be IP based.

The output is written to a .txt file named the date and time of completion.
