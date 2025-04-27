import json
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def main():
    chrome_driver_path = Path('./chromedriver').absolute()
    website = 'https://www.theguardian.com/football/premierleague/fixtures'

    service = Service(executable_path=chrome_driver_path)
    with webdriver.Chrome(service=service) as driver:
        driver.get(website)

        containers = driver.find_elements(by=By.XPATH, value='//section[@class="dcr-jjtqpb"]')
        if not containers:
            print("Couldn't fetch any upcoming fixtures..")
            exit()
        #endif

        all_matches = []

        for container in containers:
            date = container.find_element(by=By.XPATH, value='./h2').text
            matches = container.find_elements(by=By.TAG_NAME, value='li')

            if not matches:
                print("No Matches found...")
                continue
            #endif

            for match in matches:
                try:
                    time = match.find_element(by=By.TAG_NAME, value='time').text
                    home = match.find_element(by=By.CLASS_NAME, value='dcr-iqim6o').text
                    away = match.find_element(by=By.CLASS_NAME, value='dcr-rm7qtf').text

                    all_matches.append({
                        'date': date,
                        'time': time,
                        'home': home,
                        'away': away
                    })
                except Exception as e:
                    print(f"Skipping a match due to missing data: {e}")
                    continue
                #endtry
            #endfor
        #endfor

    results_path = Path('results.json')
    with results_path.open('w', encoding='utf-8') as file:
        json.dump(all_matches, file, indent=4, ensure_ascii=False)
    #endwith

    print("Done!")
#enddef


if __name__ == '__main__':
    main()
#endif