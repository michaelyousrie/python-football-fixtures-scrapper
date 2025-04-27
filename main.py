import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def main():
    chrome_driver_path = './chromedriver'
    website = 'https://www.theguardian.com/football/premierleague/fixtures'

    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service)

    driver.get(website)

    containers = driver.find_elements(by="xpath", value='//section[@class="dcr-jjtqpb"]')
    if not len(containers):
        print("Couldn't fetch any upcoming fixtures..")
        exit()
    #endif

    all_matches = []

    for container in containers:
        date = container.find_element(by=By.XPATH, value='./h2').text
        matches = container.find_elements(by=By.TAG_NAME, value='li')

        if not len(matches):
            print("No Matches found...")
            continue
        #endif

        for match in matches:
            time = match.find_element(by=By.TAG_NAME, value='time').text
            home = match.find_element(by=By.CLASS_NAME, value='dcr-iqim6o').text
            away = match.find_element(by=By.CLASS_NAME, value='dcr-rm7qtf').text

            all_matches.append({
                'date': date,
                'time': time,
                'home': home,
                'away': away
            })
        #endfor
    #endfor

    driver.quit()

    with open('results.json', 'w') as file:
        json.dump(all_matches, file, indent=4)
    #endwith
#enddef


if __name__ == '__main__':
    main()
#endif