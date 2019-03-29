# Important note:

For all examples, I am using python 3.6.8. If there are any errors due to dictionaries and ordering, I'm using a few niceties that were implemented close to 3.7. 

All tests require internet access.

In the readme, you'll find user documentation. For implementation documentation, see the docstrings in each function body where implementation documentation is needed. You'll find necessary explanations in the docstrings of each function, explaining how each one works. 

You'll see a few utility functions imported from `helpers.py`. See the bottom section for descriptions for those functions.


## Trie and Trie OOP
To run: 
```
$ python3 ./trie.py '<test-password>'
```
`<test-password>` should be wrapped in `''`.

Both of these produce the same result. Recursively generates a trie data structure to discover password uniquness. The requirement says to read the text from a file. I do read the results from a file, but that file is coming directly from the url provided in the requirements, and is then deleted.

## Weather
Depends on:
- requests `pip install requests`

To run:
```
$ python3 weather <zip-code>
```
`<zip-code>` should be a 5 digit integer

1. Get the lat-long conversion from an api. 
2. Take the lat-long and get the weather results from the national weather service. 
3. The national weather service returns another end-point to call based on what kind of report you would like. HTTP Get the end-point for hourly forecast.
4. Get the description and temperature from the first item in the hourly forecast
5. convert temperature to kelvin


## Fizz Buzz Server

Depends on:
- urllib.parse (python 3.4+)
- http.server

To run:
```
$ python3 fizz_buzz_server
```

Next, open another terminal session and run:
```
$ curl http://localhost:8080/fizzbuzz?begin=0%26end=100
```

I had some issues using `&` directly in the query-string, so I used the encoded `%26` instead. Also, there is very little error checking surrounding the querystring, so it's probably very easy to break. 

## Helpers
You'll see the following functions used sparingly throughout the code. They were particularly helpful in the recursive trie solutions. 
- Take +n list: get the first n elements
- Take -n list: get the last n elements

- Drop +n list: get the last n elements
- Drop -n list: get the first n elements

- first   list: get the first element in a list
- rest    list: get all but the first element in a list