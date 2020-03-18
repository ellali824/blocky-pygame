"""
Assignment 0 starter code
CSC148, Winter 2020

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Mario Badr, Christine Murad, Diane Horton, Misha Schwartz, Sophia Huynh
and Jaisie Sin

All of the files in this directory and all subdirectories are:
Copyright (c) 2020 Mario Badr, Christine Murad, Diane Horton, Misha Schwartz,
Sophia Huynh and Jaisie Sin
"""
from datetime import datetime
from typing import Dict, List, TextIO, Tuple

# The additional pay per hour instructors receive for each certificate they
# hold.
BONUS_RATE = 1.50


class WorkoutClass:
    """A workout class that can be offered at a gym.

    === Private Attributes ===
    _name: The name of this WorkoutClass.
    _required_certificates: The certificates that an instructor must hold to
        teach this WorkoutClass.
    """
    _name: str
    _required_certificates: List[str]

    def __init__(self, name: str, required_certificates: List[str]) -> None:
        """Initialize a new WorkoutClass called <name> and with the
        <required_certificates>.

        >>> workout_class = WorkoutClass('Kickboxing', ['Strength Training'])
        >>> workout_class.get_name()
        'Kickboxing'
        """
        self._name = name
        self._required_certificates = required_certificates[:]

    def get_name(self) -> str:
        """Return the name of this WorkoutClass.

        >>> workout_class = WorkoutClass('Kickboxing', ['Strength Training'])
        >>> workout_class.get_name()
        'Kickboxing'
        """
        return self._name

    def get_required_certificates(self) -> List[str]:
        """Return all the certificates required to teach this WorkoutClass.

        >>> workout_class = WorkoutClass('Kickboxing', ['Strength Training'])
        >>> workout_class.get_required_certificates()
        ['Strength Training']
        """
        return self._required_certificates[:]


class Instructor:
    """An instructor at a Gym.

    Each instructor may hold certificates that allows them to teach specific
    workout classes.

    === Public Attributes ===
    name: This Instructor's name.

    === Private Attributes ===
    _id: This Instructor's identifier.
    _certificates: The certificates held by this Instructor.
    """
    name: str
    _id: int
    _certificates: List[str]

    def __init__(self, instructor_id: int, instructor_name: str) -> None:
        """Initialize a new Instructor with an <instructor_id> and their
        <instructor_name>. Initially, the instructor holds no certificates.

        >>> instructor = Instructor(1, 'Matylda')
        >>> instructor.get_id()
        1
        >>> instructor.name
        'Matylda'
        """
        self.name = instructor_name
        self._id = instructor_id
        self._certificates = []

    def get_id(self) -> int:
        """Return the id of this Instructor.

        >>> instructor = Instructor(1, 'Matylda')
        >>> instructor.get_id()
        1
        """
        return self._id

    def add_certificate(self, certificate: str) -> bool:
        """Add the <certificate> to this instructor's list of certificates iff
        this instructor does not already hold the <certificate>.

        Return True iff the <certificate> was added.

        >>> instructor = Instructor(1, 'Matylda')
        >>> instructor.add_certificate('Strength Training')
        True
        >>> instructor.add_certificate('Strength Training')
        False
        """
        if certificate not in self._certificates:
            self._certificates.append(certificate)
            return True

        return False

    def get_num_certificates(self) -> int:
        """Return the number of certificates held by this instructor.

        >>> instructor = Instructor(1, 'Matylda')
        >>> instructor.add_certificate('Strength Training')
        True
        >>> instructor.get_num_certificates()
        1
        """
        return len(self._certificates)

    def can_teach(self, workout_class: WorkoutClass) -> bool:
        """Return True iff this instructor has all the required certificates to
        teach the workout_class.

        >>> matylda = Instructor(1, 'Matylda')
        >>> kickboxing = WorkoutClass('Kickboxing', ['Strength Training'])
        >>> matylda.can_teach(kickboxing)
        False
        >>> matylda.add_certificate('Strength Training')
        True
        >>> matylda.can_teach(kickboxing)
        True
        """
        req = workout_class.get_required_certificates()

        for c in req:
            if c not in self._certificates:
                return False

        return True


