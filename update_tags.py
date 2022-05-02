from app import Tag, tags, db

def clear_tags():
    db.session.query(tags).delete()
    db.session.query(Tag).delete()
    db.session.commit()

clear_tags()
