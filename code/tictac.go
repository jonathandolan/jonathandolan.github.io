package main

import (
	"fmt"
	"strings"
)

var initial string
var xboard string
var yboard string

func checkX(c chan bool) {
	c <- checkHoriz(xboard, "xxxx")
	c <- checkVertX(xboard)
	c <- checkDiagX(xboard)
	close(c)
}

func checkY(c chan bool) {
	c <- checkHoriz(yboard, "yyyy")
	c <- checkVertY(yboard)
	c <- checkDiagY(yboard)
	close(c)
}

func checkHoriz(input string, target string) bool {
	if strings.Contains(input, target) {
		return true
	} else {
		return false
	}
}

func checkVertX(input string) bool {
	answer := false
	for i := 0; i < 4; i++ {
		if input[i] == 'x' && input[i+4] == 'x' && input[i+8] == 'x' && input[i+12] == 'x' {
			answer = true
			break
		}
	}
	return answer
}

func checkVertY(input string) bool {
	answer := false
	for i := 0; i < 4; i++ {
		if input[i] == 'y' && input[i+4] == 'y' && input[i+8] == 'y' && input[i+12] == 'y' {
			answer = true
			break
		}
	}
	return answer
}

func checkDiagX(input string) bool {
	answer := false
	if input[0] == 'x' && input[5] == 'x' && input[10] == 'x' && input[15] == 'x' {
		answer = true
	} else if input[3] == 'x' && input[6] == 'x' && input[9] == 'x' && input[12] == 'x' {
		answer = true
	}
	return answer
}

func checkDiagY(input string) bool {
	answer := false
	if input[0] == 'y' && input[5] == 'y' && input[10] == 'y' && input[15] == 'y' {
		answer = true
	} else if input[3] == 'y' && input[6] == 'y' && input[9] == 'y' && input[12] == 'y' {
		answer = true
	}
	return answer
}

func checkDraw(input string) bool {
	answer := true
	if strings.ContainsRune(input, '-') == true {
		answer = false
	}
	return answer
}

func main() {
	//x won
	//x x x t
	//- - - -
	//o o - -
	//- - - -
	initial = "xxxt----oo------"

	//draw
	//x o x t
	//x x o o
	//o x o x
	//x x o o
	//initial = "xoxtxxoooxoxxxoo"

	//ongoing
	//x o x -
	//o x - -
	//- - - -
	//- - - -
	//initial = "xox-ox----------"

	//o won
	//o o x x
	//o x x x
	//o x - t
	//o - - o
	//initial = "ooxxoxxxox-to--o"

	//o won
	//x x x o
	//- - o -
	//- o - -
	//t - - -
	//initial = "xxxo--o--o--t---"

	//o won
	//o x x x
	//x o - -
	//- - o -
	//- - - o
	//initial = "oxxxxo----o----o"
	xboard = strings.Replace(initial, "t", "x", -1)
	yboard = strings.Replace(initial, "t", "y", -1)
	cX := make(chan bool, 3)
	cY := make(chan bool, 3)
	var done bool

	go checkX(cX)
	go checkY(cY)

	for i := range cX {
		if i == true {
			fmt.Println("X WINS")
			done = true
		}
	}

	for i := range cY {
		if i == true {
			fmt.Println("Y WINS")
			done = true
		}
	}

	if checkDraw(xboard) == true || checkDraw(yboard) {
		fmt.Println("Draw")
	} else if done == false && (strings.Contains(xboard, "-") || strings.Contains(yboard, "-")) {
		fmt.Println("ongoing")
	}

}
