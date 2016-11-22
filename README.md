# mcomix-touchnav
This python (2.7) script provides navigation buttons for use in MComix.

It's a really ugly and hacky script I wrote in high-school with zero prior
WinAPI experience and nearly zero prior Python experience. It shows.
Please don't judge me by this too much; take it as an item of historical
significance to me as it was very cool in my eyes when I wrote it in the 10th
or 11th grade.

It is currently windows-only, because I was never able to get a GNU/Linux distro
working on a Clover Trail SOC, unfortunately, and I did it on a school tablet
that I no longer posess that ran Windows 8. If I ever get a cheap touchscreen
tablet that I can boot a regular GNU/Linux distro off of, you can bet I'll
make this work on it via XCB or Xlib.

It's been so long since I made this and last used it that I can't really
remember much about how it was used, but I believe that after launching it I
hit the `Select` button, and then had three seconds to change the active
window to mcomix. After three seconds, the progam checks the currently active
window, and stores the window's ID (This sounded like a good idea at the time).

The `Fullscreen` button sends the 'f' keystroke to mcomix to put it into
fullscreen mode. It sends the PageUp and PageDown keys when the arrows are
pressed. It handles changing window focuses and keeping the control window on top.

Not an elegant solution, but it let me read my manga on my tablet in portrait
mode without a keyboard attached, so it was worth it.
