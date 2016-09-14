package main

import (
	"fmt"
	"os/exec"
	"github.com/pebbe/zmq4"
)


func main (){

	context ,_ := zmq4.NewContext()
	socket,_ := context.NewSocket(zmq4.REP)
	defer socket.Close()
	socket.Bind("tcp://*:9999")
	for {
		msg,_ := socket.Recv(0)
		fmt.Println("MSG is",string(msg))
		neighor := "172.16.2.10"
		out,err := exec.Command("./gobgp","neighbor",neighor,"adj-in","-a","link-state","-j").Output()
		if err != nil {
			fmt.Println("",err)
		}

		socket.Send(string(out), 0)
	}


}