class Gym:
    """A gym tt hosts workout classes taught by instructors.

    All offerings of workout classes start on the hour and are 1 hour long.

    === Public Attributes ===
    name: The name of the gym.

    === Private Attributes ===
    _instructors: The roster of instructors who work at this Gym.
        Each key is an instructor's ID and its value is the Instructor object
        representing them.
    _workouts: The workout classes that are taught at this Gym.
        Each key is the name of a workout class and its value is the
        WorkoutClass object representing it.
    _rooms: The rooms in this Gym.
        Each key is the name of a room and its value is its capacity, that is,
        the number of people who can register for a class in this room.
    _schedule: The schedule of classes offered at this gym.  Each key is a date
        and time and its value is a nested dictionary describing all offerings
        that start then. Each key in the nested dictionary is the name of a room
        that has an offering scheduled then, and its value is a tuple describing
        the offering. The tuple elements record the instructor teaching the
        class, the workout class itself, and a list of registered clients. Each
        client is represented by a unique string.

    === Representation Invariants ===
    - Each key in _schedule is for a time that is on the hour.
    - No instructor is recorded as teaching two workout classes at the same
      time. (good)
    - No client is recorded as registered for two workout classes at the same
      time.
    - If an instructor is recorded as teaching a workout class, they have the
      necessary qualifications. (good)
    - If there are no offerings scheduled at date and time <d> in room <r> then
      <r> does not occur as a key in _schedule[d]
    - If there are no offerings at date and time <d> in any room at all, then
      <d> does not occur as a key in _schedule
    """
    name: str
    _instructors: Dict[int, Instructor]
    _workouts: Dict[str, WorkoutClass]
    _rooms: Dict[str, int]
    _schedule: Dict[datetime,
                    Dict[str, Tuple[Instructor, WorkoutClass, List[str]]]]

    def __init__(self, gym_name: str) -> None:
        """Initialize a new Gym with <name> that has no instructors, workout
        classes, rooms, or offerings.

        >>> ac = Gym('Athletic Centre')
        >>> ac.name
        'Athletic Centre'
        """
        self.name = gym_name
        self._instructors = {}
        self._workouts = {}
        self._rooms = {}
        self._schedule = {}

    def add_instructor(self, instructor: Instructor) -> bool:
        """Add a new <instructor> to this Gym's roster iff the <instructor>
        has not already been added to this Gym's roster.

        Return True iff the instructor was added.

        >>> ac = Gym('Athletic Centre')
        >>> diane = Instructor(1, 'Diane')
        >>> ac.add_instructor(diane)
        True
        >>> diane = Instructor(1, 'Diane')
        >>> ac.add_instructor(diane)
        False
        >>> ella = Instructor(1, 'ella')
        >>> ac.add_instructor(ella)
        False
        >>> ella2 = Instructor(2, 'Diane')
        >>> ac.add_instructor(ella2)
        True
        """
        id_i = instructor.get_id()

        if id_i not in self._instructors:
            self._instructors[id_i] = instructor
            return True

        return False

    def add_workout_class(self, workout_class: WorkoutClass) -> bool:
        """Add a <workout_class> to this Gym iff the <workout_class> has not
        already been added this Gym.

        Return True iff the workout class was added.

        >>> ac = Gym('Athletic Centre')
        >>> kickboxing = WorkoutClass('Kickboxing', ['Strength Training'])
        >>> ac.add_workout_class(kickboxing)
        True
        >>> ac.add_workout_class(kickboxing)
        False
        """
        class_name = workout_class.get_name()

        if class_name not in self._workouts:
            self._workouts[class_name] = workout_class
            return True

        return False

    def add_room(self, name: str, capacity: int) -> bool:
        """Add a room with a <name> and <capacity> to this Gym iff the room
        has not already been added to this Gym.

        Return True iff the room was added.

        >>> ac = Gym('Athletic Centre')
        >>> ac.add_room('Dance Studio', 50)
        True
        >>> ac.add_room('Dance Studio', 50)
        False
        """
        if name not in self._rooms:
            self._rooms[name] = capacity
            return True

        return False

    def schedule_workout_class(self, time_point: datetime, room_name: str,
                               workout_name: str, instr_id: int) -> bool:
        """Add an offering to this Gym at a <time_point> iff:
            - the room with <room_name> is available,
            - the instructor with <instr_id> is qualified to teach the workout
              class with <workout_name>, and
            - the instructor is not teaching another workout class during the
              same <time_point>.
        A room is available iff it does not already have another workout class
        scheduled at that date and time.

        The added offering should start with no registered clients.

        Return True iff the offering was added.

        Preconditions:
            - The room has already been added to this Gym.
            - The Instructor has already been added to this Gym.
            - The WorkoutClass has already been added to this Gym.

        >>> ac = Gym('Athletic Centre')
        >>> diane = Instructor(1, 'Diane')
        >>> ac.add_instructor(diane)
        True
        >>> diane.add_certificate('Cardio 1')
        True
        >>> ac.add_room('Dance Studio', 50)
        True
        >>> boot_camp = WorkoutClass('Boot Camp', ['Cardio 1'])
        >>> ac.add_workout_class(boot_camp)
        True
        >>> sep_9_2019_12_00 = datetime(2019, 9, 9, 12, 0)
        >>> ac.schedule_workout_class(sep_9_2019_12_00, 'Dance Studio',\
        boot_camp.get_name(), diane.get_id())
        True
        """

        not_in = False
        if time_point not in self._schedule:
            self._schedule[time_point] = {}
            not_in = True

        room_avail = self._room_available(time_point, room_name)
        instructor_qual = self._instructors[instr_id].can_teach(
            self._workouts[workout_name])
        instructor_avail = self._instructor_available(time_point, instr_id)

        if room_avail and instructor_qual and instructor_avail:
            # self._schedule[time_point] is at least {}
            self._schedule[time_point].update(
                {room_name: (self._instructors[instr_id],
                             self._workouts[workout_name], [])})

            return True

        if not_in:
            del self._schedule[time_point]

        return False

    def _room_available(self, time: datetime, name_room: str) -> bool:
        """
        Return True iff the room with <name_room> is available at time <time>.

        A room is available iff it does not already have another workout class
        scheduled at that date and time.

        Preconditions:
        1. The room has already been added to this Gym.
        2. <time> is in _schedule

        >>> ac = Gym('Athletic Centre')
        >>> diane = Instructor(1, 'Diane')
        >>> ac.add_instructor(diane)
        True
        >>> diane.add_certificate('Cardio 1')
        True
        >>> ac.add_room('Dance Studio', 50)
        True
        >>> boot_camp = WorkoutClass('Boot Camp', ['Cardio 1'])
        >>> ac.add_workout_class(boot_camp)
        True
        >>> sep_9_2019_12_00 = datetime(2019, 9, 9, 12, 0)
        >>> ac.schedule_workout_class(sep_9_2019_12_00, 'Dance Studio',\
        boot_camp.get_name(), diane.get_id())
        True
        >>> ac._room_available(sep_9_2019_12_00, "Dance Studio")
        False

        """
        list_names = self._schedule[time].keys()  # List[str] of room names
        if name_room in list_names:
            return False

        return True

    def _instructor_available(self, time: datetime, ins_id: int) -> bool:
        """
        Return True iff Instructor with <ins_id> is available at time <time>.

        Instructor is available if at time <time>
        they are not teaching in any of the rooms.

        Preconditions:
        1. The Instructor has already been added to this Gym.
        2. <time> is in _schedule.

        >>> ac = Gym('Athletic Centre')
        >>> diane = Instructor(1, 'Diane')
        >>> ac.add_instructor(diane)
        True
        >>> diane.add_certificate('Cardio 1')
        True
        >>> ac.add_room('Dance Studio', 50)
        True
        >>> boot_camp = WorkoutClass('Boot Camp', ['Cardio 1'])
        >>> ac.add_workout_class(boot_camp)
        True
        >>> sep_9_2019_12_00 = datetime(2019, 9, 9, 12, 0)
        >>> ac.schedule_workout_class(sep_9_2019_12_00, 'Dance Studio',\
        boot_camp.get_name(), diane.get_id())
        True
        >>> ac._instructor_available(sep_9_2019_12_00, 1)
        False
        """

        list_tups = self._schedule[time].values()  # List[Tuple]

        for t in list_tups:
            if ins_id == t[0].get_id():  # id of instructor (it is unique)
                return False

        return True

    def register(self, time_point: datetime, client: str, workout_name: str) \
            -> bool:
        """Add <client> to the WorkoutClass with <workout_name> that is being
        offered at <time_point> iff the client has not already been registered
        in any course (including <workout_name>) at <time_point>, and the room
        is not full.

        If the WorkoutClass is being offered in more than one room at
        <time_point>, then the client is added to any one of the rooms (i.e.,
        the room chosen does not matter).

        Return True iff the client was added.

        Precondition: the WorkoutClass with <workout_name> is being offered in
            some room at <time_point>. (<time_point> exists in self._schedule)

        >>> ac = Gym('Athletic Centre')
        >>> diane = Instructor(1, 'Diane')
        >>> diane.add_certificate('Cardio 1')
        True
        >>> ac.add_instructor(diane)
        True
        >>> ac.add_room('Dance Studio', 50)
        True
        >>> boot_camp = WorkoutClass('Boot Camp', ['Cardio 1'])
        >>> ac.add_workout_class(boot_camp)
        True
        >>> sep_9_2019_12_00 = datetime(2019, 9, 9, 12, 0)
        >>> ac.schedule_workout_class(sep_9_2019_12_00, 'Dance Studio',\
        boot_camp.get_name(), diane.get_id())
        True
        >>> ac.register(sep_9_2019_12_00, 'Philip', 'Boot Camp')
        True
        >>> ac.register(sep_9_2019_12_00, 'Philip', 'Boot Camp')
        False
        """

        not_full_rooms = []

        for room in self._list_of_rooms(time_point, workout_name):
            if self._room_not_full(time_point, room):
                not_full_rooms.append(room)

        if self._client_not_registered(time_point, client) and \
                (len(not_full_rooms) != 0):

            self._schedule[time_point][not_full_rooms[0]][2].append(
                client)
            return True

        return False

    def _list_of_rooms(self, time: datetime, name_workout: str) -> List[str]:
        """Return a list of the names of rooms that Workout with name
        <name_workout> is offered in at time <time>.

        Precondition: the WorkoutClass with <workout_name> is being offered in
        some room at <time_point>.

        >>> ac = Gym('Athletic Centre')
        >>> diane = Instructor(1, 'Diane')
        >>> diane.add_certificate('Cardio 1')
        True
        >>> ac.add_instructor(diane)
        True
        >>> ac.add_room('Dance Studio', 50)
        True
        >>> boot_camp = WorkoutClass('Boot Camp', ['Cardio 1'])
        >>> ac.add_workout_class(boot_camp)
        True
        >>> sep_9_2019_12_00 = datetime(2019, 9, 9, 12, 0)
        >>> ac.schedule_workout_class(sep_9_2019_12_00, 'Dance Studio',\
        boot_camp.get_name(), diane.get_id())
        True
        >>> ac._list_of_rooms(sep_9_2019_12_00,boot_camp.get_name())
        ['Dance Studio']
        """
        lst_rooms = []

        dictionary = self._schedule[time]  # accesses nested dictionary
        for room in dictionary:  # iterates through each room
            if dictionary[room][1].get_name() == name_workout:  # Workout name
                lst_rooms.append(room)

        return lst_rooms

    def _client_not_registered(self, time: datetime, client_name: str) -> bool:
        """Return True iff client with <client_name> is not registered
        in any workout classes at time <time>.

        Note:  Each client is represented by a unique string.
        Precondition: <time> is in _schedule

        >>> ac = Gym('Athletic Centre')
        >>> diane = Instructor(1, 'Diane')
        >>> diane.add_certificate('Cardio 1')
        True
        >>> ac.add_instructor(diane)
        True
        >>> ac.add_room('Dance Studio', 50)
        True
        >>> boot_camp = WorkoutClass('Boot Camp', ['Cardio 1'])
        >>> ac.add_workout_class(boot_camp)
        True
        >>> sep_9_2019_12_00 = datetime(2019, 9, 9, 12, 0)
        >>> ac.schedule_workout_class(sep_9_2019_12_00, 'Dance Studio',\
        boot_camp.get_name(), diane.get_id())
        True
        >>> ac._client_not_registered(sep_9_2019_12_00, "Philip")
        True
        >>> ac.register(sep_9_2019_12_00, 'Philip', 'Boot Camp')
        True
        >>> ac._client_not_registered(sep_9_2019_12_00, "Philip")
        False
        """
        list_tups = self._schedule[time].values()
        for t in list_tups:
            if client_name in t[2]:  # t[2] is a list of client names
                return False

        return True

    def _room_not_full(self, time: datetime, r_name: str) -> bool:
        """Return True iff room with <r_name> is not full (under capacity) at
        time <time>.

        Precondition: <time> is in _schedule

        >>> ac = Gym('Athletic Centre')
        >>> diane = Instructor(1, 'Diane')
        >>> diane.add_certificate('Cardio 1')
        True
        >>> ac.add_instructor(diane)
        True
        >>> ac.add_room('Dance Studio', 1)
        True
        >>> boot_camp = WorkoutClass('Boot Camp', ['Cardio 1'])
        >>> ac.add_workout_class(boot_camp)
        True
        >>> sep_9_2019_12_00 = datetime(2019, 9, 9, 12, 0)
        >>> ac.schedule_workout_class(sep_9_2019_12_00, 'Dance Studio',\
        boot_camp.get_name(), diane.get_id())
        True
        >>> ac._room_not_full(sep_9_2019_12_00, 'Dance Studio')
        True
        >>> ac.register(sep_9_2019_12_00, 'Philip', 'Boot Camp')
        True
        >>> ac._room_not_full(sep_9_2019_12_00, 'Dance Studio')
        False
        """
        list_clients = self._schedule[time][r_name][2]  # List[str] of clients
        capacity = self._rooms[r_name]
        return len(list_clients) < capacity

    def offerings_at(self, time_point: datetime) -> List[Tuple[str, str, str]]:
        """Return all the offerings that start at <time_point>.

        Return a list of 3-element tuples containing: the instructor's name, the
        workout class's name, and the room's name. If there are no offerings at
        <time_point>, return an empty list.

        The order of the elements in the returned list does not matter.

        >>> ac = Gym('Athletic Centre')
        >>> diane = Instructor(1, 'Diane')
        >>> diane.add_certificate('Cardio 1')
        True
        >>> ac.add_instructor(diane)
        True
        >>> ac.add_room('Dance Studio', 50)
        True
        >>> boot_camp = WorkoutClass('Boot Camp', ['Cardio 1'])
        >>> ac.add_workout_class(boot_camp)
        True
        >>> t1 = datetime(2019, 9, 9, 12, 0)
        >>> ac.schedule_workout_class(t1, 'Dance Studio',\
        boot_camp.get_name(), diane.get_id())
        True
        >>> ('Diane', 'Boot Camp', 'Dance Studio') in ac.offerings_at(t1)
        True
        """

        if time_point not in self._schedule:
            return []

        else:  # time_point is in self._schedule
            lst_tuple = []
            dictionary = self._schedule[time_point]

            for room in dictionary:  # each room in dictionary at <time_point>
                instructor_name = dictionary[room][0].name
                workout_name = dictionary[room][1].get_name()
                lst_tuple.append((instructor_name, workout_name, room))

            return lst_tuple

    def instructor_hours(self, time1: datetime, time2: datetime) -> \
            Dict[int, int]:
        """Return a dictionary reporting the hours worked by instructors
        between <time1> and <time2>, inclusive.

        Each key is an instructor ID and its value is the total number of hours
        worked by that instructor between <time1> and <time2> inclusive. Both
        <time1> and <time2> specify the start time for an hour when an
        instructor may have taught.

        Precondition: time1 < time2

        >>> ac = Gym('Athletic Centre')
        >>> diane = Instructor(1, 'Diane')
        >>> david = Instructor(2, 'David')
        >>> diane.add_certificate('Cardio 1')
        True
        >>> ac.add_instructor(diane)
        True
        >>> ac.add_instructor(david)
        True
        >>> ac.add_room('Dance Studio', 50)
        True
        >>> boot_camp = WorkoutClass('Boot Camp', ['Cardio 1'])
        >>> ac.add_workout_class(boot_camp)
        True
        >>> t1 = datetime(2019, 9, 9, 12, 0)
        >>> ac.schedule_workout_class(t1, 'Dance Studio', boot_camp.get_name(),
        ... 1)
        True
        >>> t2 = datetime(2019, 9, 10, 12, 0)
        >>> ac.instructor_hours(t1, t2) == {1: 1, 2: 0}
        True
        """

        hours_dict = {}

        # not recording those who don't work
        for t in self._schedule:
            if time1 <= t <= time2:
                instructor_ids = self._list_of_instructor_ids(t)

                _update_dictionary(hours_dict, instructor_ids)

        for i in self._instructors:
            if i not in hours_dict:
                hours_dict[i] = 0

        return hours_dict

    def _list_of_instructor_ids(self, time: datetime) -> List[int]:
        """Return a list of the ids of instructors who are teaching at time
        <time>.

        Precondition: <time> is in _schedule

        >>> ac = Gym('Athletic Centre')
        >>> diane = Instructor(1, 'Diane')
        >>> diane.add_certificate('Cardio 1')
        True
        >>> ac.add_instructor(diane)
        True
        >>> ac.add_room('Dance Studio', 1)
        True
        >>> boot_camp = WorkoutClass('Boot Camp', ['Cardio 1'])
        >>> ac.add_workout_class(boot_camp)
        True
        >>> sep_9_2019_12_00 = datetime(2019, 9, 9, 12, 0)
        >>> ac.schedule_workout_class(sep_9_2019_12_00, 'Dance Studio',\
        boot_camp.get_name(), diane.get_id())
        True
        >>> ac._list_of_instructor_ids(sep_9_2019_12_00)
        [1]
        """
        list_of_ids = []
        dictionary = self._schedule[time]
        for room in dictionary:  # each room in dictionary
            instructor_id = dictionary[room][0].get_id()
            list_of_ids.append(instructor_id)

        return list_of_ids

    def payroll(self, time1: datetime, time2: datetime, base_rate: float) \
            -> List[Tuple[int, str, int, float]]:
        """Return a sorted list of tuples reporting the total wages earned by
        instructors between <time1> and <time2>, inclusive.

        Each tuple contains 4 elements, in this order:
            - the instructor's ID,
            - the instructor's name,
            - the number of hours worked by the instructor between <time1>
              and <time2> inclusive, and
            - the instructor's total wages earned between <time1> and <time2>
              inclusive.
        The list is sorted by instructor ID.

        Both <time1> and <time2> specify the start time for an hour when an
        instructor may have taught.

        Each instructor earns a <base_rate> per hour plus an additional
        BONUS_RATE per hour for each certificate they hold.

        Precondition: time1 < time2

        >>> ac = Gym('Athletic Centre')
        >>> diane = Instructor(1, 'Diane')
        >>> david = Instructor(2, 'David')
        >>> diane.add_certificate('Cardio 1')
        True
        >>> ac.add_instructor(diane)
        True
        >>> ac.add_instructor(david)
        True
        >>> ac.add_room('Dance Studio', 50)
        True
        >>> boot_camp = WorkoutClass('Boot Camp', ['Cardio 1'])
        >>> ac.add_workout_class(boot_camp)
        True
        >>> t1 = datetime(2019, 9, 9, 12, 0)
        >>> ac.schedule_workout_class(t1, 'Dance Studio', boot_camp.get_name(),
        ... 1)
        True
        >>> t2 = datetime(2019, 9, 10, 12, 0)
        >>> ac.payroll(t1, t2, 25.0)
        [(1, 'Diane', 1, 26.5), (2, 'David', 0, 0.0)]
        """

        lst_tup = []
        # instructor's id is in _instructor
        dict_id_hours = self.instructor_hours(time1, time2)

        for id_dict in dict_id_hours:
            id_tup = id_dict
            hours_tup = dict_id_hours[id_dict]
            name_tup = self._instructors[id_tup].name
            certificate_num = self._instructors[id_tup].get_num_certificates()
            pay_tup = hours_tup * (base_rate + certificate_num * BONUS_RATE)

            lst_tup.append((id_tup, name_tup, hours_tup, pay_tup))

        lst_tup.sort()

        return lst_tup


