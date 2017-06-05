class AtoBAssoc(db.Model, BaseModelMixin):
    __tablename__ = 'A_B_assoc'

    a_id = db.Column(db.Integer, db.ForeignKey("a.id",
                                                  ondelete="CASCADE"),
                        nullable=False)

    b_id = db.Column(db.Integer, db.ForeignKey("b.id"),
                        nullable=False)

    type = db.Column(db.String(50))
    bb = db.relationship("B", backref="A_B_assoc")

    @staticmethod
    def associate_b(a, b, type):
        b_objs = B.query.filter(
            B.name.in_(b)).all()
        b_exist = [b_obj.name for b_obj in b_objs]
        missing_b = set(b).difference(set(b_exist))
        for missing_b in missing_b:
            b = B(name=missing_b)
            error = b.persist()
            if error:
                return error

            b_objs.append(b)

        for bobj in b_objs:
            aba = AtoBAssoc(a_id=changeset.id,
                                b_id=bobj.id, type=type)
            a.association.append(aba)
            db.session.add(aba)
        db.session.commit()