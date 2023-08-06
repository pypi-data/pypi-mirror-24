=====================
gtmanipulator Package
=====================
**Contents:**

- gtmanipulator source code
- Gt GUI source code (windowed and non-windowed versions)
- Sample data
- Unit tests

**Installation:**

    Using pip: pip install gtmanipulator

    Using setup.py:

        1. Download the github repository: gtmanipulator_
        2. Extract the repository form the zip file
        3. Navigate to the directory containing the setup.py file
        4. pip install .

===
API
===
Use:
----

::

    # Importing and summarizing
    import gtmanipulator at gt
    data = "some_data_file.csv"
    manipulator = gt.GtManipulator(data)
    summarizedDf = manipulator.summarize()
    print(summarizedDf.head())

    # Calculating allelic frequencies
    freqDf = manipulator.calc_frequencies(missing={"??"})
    print(freqDf)

    # Setting definitions of morphisms and predicting morphisms
    morphedDf = manipulator.predict_morphisms(failed=0.20, mono=0.80, 
                                              poly={"Type 1": (0.80, 0.20, 0.10),
                                                    "Type 2": (0.80, 0.10, 0.20),
                                                    "Type 3": (0.10, 0.10, 0.10)},
                                              comp_ops={"Type 1": ("<", ">", "<="),
                                                        "Type 2": ("<", "<=", ">"),
                                                        "Type 3": (">", ">", ">")})
    print(morphedDf)

    # Saving 
    manipulator.save("some_file.csv")

    # Transposing
    manipulator.transpose()

===
GUI
===
Use:
----
    In order to run the Gt Gui you must first have properly installed the
    gtmanipulator package. You may then run the GUI with or without a console.
    To run without a console simply double-click on the gtgui.pyw file. To 
    get the GUI files download the gtmanipulator_ repository and extract the zip
    file. Then navigate to the gtgui directory where the gtgui.py and gtgui.pyw
    files can be found.

=====
Notes
=====
Additional documentation and instructions can be found in the docstrings of the
API or in the tooltips within the GUI.

For any other questions email: travis.m.couture@gmail.com

.. _gtmanipulator: https://github.com/TravisCouture/gtmanipulator
   