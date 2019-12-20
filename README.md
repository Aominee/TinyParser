# TinyParser
A parser for Tiny language

# How to use the scanner
- Make instance of it as following where `tiny_code` is the input code <br>
`s = TinyScanner(tiny_code)`
- You can scan the code using `scan` function which returns a string of (tokenvalue, tokentype)<br>
`output_str = s.scan()`
- You can save the output to a file using `createOutputFile` function<br>
` s.createOutputFile('out.txt')`

# How to setup the requirments
- You need to have python 3 up and running
- You need to install the libraries in the requirements.txt file. You can install them via `pip` using the following command<br>
`pip install -r requirements.txt`
- You need to install Graphviz
- For ubuntu, write this command in terminal<br>
`sudo apt-get install graphviz`
- For windows, download from this link<br>
http://www.graphviz.org/Download_windows.php
and then add the following folder to the path in your environment variables<br>
`C:\Program Files (x86)\Graphviz2.38\bin\`
