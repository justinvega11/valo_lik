from sqlalchemy.orm import Session
from database import User


def create_user(db: Session, discord_id: str, discord_name: str, riot_name: str = None, riot_tag: str = None):
    db_user = User(
        discord_id=discord_id,
        discord_name=discord_name,
        riot_name=riot_name,
        riot_tag=riot_tag
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user