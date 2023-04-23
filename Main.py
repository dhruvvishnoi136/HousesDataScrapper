# d: && cd me\#\python\HousesDataScrapper && python -u "d:\ME\#\PYTHON\HousesDataScrapper\Main.py"
from time import sleep, time
import io
import mysql.connector as databaseConn
from bs4 import BeautifulSoup
from os import fsync
from selenium import webdriver
import selenium.common.exceptions as selExec
import random
def fetchAllLinks(driver:webdriver.Chrome):
    startTimeFetchingLinks = time()
    totalNumberOfPages = 0
    linksFileObj = io.open(file = "./assets/AllPagesLinks.txt", mode = "w", encoding = "utf-8")
    driver.get("https://www.99acres.com/")
    driver.maximize_window()
    # Search for specific location and get counter 
    try:
        sleep(1)
        driver.find_element(by = "xpath",value="//*[@id=\"keyword2\"]").send_keys("Delhi")
        sleep(2)
        driver.find_element(by = "xpath", value = "//*[@id=\"inPageSearchForm\"]/div[2]/div/div/div[1]/div[3]/button").click()
        sleep(4)
        pageNumberFinderSoup = BeautifulSoup(driver.page_source, features = 'html.parser').find("div", {"class":"caption_strong_large"}) 
        if pageNumberFinderSoup is not None:
            totalNumberOfPages = int((pageNumberFinderSoup.text).split(" ")[-1])
            print("\n\nFound total Pages")
        else:
            print("\n\nUnable to find Counter value")
            del pageNumberFinderSoup
            exit()

        print()
    except Exception as e:
        print("\n\n\n\nsError While in \"fetchData\" function\n\n")
        print(e)
        exit()
    
    # Getting links to all the pages we got pages
    nextSetFinder = ""
    pageIterator = totalNumberOfPages/10
    pagesData = []
    while(pageIterator <= 0):
        temporaryListOfLinks = []
        timer1 = random.randrange(3,6)
        print(f"\nWaiting for {timer1} Seconds")
        sleep(timer1)
        #Fetching links from Current Page
        try:
            #Flushing 10 links in file
            pagesData = BeautifulSoup(
                                        str(
                                            BeautifulSoup(
                                                            driver.page_source,
                                                            features = 'html.parser'
                                                            ).find("div", {"class" : "Pagination__srpPageBubble list_header_semiBold"})
                                            )
                                            ,features = 'html.parser'
                                        ).find_all('a', href = True)
            
            for aTag in pagesData:
                temporaryListOfLinks.append(aTag['href'])
            
            temporaryListOfLinks[0] = str(driver.current_url)
            # Flushing in a File
            try:
                for aLink in temporaryListOfLinks:
                    linksFileObj.write(aLink + "\n")
                    linksFileObj.flush()
                print("\n\nFlushed One Set of 10")
            except Exception as e:
                print("\n\nunable to Flush Links in File for link set", driver.current_url)
                print(e)            
        except Exception as e:
            print("\n\nUnable to Process Current Page Data")   
            print(e)
                    
        # Fetch Next 10 links
        timer2 = random.randrange(1,3)
        print(f"\nWaiting for {timer2} Seconds")
        sleep(timer2)
        driver.get(temporaryListOfLinks[-1])
        try:
            # Getting link to load next 10 pages links
            nextSetFinder = (BeautifulSoup(
                                            str(
                                                BeautifulSoup(driver.page_source
                                                            , features = 'html.parser'
                                                            ).find("div", {"class" : "Pagination__srpPagination"})
                                                ),
                                                features = 'html.parser'
                                                ).find_all('a', href = True)[-1])["href"]
            timer3 = random.randrange(2,5)
            print(f"\nWaiting for {timer3} Seconds")
            sleep(random.randrange(2,5))
            driver.get(nextSetFinder)
        except Exception as e:
            print("\n\nUnable to find next page")
        
        print(f"Page Number:- {pageIterator}")
        pageIterator -= 1
    print(f"Time Taken while Fetching Links:- {(time() - startTimeFetchingLinks)/60}")

# Stage 2
def fetchData(driver:webdriver.Chrome):
    startTimeFetchingData = time()
    driver.maximize_window()
    linksFileObj = io.open(file = "./assets/allPagesLinks.txt", mode = 'r', encoding = "utf-8")
    dataDivFramesFileObj = io.open("./assets/dataDivFrames.txt", mode = 'a', encoding = "utf-8")
    dataTableFramesFileObj = io.open("./assets/dataTablesFrames.txt", mode = 'a', encoding = "utf-8")
    for link in linksFileObj.readlines():
        print(f"\nFetching Link:- {link}")
        sleep(random.randrange(1,7))
        driver.get(str(link))
        last_height = driver.execute_script("return document.body.scrollHeight")
        new_height = 0
        while new_height != last_height:
            last_height = new_height
            for i in range(1, last_height):
                sleep(random.uniform(0.125,1))
                temp = i * 1000
                if temp < last_height:
                    i = temp
                    driver.execute_script(f"window.scrollTo(0, {i});")
                else:
                    break
            new_height = driver.execute_script("return document.body.scrollHeight")

        # Extracting data frames of link 
        sleep(3)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        dataDivFrames = soup.find_all(name = "div", attrs = {"class" : "projectTuple__descCont"})
        dataTablesFrames = soup.find_all(name = "table", attrs = {"class" : "false"})

        print("Length of dataDivFrames:- " + str(len(dataDivFrames)))
        print("Length of dataTablesFrames:- " + str(len(dataTablesFrames)))
        for divFrames in dataDivFrames:
            dataDivFramesFileObj.write(str(divFrames) + "\n")
        for tableFrames in dataTablesFrames:
            dataTableFramesFileObj.write(str(tableFrames) + "\n")
        dataDivFramesFileObj.flush()
        fsync(dataDivFramesFileObj.fileno())
        dataTableFramesFileObj.flush()
        fsync(dataTableFramesFileObj.fileno())

    linksFileObj.close()
    dataDivFramesFileObj.close()
    dataTableFramesFileObj.close()
    print(f"Time Taken while Fetching Data:- {(time() - startTimeFetchingData)}")
# Stage 3
def cleaner(dataTagsList:list):
    startTimeCleaner = time()
    print(f"Time Taken while Cleaning:- {(time() - startTimeCleaner)/60}")

# Stage 4
def injectorSQL(dataGram:dict):
    return

if __name__ == "__main__":
    website = "https://www.99acres.com/"
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(executable_path = "./assets/chromedriverV112_0_5615_121.exe", options = options)
    try:
        # fetchAllLinks(driver = driver)
        fetchData(driver = driver)
    except Exception as exec:
        print(f"\n\n\nUnknown Error occured:-\n{exec}")
        exit()
    finally:
        driver.quit()

    
