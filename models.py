"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, designation, **info):
        """Create a new `NearEarthObject`.

        :param pdes: primary designation (required, unique)
        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        # designation is the "ID" of this object so only the intended use is permitted
        self.designation = designation
        assert isinstance(self.designation, str)

        # name and diameter are less important so I can cast them
        self.name = info["name"] if "name" in info.keys() else None
        self.diameter = (
            float(info["diameter"]
                  ) if "diameter" in info.keys() else float("nan")
        )
        self.hazardous = info["hazardous"] if "hazardous" in info.keys(
        ) else False

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return (
            self.designation + ", " + self.name
            if self.name is not None
            else self.designation
        )

    def __str__(self):
        """Return `str(self)`."""
        text = f"A NearEarthObject with designation {self.designation}."
        if self.name is not None:
            text += f" It's name is {self.name}"
        # check that diameter is not "nan"
        if self.diameter == self.diameter:
            text += f" It has a diameter of {self.diameter}m."
        if self.hazardous:
            text += " It is endangering us all!"
        else:
            text += " It is harmless."
        return text

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (
            f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
            f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"
        )


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, designation, time, **info):
        """Create a new `CloseApproach`.

        :param designation: Designation of CloseApproach as a string
        :param time: A calendar date in YYYY-bb-DD hh:mm format
        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self._designation = designation
        self.time = cd_to_datetime(time)
        self.distance = float(
            info["distance"]) if "distance" in info.keys() else 0.0
        self.velocity = float(
            info["velocity"]) if "velocity" in info.keys() else 0.0

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        text = (
            f"A CloseApproach of {self._designation} that happened on {self.time_str}."
        )
        if self.velocity > 0.0:
            text += f" The velocity was {self.velocity}"
        if self.distance > 0.0:
            text += f" The distance was {self.distance}"
        return text

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (
            f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
            f"velocity={self.velocity:.2f}, neo={self.neo!r})"
        )
