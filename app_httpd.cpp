#include "esp_camera.h"
#include "esp_http_server.h"

// Streaming ke liye boundary headers (yeh video frames ko alag karne me madad karta hai)
#define PART_BOUNDARY "123456789000000000000987654321"
static const char* _STREAM_CONTENT_TYPE = "multipart/x-mixed-replace;boundary=" PART_BOUNDARY;
static const char* _STREAM_BOUNDARY = "\r\n--" PART_BOUNDARY "\r\n";
static const char* _STREAM_PART = "Content-Type: image/jpeg\r\nContent-Length: %u\r\n\r\n";

httpd_handle_t stream_httpd = NULL;

// 1. Live Stream Handle Karne Ka Function
static esp_err_t stream_handler(httpd_req_t *req) {
    camera_fb_t * fb = NULL;
    esp_err_t res = ESP_OK;
    char * part_buf[64];

    // HTTP connection type ko "multipart/x-mixed-replace" set karna (streaming ke liye zaroori)
    res = httpd_resp_set_type(req, _STREAM_CONTENT_TYPE);
    if(res != ESP_OK) return res;

    // Infinite loop jo lagatar frames bhejega
    while(true) {
        fb = esp_camera_fb_get(); // Camera se naya frame (photo) capture karna
        if (!fb) {
            Serial.println("Camera capture failed!");
            res = ESP_FAIL;
            break;
        }

        // Frame ko chhote HTTP chunks (hisse) me convert karke bhejna
        if(res == ESP_OK){
            res = httpd_resp_send_chunk(req, _STREAM_BOUNDARY, strlen(_STREAM_BOUNDARY));
        }
        if(res == ESP_OK){
            size_t hlen = snprintf((char *)part_buf, 64, _STREAM_PART, fb->len);
            res = httpd_resp_send_chunk(req, (const char *)part_buf, hlen);
        }
        if(res == ESP_OK){
            res = httpd_resp_send_chunk(req, (const char *)fb->buf, fb->len); // Actual image data
        }
        
        esp_camera_fb_return(fb); // Memory ko free karna taaki naya frame aa sake
        
        // Agar laptop/receiver disconnect ho jaye, toh loop tod dena
        if(res != ESP_OK) {
            break; 
        }
    }
    return res;
}

// 2. Web Server Start Karne Ka Function
void startCameraServer() {
    httpd_config_t config = HTTPD_DEFAULT_CONFIG();
    config.server_port = 81; // Stream ko Port 81 par set karna

    // Stream URL define karna (e.g., http://192.168.x.x:81/stream)
    httpd_uri_t stream_uri = {
        .uri       = "/stream",
        .method    = HTTP_GET,
        .handler   = stream_handler,
        .user_ctx  = NULL
    };
    
    Serial.printf("Starting web server on port: '%d'\n", config.server_port);
    
    // Server start karna aur /stream link ko active karna
    if (httpd_start(&stream_httpd, &config) == ESP_OK) {
        httpd_register_uri_handler(stream_httpd, &stream_uri);
    } else {
        Serial.println("Error starting streaming server!");
    }
}
