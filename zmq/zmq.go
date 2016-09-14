package main

import (
	"fmt"
	"github.com/pebbe/zmq4"
	//"encoding/json"
)


func main (){
	context, _ := zmq4.NewContext()
	socket, _ := context.NewSocket(zmq4.REQ)
	defer socket.Close()

	socket.Connect("tcp://localhost:9999")
	msg:= "SendTopology"
	socket.Send(msg,0)

	reply,_ := socket.Recv(0)
	//json_recv,_ := json.Marshal(reply)
	fmt.Println("Recieved: ",string(reply))

}
