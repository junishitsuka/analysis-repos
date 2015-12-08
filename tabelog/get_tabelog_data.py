from selenium import webdriver
from bs4 import BeautifulSoup

def main():
    driver = webdriver.PhantomJS()
    # url = "http://tabelog.com/tokyo/A1305/A130504/R11084/rstLst/?LstRange=SG&svd=20151207&svt=2100&svps=2" # 西早稲田 500m
    url = "http://tabelog.com/tokyo/A1304/A130401/R8219/rstLst/?LstRange=SG&svd=20151207&svt=1900&svps=2" # 東新宿500m
    while url:
        driver.get(url)
        data = driver.page_source.encode('utf-8')
        url = get_page_content(data)
    driver.quit()
    return 

def get_page_content(data):
    html = BeautifulSoup(data, "html.parser")
    store_list = html.find_all("li", class_="list-rst")
    next_url = html.find("a", class_="page-move__target--next")
    for store in store_list:
        output_store_content(store)
    if next_url:
        return next_url.attrs["href"]
    return ""

def output_store_content(store):
    name = store.find("a", class_="list-rst__rst-name-target")
    area_genre = store.find("span", class_="list-rst__area-genre")
    rating = store.find_all("span", class_="list-rst__rating-val") # 総合, 夜, 昼
    num = store.find("em", class_="list-rst__rvw-count-num")
    budget = store.find_all("span", class_="list-rst__budget-val") # 夜, 昼
    table = store.find("p", class_="list-rst__table-data")
    pr = store.find("p", class_="list-rst__pr")

    if len(rating) == 0:
        rating = ["-","-","-"]
    else:
        rating = [e.string for e in rating]

    if pr:
        pr = pr.string.strip()
    else:
        pr = ""

    return print("%s;%s;%s;%s;%s;%s;%s;%s;%s" % (
        name.string,
        area_genre.string,
        rating[0],
        rating[1],
        rating[2],
        budget[0].string,
        budget[1].string,
        table.string.strip(),
        pr
    ))

if __name__ == "__main__":
    print("name;area_genre;rating;dinner_rating;lunch_rating;dinner_budget;lunch_budget;table;pr")
    main()
