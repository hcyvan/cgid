from application.ext import db


class BaseModel(db.Model):
    __abstract__ = True
    db = db
    exclude_fields = []

    def to_dict(self):
        result = {}
        for c in self.__dict__.keys():
            if c.startswith('_') or c in self.exclude_fields:
                continue
            value = getattr(self, c, None)
            if isinstance(value, list):
                result[c] = [e.to_dict() if isinstance(e, db.Model) else e for e in value]
            elif isinstance(value, db.Model):
                result[c] = value.to_dict()
            else:
                result[c] = value

        return result

    def update(self):
        self.db.session.commit()
        return self

    def save(self):
        try:
            self.db.session.add(self)
            self.db.session.commit()
            # self.db.session.refresh(self)
        except Exception as e:
            self.db.session.rollback()

    def delete(self):
        self.db.session.delete(self)
        self.db.session.commit()
