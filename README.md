# OS Assignment 3 
#### (a1822503 Sebastian Cocks & a1773444 Cameron Scott)

## Running the Python Program
The program can be ran with:

```bash
python3 main.py -l <listening port> -p <pattern>
```
## Sending data
Data can be sent to the socket using netcat with the following syntax
```bash
nc <address> <listening port> -i <delay> < <file.txt>
```
For example, to send some test data when hosted locally on port 1024
```bash
nc localhost 1024 -i 0 < test_data/input_1.txt
```

## Testing
There are a couple of test files:

- `3_threads.sh` simultaneously sends 3 sets of data to the server on `localhost 1024`.

- `10_threads.sh` simultaneously sends 10 sets of data to the server on `localhost 1024`.