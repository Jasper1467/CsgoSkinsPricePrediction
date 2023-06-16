package main

import (
	"fmt"
	"log"
	"os"
	"strconv"

	"github.com/go-gota/gota/dataframe"
	"github.com/go-gota/gota/series"
	"gonum.org/v1/gonum/mat"
)

func main() {
	// Load the CSV file
	f, err := os.Open("prices.csv")
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()

	// Read the CSV file into a dataframe
	df := dataframe.ReadCSV(f)

	// Create the feature matrix X
	X := createFeatureMatrix(df)

	// Create the target matrix y
	y := createTargetMatrix(df)

	// Perform linear regression
	coefficients := performLinearRegression(X, y)

	// Print the coefficients
	/*fmt.Println("Coefficients:")
	for i := 0; i < Len(coefficients.); i++ {
		fmt.Printf("Coefficient %d: %.2f\n", i, coefficients.At(i, 0))
	}*/

	// Predict a new sample
	newSample := mat.NewDense(1, X.RawMatrix().Cols, []float64{100, 500, 200, 1000}) // Adjust the values as needed
	predictedPrice := predictPrice(newSample, coefficients)

	fmt.Printf("Predicted price: %.2f\n", predictedPrice)
}

func createFeatureMatrix(df dataframe.DataFrame) *mat.Dense {
	// Select the relevant columns for the feature matrix
	features := df.Select([]string{"Battle Scarred", "Factory New", "StatTrak Battle Scarred", "StatTrak Factory New"})

	// Convert the features dataframe to a matrix
	numRows, numCols := features.Dims()
	featureData := make([]float64, numRows*numCols)
	index := 0
	for i := 0; i < numRows; i++ {
		for j := 0; j < numCols; j++ {
			val := features.Elem(i, j).Float()
			featureData[index] = val
			index++
		}
	}
	featureMatrix := mat.NewDense(numRows, numCols, featureData)

	return featureMatrix
}

func createTargetMatrix(df dataframe.DataFrame) *mat.Dense {
	// Select the target column
	target := df.Col("Price")

	// Convert the target series to a matrix
	targetMatrix := seriesToMatrix(target)

	return targetMatrix
}

func seriesToMatrix(s series.Series) *mat.Dense {
	records := s.Records()
	data := make([]float64, len(records))
	for i, r := range records {
		val, err := strconv.ParseFloat(r, 64)
		if err != nil {
			log.Fatalf("conversion error: %v\n", err)
		}
		data[i] = val
	}

	return mat.NewDense(len(records), 1, data)
}

func performLinearRegression(X, y *mat.Dense) *mat.Dense {
	// Create a new matrix to store the coefficients
	coefficients := mat.NewDense(X.RawMatrix().Cols, 1, nil)

	// Perform linear regression
	ok := coefficients.Solve(X, y)
	if ok == nil {
		log.Fatal("Failed to perform linear regression")
	}

	return coefficients
}

func predictPrice(sample *mat.Dense, coefficients *mat.Dense) float64 {
	var result mat.Dense
	result.Mul(sample, coefficients)

	return result.At(0, 0)
}
