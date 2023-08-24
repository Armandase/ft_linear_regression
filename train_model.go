package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"

	"gonum.org/v1/gonum/mat"
	"gonum.org/v1/plot"
	"gonum.org/v1/plot/plotter"
)

func main() {
	xys, divisor_x, divisor_y, err := readData("data.csv")
	render_file := "data.png"
	if err != nil {
		log.Fatalf("Could not read data.csv: %v", err)
	}
	sum1 := 0.0
	sum0 := 0.0
	theta0 := 0.0
	theta1 := 0.0
	learning_rate := 0.001
	// for i := 0; i < 1000; i++ {
	sum1 = 0.0
	sum0 = 0.0
	for _, point := range xys {
		sum0 += (theta0 + theta1*point.X) - point.Y
		sum1 += ((theta0 + theta1*point.X) - point.Y) * point.X
	}
	theta0 = learning_rate * 1.0 / float64(xys.Len()) * sum0
	theta1 = learning_rate * 1.0 / float64(xys.Len()) * sum1
	// }
	// theta0 *= divisor_x
	// theta1 *= (divisor_x / divisor_y)
	fmt.Println(divisor_x / divisor_y)
	fmt.Println("theta0: ", theta0)
	fmt.Println("theta1: ", theta1)
	fmt.Println("price for 42000: ", theta0+theta1*42000)

	file, err := os.OpenFile("theta.csv", os.O_CREATE|os.O_WRONLY|os.O_TRUNC, 0600)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	string_data := fmt.Sprintf("theta0,theta1\n%f,%f", theta0, theta1)
	_, err = file.WriteString(string_data)
	if err != nil {
		panic(err)
	}
	err = plotData(render_file, theta0, theta1, xys)
	if err != nil {
		log.Fatalf("Could not plot data: %v", err)
	}

}

func plotData(file string, theta0 float64, theta1 float64, pxys plotter.XYs) error {
	f, err := os.Create(file)
	if err != nil {
		return fmt.Errorf("could not create data.png: %v", err)
	}
	defer f.Close()

	p := plot.New()

	s, err := plotter.NewScatter(pxys)
	if err != nil {
		return fmt.Errorf("could not create scatter: %v", err)
	}
	p.Add(s)

	maxX := math.Inf(-1)
	minX := math.Inf(1)
	for _, point := range pxys {
		if point.X > maxX {
			maxX = point.X
		}
		if point.X < minX {
			minX = point.X
		}
	}
	l, err := plotter.NewLine(plotter.XYs{
		{X: minX, Y: theta0 + (theta1 * minX)},
		{X: maxX, Y: theta0 + (theta1 * maxX)},
	})
	if err != nil {
		return fmt.Errorf("could not create line: %v", err)
	}
	p.Add(l)

	wt, err := p.WriterTo(512, 512, "png")
	if err != nil {
		return fmt.Errorf("could not create writer: %v", err)
	}
	_, err = wt.WriteTo(f)
	if err != nil {
		return fmt.Errorf("could not write to %s: %v", file, err)
	}

	if err := f.Close(); err != nil {
		return fmt.Errorf("could not close %s: %v", file, err)
	}
	return nil
}

func readData(path string) (plotter.XYs, float64, float64, error) {
	f, err := os.Open(path)
	if err != nil {
		return nil, 0.0, 0.0, err
	}

	defer f.Close()

	var tmp_xys plotter.XYs
	var x_array []float64
	var y_array []float64
	s := bufio.NewScanner(f)
	for s.Scan() {
		var x, y float64
		_, err := fmt.Sscanf(s.Text(), "%f,%f", &x, &y)
		if err != nil {
			fmt.Println("Bad data: ", err)
		} else {
			tmp_xys = append(tmp_xys, struct{ X, Y float64 }{x, y})
			x_array = append(x_array, x)
			y_array = append(y_array, y)
		}
	}
	if err := s.Err(); err != nil {
		return nil, 0.0, 0.0, err
	}

	vec_x := mat.NewVecDense(len(x_array), x_array)
	vec_y := mat.NewVecDense(len(y_array), y_array)
	divisor_x := mat.Norm(vec_x, 2) / float64(len(x_array))
	divisor_y := mat.Norm(vec_y, 2) / float64(len(y_array))

	var xys plotter.XYs
	for _, point := range tmp_xys {
		xys = append(xys, struct{ X, Y float64 }{point.X / divisor_x, point.Y / divisor_y})
	}
	return xys, divisor_x, divisor_y, err
}
