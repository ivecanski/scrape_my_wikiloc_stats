""" Scrape wikiloc stats using selenium for browsing 
    Easy on wikiloc resources, gathers data from the 10-trail pages, not single trail pages """

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import creds
import time
import json
import os, os.path

login_url = 'https://www.wikiloc.com/wikiloc/login.do'
output_dir = 'output'
output_filename = 'my_wikiloc_stats_{}.csv'.format(time.strftime("%Y%m%d-%H%M%S"))

def wait(seconds):
    print("> going to sleep for {} seconds".format(seconds))
    time.sleep(seconds)

def get_output_filename():
    return os.path.join(output_dir,output_filename)

def main():

    driver = webdriver.Chrome()
    driver.get(login_url)

    # Find elements
    driver.find_element_by_xpath('//*[@id="email"]').send_keys(creds.email)
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(creds.password)
    driver.find_element_by_xpath('//*[@id="submit-button"]').click()

    # Go to sleep, allow the page to display fully and also allow extra time for manually solving the CAPTCHA in case it pops up
    wait(20)

    # If all went fine we should now be logged in and our main profile page displayed

    # Let's collect our trails information
    trails_list = []
    has_more_pages = True

    while has_more_pages:
        script_tag = driver.find_element_by_xpath("//script[contains(.,'let trails')]")
        if script_tag != None:
            script_text = script_tag.get_attribute('innerHTML')

            if script_text != None:
                
                # Extract the json with number of downloads/views
                trails_txt = 'let trails = '
                i = script_text.find(trails_txt)
                j = script_text.find(';\n')
                if i>-1:
                    trails_json_str = script_text[i+len(trails_txt):j]
                    trails_json = json.loads(trails_json_str)

                    for trail_json in trails_json:
                        trail = {
                            'name': trail_json["name"],
                            'views': trail_json["nViews"],
                            'downloads': trail_json["nDownloads"], 
                            'trailrank': trail_json['trailrank']
                        }
                        trails_list.append(trail)

                else:
                    print("Not found 'let trails' script tag")
            else:
                print("No element found!")
        else:
            print("Script with 'let trails' not found")

            
        # Find the link to the next page (if it exists)
        # XPath 2.0: "//a[@class='pagination__item'][1]/@href", 
        # Selenium supports XPath 1.0, only returns elements
        try:
            next_page_a = driver.find_element_by_xpath("//a[@class='pagination__item'][1]")
            next_page_href = next_page_a.get_attribute("href")
            print("-- next_page link: {}".format(next_page_href))
            driver.get(next_page_href)
            # wait a few seconds for the page to load
            wait(2)
        except:
            has_more_pages = False

    print("< all data gathered, processing...")

    # Load our trails to pandas for easy analysis
    # df = pd.DataFrame(trails_list)
    df = pd.json_normalize(trails_list)  # res is a list of json objects

    if not os.path.exists(output_dir): 
        os.makedirs(output_dir)

    filename = get_output_filename()
    df.to_csv(filename)

    # Close browswer
    driver.quit()

    print("Scraping completed, results stored in {}".format(filename))

if __name__ == '__main__':
    main()