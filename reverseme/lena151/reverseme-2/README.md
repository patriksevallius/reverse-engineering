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

sub_42C1E0 is CWinThread::InitInstance() and sub_42F6F0 is CWinThread::ExitInstance().

Go to sub_42C1E0 (this is where everything interesting happens) and rename 'lParam' to 'this'.
Browsing through all the calls from sub_42C1E0 I found sub_42D270 that calls FindResourceA(0, 129, 10). 10 is RT_RCDATA.

This led me to fireing up ResourceHacker.

![initterm calls](/reverseme/lena151/reverseme-2/images/resourcehacker.png)

Would you look at that, it has RCData 129, and it contains what look to be registration strings, probably the false ones Lena151 talked about. sub_42D270 loads the resource and creates a CMemFile object out of it and stores it in this+0xf4.

Back to sub_42C1E0, at 42C5A0 a call to dword ptr [eax+3Ch] is made, eax contains the vtable for the CMemFile from above. This is CMemFile::Read. Additional calls to CMemFile::Read are made. I extracted the RCData 129 to a file and began structuring it according to the read calls.

![initterm calls](/reverseme/lena151/reverseme-2/images/rs129-1.png)

The call to sub_42F880 reads 32 more bytes, the last 4 bytes are used as a size, and since it's 0 nothing more happens.
We then reads 4 more bytes and treats them as a count (0 for this resource file). We repeat this 4 times.

The next interesting call is at 42C88E where sub_42D430 is called. Here we reads 4 more bytes and treats them as a count (0x48 for this resource file). We then read 1 byte 0x48 times. Valid values seems to be 0, 1 and 4.

At 42C8D0, sub_42D540 is called. Here we reads 4 more bytes and treats them as a count (0x19 for this resource file). We then read 4 bytes 0x19 times. These looks like offsets to me.

At 42C912, sub_42D5D0 is called. Here we reads 4 more bytes and treats them as a count (2 for this resource file). We then read 4 bytes 0x19 times. 

At 42C954, sub_42D660 is called. Here we reads 4 more bytes and treats them as a count (0 for this resource file).

Not much of interest happens until 42CBD4 where sub_41A6A0 is called. Here a new unknown object is created, with a new CMemFile for the same resource and stored at offset 8 in the new object. The object pointer is stored in [ebp+var_198] from the calling method.

Finally at 42CBF4, sub_41A7C0 is called.

sub_41A7C0 calls CMemFile->vtable+0x14 and CMemFile->vtable+0x30 (CMemFile::GetPosition and CMemFile::Seek) then calls sub_41A8D0 and then CMemFile::Seek with the position saved from the CMemFile::GetPosition call. The position it seeks to is passed in as the first argument. The offset is the first 4 bytes we read from the resource file (0x102).

sub_41A8D0 reads one byte from the CMemFile and then switches on that value.
Accepted values are: 4, 5, 0x12, 0x14, 0x16, 0x1a, 0x1e, 0x2f. All other values are discarded and a new byte is read.

