# import pendulum

# timezones = {
#     "Egypt": "Africa/Cairo",
#     "US (San Francisco)": "America/Los_Angeles",
#     "Lebanon": "Asia/Beirut",
# }

# for location, tz in timezones.items():
#     now = pendulum.now(tz)
#     print(f"{location}: {now.to_datetime_string()} ({now.format('dddd, MMMM D, YYYY')})")

import pendulum

for name, tz in {
    "Egypt": "Africa/Cairo",
    "US (San Francisco)": "America/Los_Angeles",
    "Lebanon": "Asia/Beirut",
    "India": "Asia/Kolkata",
}.items():
    now = pendulum.now(tz)
    print(
        f"{name:20} "
        f"{now.format('YYYY-MM-DD HH:mm:ss')} "
        f"{now.format('ZZ')} "
        f"{now.timezone_name}"
    )