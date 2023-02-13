## My Python Scraping Projects

## priceComparison.py

    This is a tool used to compare prices of products on various ecommerce sites
    1. Users enter the name of the product they want
    2. The program scrapes the prices of the top 10 results on the various ecommerce sites
    3. The program calculates the average price for each site and returns the results to the user

## jobListings.py

    This is a tool used to scrape websites for required job postings
    Its activity is masked using the tor client and temporary html headers while scraping
    The tool looks through the websites everjobs, theugandanjobline and ugandajob
    It uses 3 thread to look for the required job on all the websites simultaneously
    it organises the results found and presents the url, the job title, organisation and location of the job listing in the terminal

## wikiProfileScraper.py

    This is a program that scrapes wikipedia profile pages for details and information about the people
    It starts with a base url then it collects the name, date of birth and birthplace of the person
    It then organizes and formats them uniformly
    It finally stores the information in a mysql database
    Afterwards, it scrapes the rest of the page for more profile links and recursively processes them
    The program creates multiple threads and detail collection, link collection and dB storage are all done by separate threads

## newsAggregator.py

    This is a program used to collect news articles from various websites and publish them in on a central site
    the program visits the top 5 news paper companies in Uganda namely: The daily monitor for national news, New Vision for world news,
    The independent for business news, KFM for lifestyle news and the kampala sun for gossip
    The scraper is powered by 5 independent scrapers that collect information from the webistes simultaneously