import sqlite3

class SqliteDB(object):

	def __init__(self,cursor):
		self.cursor = cursor

	def create_db(self):
		self.cursor.execute("""CREATE TABLE events(
							event_id text,
							name text,
							description text,
							event_time text,
							event_date text,
							ticket_info text,
							event_price text,
							location text,
							pub_id text
							)""")

		self.cursor.execute("""CREATE TABLE pubs(
							name text,
							description text,
							location text,
							pub_id text
							)""")


	def add_events(self,event):
		self.cursor.execute("""INSERT INTO events VALUES (:name,:description,:location,
													 :event_time,:event_date,:ticket_info,
													 :event_price,:event_id,:pub_id)""",
													 {"event_id":event.event_id,
													 "name":event.name,
													 "description":event.description,
													 "event_time":event.time,
													 "event_date":event.date,
													 "ticket_info":event.ticket_url,
													 "event_price":event.price,
													 "location":event.location,
													 "pub_id":event.pub_id})

	def remove_event(self,event):
		self.cursor.execute("DELETE FROM events WHERE event_id = :event_id",
						{"event_id":event.id})

	def add_pub(self,pub):
		self.cursor.execute("INSERT INTO pubs VALUES (:name,:description,:location,:pub_id)",
												   {"name":pub.name,
												    "description":pub.description,
												    "location":pub.location,
												    "pub_id":pub.pub_id})
	def remove_pub(self,pub):
		self.cursor.execute("""DELETE FROM pubs WHERE pub_id = :pub_id""",{"pub_id":pub.pub_id})

	def print_all_pubs(self):
		self.cursor.execute("SELECT * FROM pubs")
		print(self.cursor.fetchall())

	def print_all_events(self):
		self.cursor.execute("SELECT * FROM events")
		print(self.cursor.fetchall())	


def main():
	conn = sqlite3.connect('event.db')
	cur = conn.cursor()
	db = SqliteDB(cur)
	pub = Pub("name","description","location",1234)
	db.add_pub(pub)
	conn.commit()
	db.testy_test()
	conn.close()

if __name__ == '__main__':
	main()