#### BUSINESS PROBLEM RESTATED:

We need to create data pipeline that takes in incidents creates a collective database that sorts and analyzes them, all for the purpose of proving staffing needs. The final working product needs to be able to categorize the incidents with categories, resolution times, averages, as well as display a succinct visualization of the analysis of the data through separate charts.

#### APPROACH
Python pipeline. One script pulls rows from /incidents , loads them into pandas, cleans them, and writes every CSV and PNG in one run. This demonstrates repeatability: one command regenerates everything, and the script is the documentation.
