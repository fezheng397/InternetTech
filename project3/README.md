Project 3 ReadMe

0. Please write down the full names and netids of all your team members.
   Felix Zheng fdz6
   Jason Gomes jjg253
1. Briefly discuss how you implemented the challenge-response functionality and
   the authenticated DNS query.
   We created a socket on both the client and the AS server to facilitate a connection. Afterwards, we created the digests on the client side using the keys and sent the list of challenges and digests from client to AS. Afterwards, AS creates two connections, one with TS1 and one with TS2 and sent the challenges forward. The TS servers received each challenge and created then returned the digest to the AS server. AS then verified whether or not one of the two digests matched the digest from the client side. If so, it was considered authenticated and the hostname of the corresponding TS server was sent back to the client. If not, it returned an error message.

1. Are there known issues or functions that aren't working currently in your
   attached code? If so, explain.
   No, all the functionalities within the instructions.txt doc that were required should be fully functional and working.

1. What problems did you face developing code for this project?
   We faced a challenge when deciding how to architect the connections for the project. Specifically, deciding how to split up each connection and what jobs each should do. This popped up in two specific scenarios, the first being how to handle the TS sockets as they had to receive both a connection from the AS server, and then later from the client. This was fixed by creating two separate, sequential threads. One would handle the connection to the AS server, the other afterwards, handled the client connection. The second case was when deciding how to split the sending messages from client to the correct server of TS1 or TS2. We finally decided to send all the messages destined for TS1 at once, then all the messages destined for TS2 afterwards. This way, we kept it clean and organized. We then reordered the responses at the end so the resolved output remained correct.

1. What did you learn by working on this project?
   We learned much about client-server architecture and the connections between them. It certainly helped our understanding of how the internet and the DNS system works as a whole as well. It is certainly something that will benefit in future work as a software engineer regarding any project working on a website.