def _update_dictionary(d: Dict[int, int], id_list: List[int]) -> None:
    """Update dictionary <d> by first creating a new key for each number in
    <id_list> (if the key doesn't exist already) and setting its value to 0.
    Then, update <d> by adding 1 to each key's value.

    >>> lst = [1,2]
    >>> d = {}

    >>> _update_dictionary(d, lst)
    >>> d
    {1: 1, 2: 1}

    """
    for ins_id in id_list:  # for each id in list
        if ins_id not in d:
            d[ins_id] = 0
        d[ins_id] = d[ins_id] + 1


def parse_instructor(file: TextIO, header: str) -> Instructor:
    """Return a new Instructor based on the data found in the file and the
    header.

    Precondition: header has the format 'Instructor <ID> <Full Name>'
    """
    # Extract instructor information from the header
    header_elements = header.split()
    instr_id = int(header_elements[1].strip())
    name = ' '.join(header_elements[2:])

    # Create a new instructor object.
    instr = Instructor(instr_id, name)

    # Add any certificates that the instructor holds.
    line = file.readline().strip()
    while line != '':
        certificate = line.strip()
        instr.add_certificate(certificate)

        line = file.readline().strip()

    return instr


def parse_workout_class(file: TextIO, header: str) -> WorkoutClass:
    """Return a new WorkoutClass based on the data found in the file and the
    header.

    Precondition: header has the format 'Class <Workout Class Name>'
    """
    name = header.replace('Class', '').strip()

    required_certificates = []
    line = file.readline().strip()
    while line != '':
        required_certificates.append(line.strip())

        line = file.readline().strip()

    return WorkoutClass(name, required_certificates)


