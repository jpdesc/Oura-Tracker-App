from database import *

db.session.query(Template).delete()
db.session.query(Weights.template_id).delete()
db.session.query()
db.session.commit()
