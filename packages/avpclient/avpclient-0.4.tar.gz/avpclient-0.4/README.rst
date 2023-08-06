AVP Client
=======================

AVPclient is the client that utilizes AIDVP's Portfolio Performance and Risk Analytics - Basic API.

It has a collection of functions for portfolio performance and risk analysis.
----

Please visit AIDVP's Portfolio Performance and Risk Analysis for more detail
<https://github.com/aidvp/Portfolio_Performance_and_Risk_Analysis>

The package contains a sync and an async version of the API. The async version supports data warehouse's refresh capability where it can recalculate a significant amount of data. The client will throttle at 1000 connection at a time.

The benefit of the async version are:
1. faster request
2. smaller download size

Not all requests should use the async version. If your total request's size is small, then async version will not be of much help to you. Also, it will incur higher cost. The rule of thumb is that use Async for 25+ data points. Each data point is a series of data and value.

Hope this help.