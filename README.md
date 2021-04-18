`merge_csvs` is a small script to merge a bunch of csv files inside a zip file.
It checks that the csvs actually contain the same headers and skip files that
are not csv.


## Running the script
Quite easy
```
(venv)$> python merge_csvs some-zip-file-with-at-least-two-similar-csvs.zip
```


## Installing the dependencies
Also easy, just create a virtual environment in the way you like the most.
```
$> python3 -m venv venv
$> source venv/bin/activate
$> pip install --upgrade pip
$> pip install -r requirements.txt
```


## Running the tests
If you run the tests be sure to add the `-b` flag to avoid stdout prints
```
(venv)$> python3 tests.py -b
```
