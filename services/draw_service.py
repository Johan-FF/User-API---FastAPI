from models.draw_model import DrawModel
from schemas.draw_schema import DrawSchema

class DrawService():
    def __init__(self, db):
        self.db = db

    def get_draws_by_owner(self, id_owner: int):
        result = self.db.query(DrawModel).filter(DrawModel.id_owner == id_owner).all()
        return result

    def get_id_by_name(self, name: str):
        result = self.db.query(DrawModel).filter(DrawModel.name == name).one_or_none()
        return result.id

    def get_draw(self, id) -> DrawSchema:
        result = self.db.query(DrawModel).filter(DrawModel.id == id).one_or_none()
        return result

    def create_draw(self, draw: DrawSchema):
        exists = self.get_draw(draw.id)
        if not exists:
            new_draw = DrawModel(**draw.dict())
            self.db.add(new_draw)
            self.db.commit()
            return True
        return False

    def update_draw(self, id: int, draw: DrawSchema):
        draw_found = self.db.query(DrawModel).filter(DrawModel.id == id).one_or_none()
        if not draw_found:
            return False
        update_draw = draw.dict()
        draw_found.update( **update_draw )
        self.db.commit()
        return True

    def delete_draw(self, id: int):
        draw_to_delete = self.db.query(DrawModel).filter(DrawModel.id == id).one_or_none()
        if not draw_to_delete:
            return False
        self.db.delete(draw_to_delete)
        self.db.commit()
        return True