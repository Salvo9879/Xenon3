
# Import internal modules
from package.databases import db, Users

def create_user(forename: str, surname: str, username: str, email: str, birthdate: str, password: str) -> Users:
    u = Users()
    
    u.forename = forename
    u.surname = surname

    u.username = username
    u.email = email

    u.birthdate = birthdate

    u.password = password

    try:
        db.session.add(u)
        db.session.commit()
    except:
        return None
    return u