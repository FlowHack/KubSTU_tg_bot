class Week:
    parity = None
    name = None
    next = None
    back = None
    couples = None

    def get_first(self):
        day = self

        while day.back is not None:
            day = day.back

        return day

    def get_all_days(self):
        days = []
        day = self.get_first()

        while day is not None:
            days.append(day)
            day = day.next

        return days

    def __str__(self):
        return f'{self.name} Количество пар: {len(self.couples)}'

    def __repr__(self):
        return f'{self.name} Количество пар: {len(self.couples)}'


class Couple:
    title = None
    university_building = None
    lecture_stream = False
    lecture_hall = None
    teacher = None
    period = None
    note = None
    time_from = None
    time_to = None
    type_of_occupation = None
    couple_num = None

    def __str__(self):
        lecture_hall = '' if self.lecture_hall is None else self.lecture_hall
        return f'{self.couple_num} {self.title} '  \
            f'{self.university_building}-{lecture_hall}'

    def __repr__(self):
        lecture_hall = '' if self.lecture_hall is None else self.lecture_hall
        return f'{self.couple_num} {self.title} '  \
            f'{self.university_building}-{lecture_hall}'
