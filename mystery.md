# Mystery Feature
Create a comparison feature to compare data points within one data set.

Functions may still include minimum, maximum, average, and single point.
You may assume the function is the same between comparison points A and B (we won’t ask to get a minimum and maximum in the same question).

Example data (from the original rules)
```
date: 2024-04-24 2024-04-25 2024-04-26 2024-04-27 2024-04-28 2024-04-29
weather_code: 3.0 61.0 3.0 55.0 3.0 63.0
temperature_max: 54.9464 52.6064 61.9664 52.2464 52.6064 48.4664
temperature_min: 44.2364 47.1164 48.6464 47.9264 42.796402 40.0064
precipitation_sum: 0.0 0.22440945 0.0 0.1456693 0.0 0.2952756
wind_speed_max: 9.309791 10.116089 8.249648 10.711936 13.588738 7.4495792
precipitation_probability_max: 45.0 100.0 100.0 100.0 97.0 100.0
```

Example questions for the given data:
- “Compare the `wind_speed_max` between 2024-04-24 and 2024-04-25”
    - The `wind_speed_max` on 2024-04-24 was 9.31 mph, which was less than `wind_speed_max` on 2024-04-25.
- “Compare the average `temperature_max` over days 0 through 2 against the average `temperature_max` over days 3 through 5.”
    - The average between days 0 through 2 was 56.51 degrees Fahrenheit, which was greater than the 51.11 degrees Fahrenheit of days 3 through 5.
- “Compare the minimum `precipitation_probability_max` over the first 3 days with the minimum `precipitation_probability_max` over the last 3 days.”
    - The minimum `precipitation_probability_max` is 45% in the first 3 days, which is less than the minimum of 97% in the last 3 days.
