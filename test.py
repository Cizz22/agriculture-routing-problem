"""Test file for the project."""

from arpga.core import run_arpga

def main():
    """Test function for the project."""
    track = 20
    width = 2.5
    radius = 3.5
    maxGen = 40*track
    pSize = 20 * track
    runnumbers = 10

    best_fitness, best_solution = run_arpga(
        track=track,
        width=width,
        radius=radius,
        maxGen=maxGen,
        pSize=pSize,
        runNumbers=runnumbers
    )

    print(best_fitness)
    print(best_solution)

if __name__ == "__main__":
    main()