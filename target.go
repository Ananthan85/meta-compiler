package main

/*
#include <stdint.h>
extern int32_t process_go_data(int32_t* arr, int32_t length, int32_t offset);
*/
import "C"
import (
	"fmt"
	"unsafe"
)

func main() {
	isTesting := true
	
	dataArr := []int32{0, 10, 20, 30, 40, 50, 60, 70, 80, 90}

	ptr := (*C.int32_t)(unsafe.Pointer(&dataArr[0]))
	length := C.int32_t(len(dataArr))

	if isTesting {
		fmt.Println("Passing array to C side...")
	}
	
	result := C.process_go_data(ptr, length, 9)
	fmt.Printf("Result from C function: %d\n", result)
}