def parse_room(file: TextIO, header: str) -> Tuple[str, int]:
    """Return a new Room based on the data found in the file and the header.

    Precondition: header has the format 'Room <Room Name>'
    """
    room_name = header.split()[1].strip()

    # Ignore the full name.
    file.readline()
    # Parse the capacity.
    capacity = int(file.readline().strip())

    return room_name, capacity


def parse_offerings(file: TextIO, header: str) -> \
        Tuple[datetime, List[Tuple[int, str, str]]]:
    """Return a tuple where the first element is a datetime for when the
    offerings are scheduled. The second element is a list of all offerings.
    Each offering is a tuple with three elements: the instructor ID, the
    workout class name, and the room name in that order.

    Precondition: header has the format 'Offerings <Date and Time>', where the
    date and time are in the following format: %Y-%m-%d %H:%M
    """
    date_time = header.replace('Offerings', '').strip()
    when = datetime.strptime(date_time, '%Y-%m-%d %H:%M')

    offerings = []
    line = file.readline().strip()
    while line != '':
        elements = line.split(sep=',')

        instr_id = int(elements[0].strip())
        workout_name = elements[1].strip()
        room_id = elements[2].strip()
        offerings.append((instr_id, workout_name, room_id))

        line = file.readline().strip()

    return when, offerings


