#socket fd type
FD_TYPE_ACCEPT		= 1  #accept client socket
FD_TYPE_CLIENT		= 2  #read or write client socket
FD_TYPE_SERVER		= 3  #read or write server socket
FD_TYPE_CONNECT		= 4  #connect to server
FD_TYPE_CLOSE		= 5  #close socket
FD_TYPE_TIMER		= 6

#server process type
SERVER_TYPE_CLIENT	= 1
SERVER_TYPE_GATE	= 2
SERVER_TYPE_GAME	= 3
SERVER_TYPE_DB		= 4

#mongodb operation
FIND_DOC_OP = 1
UPDATE_DOC_OP = 2
INSERT_DOC_OP = 3