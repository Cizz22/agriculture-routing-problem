
"""Main file for the project."""


from arpga.core import run_arpga


def main():
    ''''main()'''

    result = run_arpga(
        track=20,
        width=2.5,
        radius=3.5,
        maxGen=200,
        pSize=100,
        runNumbers=10
    )

    print(result)
    
main()
