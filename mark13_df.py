#import libraries
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import re

#import user-defined modules
import mark13_useragent

def get_df(url,search_word):
    prod_title=[]
    prices=[]
    prod_ratings=[]
    description=[]
    num_ratings=[]
    num_reviews=[]
    prod_id=[]
    images=[]
    seller=[]
    seller_ratings=[]

    req=mark13_useragent.fetch_html_requests(url)
    print(req)
    content=BeautifulSoup(req.content.decode('utf-8'),"html.parser")
    box=content.find("div",class_='DOjaWF YJG4Cf')

    links=[]
    start_link="https://www.flipkart.com"
    data=box.find_all('div',{'class':'slAVV4'})
    if data:
        #TITLE
        for items in data:
            rest_link=items.find('a')['href']
            name=items.find('a',attrs={'class':'wjcEIp'})
            prod_title.append(name.text)
            links.append(start_link+rest_link)
    else:
        data=box.find_all('div',{'class':'tUxRFH'})
        if data:
            for items in data:
                rest_link=items.find('a')['href']
                name=items.find('div',attrs={'class':'KzDlHZ'})
                prod_title.append(name.text)
                links.append(start_link+rest_link)
        else:
            data=box.find_all('div',{'class':'_1sdMkc LFEi7Z'})
            if data:
                for items in data:
                    rest_link=items.find('a')['href']
                    name=items.find('a',attrs={'class':'WKTcLC'})
                    prod_title.append(name.text)
                    links.append(start_link+rest_link)
            else:
                print("Data not found")
            

    #PRODUCT RATINGS
    for items in data:
        rating_div = items.find('div', class_='XQDdHH')
        if rating_div:
            prod_ratings.append(rating_div.text.strip())
        else:
            prod_ratings.append('NA')
        
    if not rating_div:
        prod_ratings=[]
        for i in links:
            r=mark13_useragent.fetch_html_requests(i)
            soup=BeautifulSoup(r.text,"html.parser")
            rating_div=soup.find('div', class_='XQDdHH _1Quie7')
            if rating_div:
                prod_ratings.append(rating_div.text.strip())
            else:
                prod_ratings.append('NA')

    for i in links:
        r=mark13_useragent.fetch_html_requests(i)
        soup=BeautifulSoup(r.text,"html.parser")
        
        #PRODUCT ID
        parsed_url = urlparse(i)
        query_params = parse_qs(parsed_url.query)
        pid_param = query_params.get('pid', None)
        if pid_param:
            pid_value = pid_param[0]
            prod_id.append(str(pid_value))
        else:
            prod_id.append('NA')


        #PRICES
        pri=soup.find('div',class_='Nx9bqj CxhGGd')
        if pri:
            for i in pri:
                pri_only=i.text
                prices.append(pri_only)
        else:
            prices.append("NA")

        #IMAGES
        uls = soup.find_all('ul',class_='ZqtVYK')
        if uls:
            # Iterate over each unordered list
            for ul in uls:
                image_list=[]

                # Find all img tags within the unordered list
                imgs = ul.find_all('img')

                # Extract the source (src) attribute of each image and print it
                for img in imgs:
                    image_list.append(img['src'])
                images.append(image_list)

        else:
            imgs=soup.find_all('img',class_='DByuf4 IZexXJ jLEJ7H')
            image_list2=[]

            for img in imgs:
                image_list2.append(img['src'])
            images.append(image_list2)


        #DESCRIPTION
        desc=soup.find_all('div',class_='xFVion')
        if desc:
            for i in desc:
                desc_only=i.text
                description.append(desc_only)
        else:
            description.append("NA")

        #SELLER
        sel=soup.find('div',class_='yeLeBC')
        if sel:
            second_span = sel.find('span').find_next('span') 
            seller.append(second_span.text.strip())
        else:
            seller.append("NA")

        #SELLER RAINGS
        selrat=soup.find_all('div',class_='XQDdHH uuhqql')
        if selrat:
            for i in selrat:
                selrat_only=i.text
                seller_ratings.append(selrat_only)
        else:
            seller_ratings.append('No rating')

        #REVIWES & RATINGS
        contents= soup.find_all('div', {"class": "row j-aW8Z"})
        if contents:
            for content in contents:
                span = content.find('span')
                if span and 'Reviews' in span.text:
                    reviews_text = span.text
                    num_reviews.append(reviews_text[:-7])
                if span and 'Ratings' in span.text:
                    ratings_text = span.text
                    num_ratings.append(ratings_text[:-9])
        else:
            rat_rev = soup.find('span', class_='Wphh3N d4OmzS')
            if rat_rev:
                ratings_pattern = r'(\d+(,\d+)*)\s+ratings'
                reviews_pattern = r'(\d+(,\d+)*)\s+reviews'
                # Extract numbers using regular expressions
                ratings_match = re.search(ratings_pattern, rat_rev.text)
                reviews_match = re.search(reviews_pattern, rat_rev.text)
        
                # Store the numbers in variables
                num_rat = int(ratings_match.group(1).replace(",", "")) if ratings_match else None
                num_rev = int(reviews_match.group(1).replace(",", "")) if reviews_match else None
                num_ratings.append(num_rat)
                num_reviews.append(num_rev)
            else:
                num_reviews.append('0')
                num_ratings.append('0')

    # Check lengths of lists
    print("Length of title:", len(prod_title))
    print("Length of ratings:", len(prod_ratings))
    print("Length of prod_id:", len(prod_id))
    print("Length of prices:", len(prices))
    print("Length of images:", len(images))
    print("Length of description:", len(description))
    print("Length of seller:", len(seller))
    print("Length of seller_ratings:", len(seller_ratings))
    print("Length of num_reviews:", len(num_reviews))
    print("Length of num_ratings:", len(num_ratings))
    print("\n")

    df=pd.DataFrame({"Search Word":search_word,"Product Title":prod_title,"Prices":prices,"Rating":prod_ratings,"Description":description,"Num of Ratings":num_ratings,"Num of Reviews":num_reviews,"Product Id":prod_id,"Images":images,"Seller":seller,"Seller Ratings":seller_ratings})
    print(df)

    return df