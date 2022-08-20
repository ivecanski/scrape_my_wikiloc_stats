#### Overview

Wikiloc is a great site for documenting your trails. However, there is currently no way to quickly get an overview of your own basic stats - how many times your trails were viewed and downloaded. 

This script scrapes **your own wikiloc account** (you need to login) and pulls the stats from the 10-trail pages instead of going through each individual trail - we try to be as easy on the website as possible. Since the stats are collected from your own account (while logged in), the scraping does not affect your stats, i.e. the number of views of your trails won't be incremented by running the script. Note that if you visit the same pages without being logged in the statistics data won't be available!

Initially I tried to implement the scraping using [Scrapy](https://scrapy.org), and also [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) with requests, but both approaches failed as wikiloc was asking for captchas. The only way I could get around this was by using [Selenium](https://www.selenium.dev) and let the user resolve the captcha manually. 

#### Sample data

Sample html pages that were used at the time the scraper was implemented are located in the `sample_data` folder. 

#### Environment

The script runs with python3, you need to install selenium and pandas libraries into your virtual environment:
```
pip install selenium
pip install pandas
```
Apart from that, you will also need to [install the WebDriber](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/) which drives the browser.

The script also requires a `creds.py` file to be present in the current directory. This is a simple file with two entries:

```
email = '<your_email>'
password = '<your_password>'
```
These will be picked up by the script to fill in the credential fields.

#### Running the script

After sourcing your virtualenv, run the script simply with `python scrape.py`:

```
~/dev/python/scrape_my_wikiloc_stats $ source /home/ivan/.virtualenvs/scraping_selenium/bin/activate
(scraping_selenium)  ~/dev/python/scrape_my_wikiloc_stats $ python scrape.py 
> going to sleep for 20 seconds
-- next_page link: https://www.wikiloc.com/wikiloc/user.do?id=6046035&from=10&to=20
> going to sleep for 5 seconds
-- next_page link: https://www.wikiloc.com/wikiloc/user.do?id=6046035&from=20&to=30
> going to sleep for 5 seconds
-- next_page link: https://www.wikiloc.com/wikiloc/user.do?id=6046035&from=30&to=40
> going to sleep for 5 seconds
< all data gathered, processing...
.. done
```
The script sleeps at certain points to allow the pages to be loaded (waiting could be optimized), and the initial wait is longer in order to allow the captcha to be resolved manually. 

#### Resulting CSV file

The script outputs the results as a csv file in the `output` sub-directory, with a unique name based on the current timestamp. An example of the output is shown below. You can further order the fields as you please.

||trail name                                                     |views|downloads|trailrank|
|------|---------------------------------------------------------|-----|---------|---------|
|0     |Vrhovi Povlena                                           |5    |1        |41       |
|1     |Stara planina: Hotel 'Stara planina' - Babin zub         |17   |3        |36       |
|2     |Stara planina: Hotel 'Babin zub' - Midžor                |64   |14       |52       |
|3     |Rila: Yastrebets - Musala                                |223  |14       |49       |
|4     |Gvozdačke stene, Azbukovica                              |23   |1        |36       |
|5     |Kučajske planine: Vrelo Grze                             |5    |2        |30       |
|6     |Kosmaj                                                   |78   |9        |33       |
|7     |Avala                                                    |54   |4        |35       |
|8     |Fruška Gora: Stražilovo                                  |50   |3        |39       |
|9     |Jablanik                                                 |34   |3        |35       |
|10    |Vršačka kula - Lisičija glava - Malo Središte            |76   |1        |35       |
|11    |Košutnjak                                                |11   |1        |19       |
|12    |Cer: Lipove Vode - Kosanin grad - Šančine - Trojanov grad|95   |6        |34       |
|13    |Rajac Suvobor                                            |160  |14       |36       |


#### Possible further improvements

The output currently doesn't contain the date when the trail took place. The reason is that this information is not available on 10-trail pages. Fetching the date would require the scraping of each individual trail.