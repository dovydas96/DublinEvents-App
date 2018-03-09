from bs4 import BeautifulSoup as Soup
from unidecode import unidecode
from geopy.geocoders import GoogleV3
import requests as re
import mysql.connector
import entertainment
from time import sleep
import eventbrite
import runner


class Database(object):
    """Class for taking scraper returns and working with the database accordingly"""
    def __init__(self, user, password, host, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.geolocator = GoogleV3(api_key="AIzaSyB1PDKub0qXbZae6x8VvhLze15Wf917V9w", timeout=20)

    def __enter__(self):
        self.cnx = mysql.connector.connect(user=self.user, password=self.password,
                                           host=self.host, database=self.database)
        print("Connected to database")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cnx.close()
        print("Finished with database")


    @staticmethod
    def select(query, column, table):
        """Returns a select statement to be used in SQL"""
        return unidecode(u"SELECT * FROM {0} WHERE {1} = \"{2}\" OR"
                         u" REPLACE({1}, \"\'\", \"\") = \"{2}\"").format(table, column, query.replace("'", ""))

    def check_db_venue(self, place):
        """Checks the database for the composite key of venue ie.(name, address)"""
        print "Checking database for " + place
        cur = self.cnx.cursor()
        name = self.select(place, "name", "venuesTest")
        cur.execute(name)
        name_res = len([l for l in cur])
        cur.close()
        return name_res # and add_res

    def google_it(self, place):
        """Google's a venue and returns information about it in a tuple as (name, rating, category, link, address)"""
        place = place
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        url = "https://www.google.ie/search?q="
        raw = re.get(url + place + "+dublin" + "&cr=IE", headers=headers)
        html = Soup(raw.content, "html5lib")
        result = html.find("div", {"class": "_OKe"})
        # if result.find("span", {"data-dtype": "d3ifr"}):
        #     phone = result.find("span", {"data-dtype": "d3ifr"}).get_text()
        # else:
        #     phone = ""
        address = result.find("span", {"class": "_Xbe"}).get_text()
        coords = self.geolocator.geocode(address)
        lat, lon = (coords.latitude, coords.longitude)
        image = result.find("img", {"alt": "Image"})
        category = self.fix_category(result.find("span", {"class": "_eMw"}).get_text())
        description = result.find("span", {"class": "_ZCm"}).text if result.find("span", {"class": "_ZCm"}) else category
        return (result.find("span", {'class': None}).get_text(),  # name
                result.find("span", {"class": "rtng"}).get_text(),  # rating
                category,  # category
                image.get("src"),  # image link
                address,  # address
                description,  # Description
                lon,
                lat)  # co-ordinates

    @staticmethod
    def get_details():
        pass

    @staticmethod
    def fix_category(cate):
        """Removes 'Republic of Ireland' from categories"""
        if "Republic of Ireland" in cate:
            cate = cate.split(",")[:-1]
            cate = ",".join(cate)
        if "in Dublin" in cate:
            return cate.replace("in Dublin", "")
        return cate

    def add_to_db_venue(self, place):
        """Adds a venue(tuple) to the database raises error if duplicate"""
        cur = self.cnx.cursor()
        name, rating, category, link, address, description, lon, lat = place
        try:
            add_place = ("INSERT INTO venuesTest "
                         "(name, rating, category, link, address, description, lon, lat) "
                         "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
            cur.execute(add_place, ((unidecode(name)).replace("'", ""),
                                    rating,
                                    category,
                                    link,
                                    address,
                                    description,
                                    lon,
                                    lat))
            print (add_place, ((unidecode(name)).replace("'", ""),
                               rating,
                               category,
                               link,
                               address,
                               description,
                               lon,
                               lat))
            print("ADDED ", name)
            self.cnx.commit()
        except mysql.connector.IntegrityError as err:
            print("Error: {}".format(err))
        cur.close()

    def find_image(self, venue_name):
        sel = "SELECT link FROM venuesTest WHERE name = \'{}\';".format(venue_name.replace("'", ""))
        cur = self.cnx.cursor()
        cur.execute(sel)
        # print(sel)
        i_link = "https://www.irishcentral.com/uploads/article/106499/cropped_MI_Guinness_pints_done_iStock.jpg"
        for res in cur:
            i_link = (res[0])
        cur.close()
        return i_link

    def add_to_db_event(self, event):
        """Adds an event (tuple) to the database raises error if duplicate"""
        cur = self.cnx.cursor()
        name, location, tickets, description, datetime, link = event
        if link == "":
            link = self.find_image(location)
        try:
            add_event = ("INSERT INTO eventsTest "
                         "(ename, location, tickets, description, datetime, elink) "
                         "VALUES (%s, %s, %s, %s, %s, %s)")
            # print(add_event, (name, (unidecode(location)).replace("'", ""), tickets, description, datetime))
            cur.execute(add_event, (name, (unidecode(location)).replace("'", ""), tickets, description, datetime, link))
            print("ADDED ", name)
            self.cnx.commit()
        except mysql.connector.IntegrityError as err:
            print("Error: {}".format(err))
        cur.close()

    def check_add_venue(self, place):
        """Takes a venue name and if it is not in the database it tries to add it"""
        if not self.check_db_venue(place):
            try:
                venue_details = self.google_it(place)
                self.add_to_db_venue(venue_details)
                print("{} added to DB".format(place))
                return venue_details[0]
            except AttributeError:
                print("Not enough info on {}".format(place))
                return
        else:
            print("{} already in DB".format(place))
            return place

    def check_add_event(self, event):
        """Adds an event to the events table and the venue to the venue table if it doesn't already exist there"""
        # print(event[1])
        name = self.check_add_venue(event[1])
        if name:
            self.add_to_db_event((event[0], name, event[2], event[3], event[4], event[5]))
        else:
            self.add_to_db_event(event)

    def run(self, scraper):
        for event in scraper:
            output = ""
            try:
                self.check_add_event(event)
            except (UnicodeEncodeError, mysql.connector.DatabaseError, ValueError, TypeError) as err:
                output += "Error : {}".format(err) + "\n"
            output += "________________________________________"
            print(output)


# db = Database("test", "1234", "159.65.84.145", "app")
# with db:
# #     # print db.google_it("the great wood")
#     db.run(foo())
    # for event in entertainment.get_info():
#         try:
#             db.check_add_event(event)
#         except UnicodeEncodeError as err:
#             print("Error : {}".format(err))
#             print("ERROR WITH", event)
#         print ("________________________________________")
#     db.check_add_venue("The Grand Social")
# db = Database("test", "1234", "159.65.84.145", "app")
# with db:
#     for event in eventbrite.get_info():
#         try:
#             db.check_add_event(event)
#         except (UnicodeEncodeError, mysql.connector.DatabaseError) as err:
#             print("Error : {}".format(err))
#             print("ERROR WITH", event)
#         print ("________________________________________")