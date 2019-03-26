# InternetTech


# Project 1
0. Please write down the full names and netids of all your team members.
0. Felix Zheng fdz6
   Jason Gomes jjg253
   
1. Briefly discuss how you implemented your recursive root and TLD server functionality.
1. We utilized recursion inside the rs.py file when the requested host is not found inside the RS' DNS table. From there, it checks if the address ends in edu or com (or neither) and connects to the appropriate TS server. After it communicates with the TS server and receives the address, it closes that connection and returns that address to the client. This isn't true recursion in that no method is called within itself, but it is a recursive nature in which we solved the problem. 

2. Are there known issues or functions that aren't working currently in your attached code? If so, explain.
2. Similar to project 1, there are no known bugs or issues with our code. Everything works as designed. My partner and I just wish we could receive feedback on Project 1 before submitting Project 2 so we could know if there is anything wrong with our code in the first place. We didn't know if there was something we should change in regards to the timeout or threading, along with all the print statements we have in our code. Other than the small things, we are confident our code works.

3. What problems did you face developing code for this project?
3. The main problem we ran into was the best way to connect to TS. We looked into possible true recursive solutions but didn't see a good way to do it, considering RS starts as a server in with the client connection and then connects as the client with the TS servers. We looked into possibly just having an if statement where it checks if the connection is as a client or a server through a boolean added in as a parameter, but it did not seem worth it. Otherwise, the solution seemed pretty simple coming from Project 1. It took us about 3 hours to make Project 2 work. The only other problem was the communication issue I mentioned in Q1 where I wish we received feedback, but that's not exactly a problem.

4. What did you learn by working on this project?
4. I don't think I learned anything new from Project 1. In Project 1, I learned that sockets and threads are very difficult to fully grasp. Over time, we gained a stronger understanding on how the sockets made connections and sent and received information, but how the threads were involved in the socket connections was sort of lost on us. Now, we are experts on it comparative to where we started. 
