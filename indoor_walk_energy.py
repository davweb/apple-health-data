"""Extract and print the energy burned during indoor walks from an Apple Health export XML file."""
from typing import Iterator
import xml.etree.ElementTree as et


def extract_workouts() -> Iterator[et.Element]:
    """Read the Apple Health export XML file and extract workout data from the
    <Workout> elements using a streaming parser."""

    with open('export.xml', encoding='utf-8') as f:
        for event, element in et.iterparse(f, events=('start', 'end')):
            if event == 'end' and element.tag == 'Workout':
                yield element
                element.clear()
            elif event == 'end' and element.tag == 'Record':
                element.clear()

def main() -> None:
    """Extract and print the energy burned during indoor walks"""
    for workout in extract_workouts():

        if workout.attrib['workoutActivityType'] != 'HKWorkoutActivityTypeWalking':
            continue

        indoor_workout = workout.find("MetadataEntry[@key='HKIndoorWorkout']")

        if indoor_workout is None or indoor_workout.attrib['value'] != '1':
            continue

        stats = workout.find("WorkoutStatistics[@type='HKQuantityTypeIdentifierActiveEnergyBurned']")

        if stats is None:
            continue

        energy_burned_unit = stats.attrib['unit']

        if energy_burned_unit != 'kcal':
            continue

        energy_burned = stats.attrib['sum']
        start_date = stats.attrib['startDate'].replace(" +0000", "")
        end_date = stats.attrib['endDate'].replace(" +0000", "")

        print(f'{start_date},{end_date},{energy_burned}')


if __name__ == '__main__':
    main()
