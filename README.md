# InternetTech


# Project 1
0. Felix Zheng fdz6
   Jason Gomes jjg253
   
1. We utilized recursion when opening the TS client socket. This recursion call is nested in our general client method and it is opened every time the RS server returns the message "{ TS DNS } - NS". We made this recursive so that everytime this situation occurs, we can quickly open the TS client socket, implement the necessary functionality, and then close it, letting our client go back to our RS client socket afterwards and continuing the main process.

2. There are no known issues with the functionality of our code. However, in the case of a timeout due to the time set by our thread.sleep methods, we were not fully sure how to handle that. This would only occur in the situation where there is a humongous input that takes a very long time to run.

3. The main problem we ran into was the best way to connect to TS. We considered ideas such as just connecting to RS, saving the results in a data structure, and then connecting to TS to query for whatever is needed. However, the recursive format we ended up using is far superior. 

4. I learned by working on this project that sockets and threads are very difficult to fully grasp. Over time, we gained a stronger understanding on how the sockets made connections and sent and received information, but how the threads were involved in the socket connections was sort of lost on us. We did definitely learn a lot about how DNS servers work, and I think that is the key point of the class. I also can say we worked really well as group and got this project started very early and generally did not stress over it. Overall, I feel very good about project 1. 
