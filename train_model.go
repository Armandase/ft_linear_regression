package main

import (
	"log"
	"fmt"
	"os"
	"bufio"
	"math"

	"gonum.org/v1/plot"
	"gonum.org/v1/plot/plotter"
)

type xy struct { x, y float64}

func main() {
	xys, err := readData("data.csv")
	file := "data.png"
	if err != nil {
		log.Fatalf("Could not read data.csv: %v", err)
	}
	
	err = plotData(file, xys)
	if err != nil{
		log.Fatalf("Could not plot data: %v", err)
	}
	
}

func plotData(file string, pxys plotter.XYs) error{
	f, err := os.Create(file)
	if err != nil{
		return fmt.Errorf("Could not create data.png: %v", err)
	}
	defer f.Close()

	p := plot.New()

	s, err := plotter.NewScatter(pxys)
	if err != nil{
		return fmt.Errorf("Could not create scatter: %v", err)
	}
	// s.Color = color.RGBA{R: 255, A: 255 }
	p.Add(s)

	maxY := math.Inf(-1)
	maxX := math.Inf(-1)
	minX := math.Inf(1)
	minY := math.Inf(1)
	for _, point := range pxys {
		if point.Y > maxY {
			maxY = point.Y
		}
		if point.X > maxX {
			maxX = point.X
		}
		if point.X < minX {
			minX = point.X
		}
		if point.Y < minY {
			minY = point.Y
		}
	}
	fmt.Println(minY)
	l, err := plotter.NewLine(plotter.XYs{
		{minX, maxY},
		{maxX, minY},
	})
	if err != nil{
		return fmt.Errorf("Could not create line: %v", err)
	}
	p.Add(l)


	wt, err := p.WriterTo(512, 512, "png")
	if err != nil{
		return fmt.Errorf("Could not create writer: %v", err)
	}	
	_, err = wt.WriteTo(f)
	if err != nil{
		return fmt.Errorf("Could not write to %s: %v", file, err)
	}

	if err := f.Close(); err != nil{
		return fmt.Errorf("Could not close %s: %v", file, err)
	}
	return nil
}

func readData(path string) (plotter.XYs, error){
	f, err := os.Open(path)
	if err != nil{
		return nil, err
	}

	defer f.Close()

	var xys plotter.XYs
	s := bufio.NewScanner(f)
	for s.Scan(){
		var x, y float64
		_, err := fmt.Sscanf(s.Text(), "%f,%f", &x, &y)
		if err != nil{
			fmt.Println("Bad data: %v", err)
		} else {
			xys = append(xys, struct{X, Y float64}{x, y})
		}
	}
	if err := s.Err(); err != nil{
		return nil, err
	}
	return xys,err
}