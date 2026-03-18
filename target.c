#include <stdint.h>
// #include <stdio.h>  // used for debugging earlier

int32_t process_go_data(int32_t* arr, int32_t length, int32_t offset) {
    int32_t temp_val = 0; 
    
    int32_t secret_index = offset + 1; 
    
    // Note: need to add bounds check here eventually
    int32_t value = arr[secret_index]; 
    
    return value + temp_val; 
}