def parse_registrations(file: TextIO, header: str) -> \
        Tuple[datetime, List[Tuple[str, str]]]:
    """Return a tuple where the first element is a datetime for the offering
    being registered for. The second element is a list of tuples where, for each
    tuple, the first element is the name of the client and the second element is
    the name of the workout class the client is registering for.

    Precondition: header has the format 'Registrations <Date and Time>', where
    the date and time are in the following format: %Y-%m-%d %H:%M
    """
    date_time = header.replace('Registrations', '').strip()
    when = datetime.strptime(date_time, '%Y-%m-%d %H:%M')

    registrations = []
    line = file.readline().strip()
    while line != '':
        elements = line.split(sep=',')

        name = elements[0].strip()
        workout_class = elements[1].strip()
        registrations.append((name, workout_class))

        line = file.readline().strip()

    return when, registrations


def load_data(file_name: str, gym_name: str) -> Gym:
    """Return a new Gym based on the contents of the file being read.

    Precondition: Assumes that the file <file_name> exists and can be read.
    """
    new_gym = Gym(gym_name)

    with open(file_name, 'r') as f:
        line = f.readline().strip()

        while line != '':
            if line.startswith('Instructor'):
                instr = parse_instructor(f, line)
                new_gym.add_instructor(instr)
            elif line.startswith('Class'):
                workout_class = parse_workout_class(f, line)
                new_gym.add_workout_class(workout_class)
            elif line.startswith('Room'):
                room_name, room_capacity = parse_room(f, line)
                new_gym.add_room(room_name, room_capacity)

                # ignore the next line
                f.readline()
            elif line.startswith('Offerings'):
                when, offerings = parse_offerings(f, line)

                for o in offerings:
                    new_gym.schedule_workout_class(when, o[2], o[1], o[0])
            elif line.startswith('Registrations'):
                when, registrations = parse_registrations(f, line)

                for r in registrations:
                    new_gym.register(when, r[0], r[1])

            line = f.readline().strip()

    return new_gym


if __name__ == '__main__':
    ac = Gym('Athletic Centre')
    diane = Instructor(1, 'Diane')
    ac.add_instructor(diane)
    diane.add_certificate('Cardio 1')
    ac.add_room('Dance Studio', 50)
    boot_camp = WorkoutClass('Boot Camp', ['Cardio 1'])
    ac.add_workout_class(boot_camp)
    sep_9_2019_12_00 = datetime(2019, 9, 9, 12, 0)
    ac.schedule_workout_class(sep_9_2019_12_00, 'Dance Studio',
                                     boot_camp.get_name(), diane.get_id())

    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['load_data'],
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'datetime'],
        'max-attributes': 15,
    })

    import doctest

    doctest.testmod()

    # ac = load_data('athletic-centre.txt', 'Athletic Centre'
