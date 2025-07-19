# utils/player_bio_parser.py — Playwright + conversion

from playwright.async_api import async_playwright


def convert_height_to_cm(height_str: str) -> int:
    try:
        feet, inches = height_str.replace("′", "'").replace("″", "").split("'")
        return round(int(feet) * 30.48 + int(inches) * 2.54)
    except Exception:
        return 0


def convert_weight_to_kg(weight_str: str) -> int:
    try:
        pounds = int(weight_str.replace(" lb", "").strip())
        return round(pounds * 0.453592)
    except Exception:
        return 0


async def get_player_bio(player_id: int) -> dict:
    url = f"https://www.nhl.com/player/{player_id}"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        print("Page loaded:", page.url)

        try:
            await page.wait_for_selector("#player-info", timeout=5000)
            player_info = await page.query_selector("#player-info")

            if not player_info:
                print("player-info block still not found!")
                await browser.close()
                return {}

            items = await player_info.query_selector_all("div")
            bio_data = {}
            for item in items:
                label_el = await item.query_selector("b")
                if not label_el:
                    continue
                label = (await label_el.inner_text()).replace(":", "").strip()
                full_text = await item.inner_text()
                value = full_text.replace(await label_el.inner_text(), "").strip()

                if label == "Height":
                    bio_data["Height_cm"] = convert_height_to_cm(value)
                elif label == "Weight":
                    bio_data["Weight_kg"] = convert_weight_to_kg(value)
                else:
                    bio_data[label] = value

            print("Parsed Bio:", bio_data)
            await browser.close()
            return bio_data

        except Exception as e:
            print("Error or Timeout:", e)
            await browser.close()
            return {}
