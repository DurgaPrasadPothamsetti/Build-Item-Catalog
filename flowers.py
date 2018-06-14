from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Flowershop, Base, AvailableItem, Guest


engine = create_engine('sqlite:///flowershop.db')


Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()



Guest1 = Guest(name="durgareddy", email="15pa1a05d7@vishnu.edu.in",
             picture='https://www.ienglishstatus.com/wp-content/uploads/2018/04/Anonymous-Whatsapp-profile-picture.jpg')
session.add(Guest1)
session.commit()



shop1 = Flowershop(guest_id=1, name="vit")
session.add(shop1)
session.commit()


flower1 = AvailableItem(guest_id=1, nameofflower="rose",course="season",information="this is rose",price="$3",
                          flowershop=shop1)

session.add(flower1)
session.commit()

flower2 = AvailableItem(guest_id=1, nameofflower="lilly",course="nonseason",information="this is lilly",price="$4",
                          flowershop=shop1)

session.add(flower2)
session.commit()

flower3 = AvailableItem(guest_id=1, nameofflower="jasmine",course="everyseason",information="this is jasmine",price="$4",
                          flowershop=shop1)

session.add(flower3)
session.commit()



shop2 = Flowershop(guest_id=1, name="dnr")
session.add(shop2)
session.commit()


flower1 = AvailableItem(guest_id=1, nameofflower="tulip",course="season",information="this is tulip",price="$5",
                          flowershop=shop2)

session.add(flower1)
session.commit()

flower2 = AvailableItem(guest_id=1, course="nonseason",nameofflower="tulipblack",information="this is tulipblack",price="$7",
                          flowershop=shop2)

session.add(flower2)
session.commit()


shop3 = Flowershop(guest_id=1, name="biet")
session.add(shop3)
session.commit()


flower1 = AvailableItem(guest_id=1, nameofflower="banth",course="everyseason",information="this is banth",price="$15",
                           flowershop=shop3)

session.add(flower1)
session.commit()

                          

                          

                          
