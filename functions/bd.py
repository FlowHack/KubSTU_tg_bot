from base_data import Couple, DayWeek


def write_all_couples_in_bd(session, days):
    for day in days:
        day_bd = DayWeek(
            name=day.name,
            parity=day.parity
        )
        session.add(day_bd)
        session.commit()
        day_bd = session.query(DayWeek).filter(
            DayWeek.name == day.name
        ).filter(DayWeek.parity == day.parity).first()

        couples = []
        for couple in day.couples:
            couples.append(
                Couple(
                    title=couple.title,
                    university_building=couple.university_building,
                    lecture_stream=couple.lecture_stream,
                    lecture_hall=couple.lecture_hall,
                    teacher=couple.teacher,
                    period=couple.period,
                    note=couple.note,
                    time_from=couple.time_from,
                    time_to=couple.time_to,
                    type_of_occupation=couple.type_of_occupation,
                    couple_num=couple.couple_num,
                    week_id=day_bd.id
                )
            )

        session.add_all(couples)
        session.commit()
