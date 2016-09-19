package main

import (
	"fmt"
	"os/exec"
	"github.com/pebbe/zmq4"
	"strings"
)

func main (){

	context ,_ := zmq4.NewContext()
	socket,_ := context.NewSocket(zmq4.REP)
	defer socket.Close()
	socket.Bind("tcp://*:9999")
	for {
		msg,_ := socket.Recv(0)
		fmt.Println("MSG is",string(msg))
		string_msg := string(msg)
		s := strings.Split(string_msg,":")
		fmt.Println("Neighor is: ",s[1])
		out,err := exec.Command("./gobgp","neighbor",s[1],"adj-in","-a","link-state","-j").Output()
		if err != nil {
			fmt.Println("",err)
		}
		socket.Send(string(out), 0)
	}


}
