from app import db

class TotalRouteTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    route = db.Column(db.String(32))
    total_time = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)

    @property
    def timestamp_fmt(self):
        return self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
