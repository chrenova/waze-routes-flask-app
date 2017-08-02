from datetime import datetime
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db, models


def main():
    db.drop_all()
    db.create_all()

    t = models.TotalRouteTime(route='a', total_time=1000, timestamp=datetime(2017, 7, 20, 16, 30, 0))
    db.session.add(t)
    t = models.TotalRouteTime(route='a', total_time=1050, timestamp=datetime(2017, 7, 20, 17, 30, 0))
    db.session.add(t)
    t = models.TotalRouteTime(route='a', total_time=900, timestamp=datetime(2017, 7, 20, 18, 00, 0))
    db.session.add(t)
    t = models.TotalRouteTime(route='a', total_time=1100, timestamp=datetime(2017, 7, 20, 18, 30, 0))
    db.session.add(t)
    db.session.commit()


if __name__ == '__main__':
    main()
