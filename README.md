# Trip-analysis

## Prerequisite and how to run
1. Runtime: Python 3.9.6
2. Clone the repo and open terminal/powershell in the repo folder, then run the following command to install dependencies:
3. `pip install -r requirements.txt`
4. Put/create the "EOL-dump" directory in the repo folder with vehicle trails in it.
5. To start the app, run via Python: `python app.py`
6. You can test the API on http://127.0.0.1:5000/api with data={'input_time1':<value>, 'input_time2':<value>} or 
with webpage UI at the URL http://127.0.0.1:5000
NOTE: If the API gives Distance and Average speed as "O" or "None" for a vehicle in a given time interval, it means those
details are missing in the CSV file of that vehicle in the given interval.

## Test Via UI 
![Test via UI](https://github.com/wasiongit/trip-analysis/assets/84765303/b0100358-e14e-4064-a6fd-14972e7a5526)

## Sample Output
![sample output](https://github.com/wasiongit/trip-analysis/assets/84765303/dad54891-7921-47fe-8b52-438a4107fb15)



