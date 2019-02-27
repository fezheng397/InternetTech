# InternetTech


# Project 1
0. Felix Zheng fdz6
   Jason Gomes jjg253
   
1. We utilized recursion when opening the TS client socket. This recursion call is nested in our general client method and it is opened 
   everytime the RS server returns the message "{ TS DNS } - NS". We made this recursive so that everytime this situation occurs, we can 
   quickly open the TS client socket, implement the necessary functionality, and then close it, letting our client go back to our RS client    socket afterwards and continuing the main process.

2. There are no known issues with the functionality of our code. However, in the case of a timeout due to the time set by our thread.sleep    methods, we were not fully sure how to handle that. This would only occur in the situation where there is a humongous input that takes a    very long time to run.

3. 
