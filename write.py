"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json
import helpers


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = (
        "datetime_utc",
        "distance_au",
        "velocity_km_s",
        "designation",
        "name",
        "diameter_km",
        "potentially_hazardous",
    )
    # TODO: Write the results to a CSV file, following the specification in the instructions.
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerow(fieldnames)
        for o in results:
            name = o.neo.name if o.neo.name is not None else ""
            dia = o.neo.diameter if o.neo.diameter == o.neo.diameter else ""
            line = (
                o.time,
                o.distance,
                o.velocity,
                o._designation,
                name,
                dia,
                o.neo.hazardous,
            )
            writer.writerow(line)


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    # TODO: Write the results to a JSON file, following the specification in the instructions.
    with open(filename, "w") as f:
        if len(results) == 0:
            json.dump([], f)
        else:
            top_lvl_list = []
            for o in results:
                neo_dict = {}
                neo_dict["designation"] = o.neo.designation
                neo_dict["name"] = o.neo.name if o.neo.name is not None else ""
                neo_dict[
                    "diameter_km"
                ] = o.neo.diameter  # if o.neo.diameter==o.neo.diameter else json.NaN
                neo_dict["potentially_hazardous"] = True if o.neo.hazardous else False
                obj_dict = {}
                obj_dict["datetime_utc"] = helpers.datetime_to_str(o.time)
                obj_dict["distance_au"] = o.distance
                obj_dict["velocity_km_s"] = o.velocity
                obj_dict["neo"] = neo_dict
                top_lvl_list.append(obj_dict)
            json.dump(top_lvl_list, f)
