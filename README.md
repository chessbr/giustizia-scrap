# Giustizia Civile Scrapper

Project that scans for italian citizenship judicial processes in Giustizia Civile from Rome court.

## Usage

Clone this repo and configure `secrets.py` file with values intercepted from Giustizia Civile mobile app.


- *UUID* - This is the UUID of the installation of the app
- *devicename* - This is the device name
- *devicewidth* - This is the device screen width
- *deviceheight* - This is the device screen height
- *token* - This is some weird hash token

To get these values, you'll need to intercept them from your mobile app.
Install the app from app store. Then install a Man-in-the-middle proxy in your computer.
We recommend the free one: https://mitmproxy.org/.

After getting the values and putting them in the secrets file, open the `scrapper.py` and adjust the scan range: 

- *INITIAL_ID* - from what process number to start the search
- *FINAL_ID* - the last process number to search
- *RANGE_YEAR* - the year of process ranges to search

:warning: You can also reduce the sleep time to something about 2 seconds, but some test cases with lower than 1s was getting requests throttled, so be careful.

Save and execute: `python screapper.py` and watch the magic. A local file will be written with the results.

## Notes

Attention: Do not overload Giustizia Civile servers to prevent blocking your UUID/token/IP and maybe also removing the API from the users.
Do not use this code for maliscious purposes.

Enjoy!

## License

MIT
