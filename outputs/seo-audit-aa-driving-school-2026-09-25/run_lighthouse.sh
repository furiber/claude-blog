#!/usr/bin/env bash
# Mobile Lighthouse (default mobile emulation: Moto G Power, slow 4G, 4x CPU) on all 7 URLs.
export CHROME_PATH=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
for u in driving-school-hub:"" driving-lessons:driving-lessons/ defensive-driving-course:defensive-driving-course/ road-code-practice-test:road-code-practice-test/ get-ready-for-learner-test:get-ready-for-learner-test/ get-ready-for-restricted-test:get-ready-for-restricted-test/ get-ready-for-full-test:get-ready-for-full-test/; do
  s=${u%%:*}; p=${u#*:}
  npx -y lighthouse@12 "https://www.aa.co.nz/drivers/driving-school/$p" --form-factor=mobile \
    --only-categories=performance,accessibility,best-practices,seo --output=json \
    --output-path=lighthouse/$s.json --chrome-flags="--headless=new --no-sandbox" --quiet || echo "FAIL $s"
done
echo DONE
