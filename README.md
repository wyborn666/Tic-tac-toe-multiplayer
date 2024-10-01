# Tic-tac-toe-multiplayer
___
This project implements a tic-tac-toe multiplayer game based on the transfer of information between the client and the server.
The code is implemented using the python standard library:

+ pygame (it was used to write the single mode class of tic-tac-toe)
+ threading (to organize the operation of parallel data transmission. It is also used to solve the problem of endless waiting for a client and server connection)
+ socket multicast technology (It was used to establish a connection between the client and the server, provided that the client does not know the IP address of the server initially. This technology also allows the client to select one of the available servers)
## Usage

1) Install .zip file and unzip it.

2) The TTT_server and TTT_client files are main files that start the game.

3) The "models" folder contain all resources that programs use.





## License
This project is open source and is available under the [MIT license.](https://github.com/wyborn666/Tic-tac-toe-multiplayer/blob/main/LICENSE)



## Links
https://habr.com/ru/companies/simbirsoft/articles/701020/

https://habr.com/ru/companies/skillfactory/articles/690186/

https://thecode.media/socket/

https://docs.python.org/3/library/socket.html

https://wiki.python.org/moin/GlobalInterpreterLock