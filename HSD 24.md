# hsd24_students
Hello students! Here are some more resources to help you test your projects.

## Submit Your Project

At the end of the hackathon, please submit your project in a zip file using the following link:

[Submit your project here](https://docs.google.com/forms/d/e/1FAIpQLSdDeUM_tIDU84ZTwUOClVqSPWCacBoT2BiJOopBfuEB4K4Etg/viewform?usp=sf_link)

## test solutions

### wichita.txt

There are 15 days stored in this file, try to make your answers match!

#### core features

Q: What is the maximum `temperature_max` of days 0-9?
A: 91.2389 degrees Fahrenheit

Q: What is the average `wind_speed_max` of all days?
A: 12.0593 mph

Q: What was the max `precipitation_probability_max` on day 4?
A: 8.0%

Q: What was the highest weather code between days 10 and 14?
A: 3.0 (or "Overcast")

#### small extra feature

For the next example questions, the data was obtained online with the parameters in the API link below:
https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&daily=temperature_2m_max&temperature_unit=fahrenheit&timezone=America%2FLos_Angeles&start_date=2024-10-04&end_date=2024-10-17

An easier-to-read version of the parameters on the actual page can be found [here](https://open-meteo.com/en/docs#hourly=&daily=temperature_2m_max&temperature_unit=fahrenheit&timezone=America%2FLos_Angeles&past_days=7&start_date=2024-10-04&end_date=2024-10-17&time_mode=time_interval)

Part of the response looks like this:
```
"temperature_2m_max":[56.7,56.2,54.3,59.3,69.6,67.8,63.7,55.5,56.1,52.7,53.0,53.6,57.0,62.2]
```

Q: Compare the `temperature_max` on day 0 (2024-10-04) against the `temperature_max` on the same day at 13.41 degrees latitude 52.52 degrees longitude.
A: (something akin to) The given max temperature of 83.0 is greater than the max temperature of 56.7 found at 13.41 degrees latitude 52.52 degrees longitude.

Q: Compare the maximum `temperature_max` between days 0 and 5 against the same days at 13.41 degrees latitude 52.52 degrees longitude.
A: The given maximum `temperature_max` of 91.2389 is greater than the maximum `temperature_max` of 69.6 found at 13.41 degrees latitude 52.52 degrees longitude.

#### medium extra feature

When drawing the histogram, please be sure to include:
- day labels ("day 0" or "2024-10-04" for example)
- axis labels

Q: Create a histogram of `temperature_min` between days 0 and 7.
A: \*insert histogram here\* (be sure to include axis and day labels!)

Q: Create a histogram of `wind_speed_max` between days 0 and 14.
A: \*insert histogram here\*

#### large extra feature

Q: Add a new day to the `wichita.txt` data, with the following values: (POST)
- contestants may have a different format to this POST, as long as the values are retained
```json
{
    "date": ["2024-10-19"],
    "weather_code": [3.0],
    "temperature_max": [79.4],
    "temperature_min": [57.3],
    "precipitation_sum": [0.0],
    "wind_speed_max": [14.0],
    "precipitation_probability_max": [0.0],
}
```
A: \*insert contestant-proposed response here\*

After the previous question,
Q: What was the `temperature_max` and `temperature_min` on day 15 (2024-10-19)? (GET)
- contestants may propose the format, as long as it is testable with an HTTP response. A suggested testing page would be [reqbin](https://reqbin.com/)
A: \*insert contestant-proposed response here\*
Example response from `wichita.txt`:
```json
{
    "date": ["2024-10-19"],
    "temperature_max": [79.4],
    "temperature_min": [57.3]
}
```

Then,
Q: Change the `temperature_min` on day 15 to 59.0 (PUT). Then get it with another GET request.
A: \*insert contestant-proposed response here\*
Example response from `wichita.txt`:
```json
{
    "date": ["2024-10-19"],
    "temperature_max": [79.4],
    "temperature_min": [59.0]
}
```

Finally,
Q: Delete day 15 from the data (DELETE). Then try to get it with another GET request.
A: \*insert contestant-proposed response here\*
Example response from `wichita.txt`:
```json
{
    "error": "Day 15 not found."
}
```
