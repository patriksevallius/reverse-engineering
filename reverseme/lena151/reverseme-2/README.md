# Reverse Me #2

https://forum.tuts4you.com/topic/9169-crackme-here-is-a-challenge-for-all-have-fun/

https://tuts4you.com/download.php?view.1346

http://crackmes.cf/users/lena151/reverseme2_by_lena151/

From what I can tell, noone has posted a keygen (except for Lena151) and I haven't found a writeup either.

This is my first writeup of a ReverseMe, so bear with me.

First I loaded the ReverseMe#2.exe in IDA 6.95 demo. Notice the RM (ReverseMe) is an MFC app.
After doing some research on reversing MFC apps I searched the code for initterm calls. 2 are found near each other called from start.

![initterm calls](/reverseme/lena151/reverseme-2/images/initterm.png)

The first call is passed start and stop address with null pointers, the second one is more interesting:

![initterm calls](/reverseme/lena151/reverseme-2/images/initterm-functions.png)

If we follow sub_42C1A0 we end up at loc_42BF30. CWinApp::CWinApp() is called, so this is probably the constructor for our main app class. On address 42BFB4 offset off_439F68 is copied into [esi], this is the vtable for our main class:

![initterm calls](/reverseme/lena151/reverseme-2/images/main-vtable.png)
