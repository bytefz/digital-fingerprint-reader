# Digital Fingerprint Reader

It's a university project for the course "Digital Systems" at the university.

This project is a digital fingerprint reader. It uses a fingerprint sensor,builed on Arduino, to read the fingerprint and a LCD to display the result. Besides, it uses a buzzer to give a sound when the fingerprint is read.

This project has an interface to connect to a computer. It uses a USB to serial converter to connect to the computer. The computer can send a command to the fingerprint reader to read the fingerprint. The fingerprint reader will send the result to the computer. This interface is used to test the fingerprint reader. It can also be used to connect to a microcontroller (Arduino). This interface was developed using Tkinter on Python, using serial and time libraries. This help to user to know if the fingerprint was read or not and to know if the person is authorized or not.


# Tools used

- Arduino IDE
- C++ language
- Python 3.8
- Tkinter