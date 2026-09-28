#include "esp_camera.h"
#include <WiFi.h>

// ==========================================
// 1. CAMERA MODEL SELECT KARNA
// ==========================================
// Baaki sabhi models ke aage '//' lagakar unhe comment kar de
// Aur sirf CAMERA_MODEL_AI_THINKER ko uncomment rakhein (Kyunki market me yahi sabse zyada milta hai)

//#define CAMERA_MODEL_WROVER_KIT
//#define CAMERA_MODEL_ESP_EYE
//#define CAMERA_MODEL_M5STACK_PSRAM
//#define CAMERA_MODEL_M5STACK_V2_PSRAM
//#define CAMERA_MODEL_M5STACK_WIDE
//#define CAMERA_MODEL_M5STACK_ESP32CAM
#define CAMERA_MODEL_AI_THINKER  // <-- Sirf isko active rakhna hai
//#define CAMERA_MODEL_TTGO_T_JOURNAL

#include "camera_pins.h"

// ==========================================
// 2. APNA WI-FI HOTSPOT DETAILS DALNA
// ==========================================
const char* ssid = "YOUR_HOTSPOT_NAME";       // Apna Wi-Fi naam yaha dale (e.g., "Shubham_Phone")
const char* password = "YOUR_HOTSPOT_PASSWORD"; // Apna Wi-Fi password yaha dale

void startCameraServer();

void setup() {
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println();

  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.frame_size = FRAMESIZE_UXGA;
  config.pixel_format = PIXFORMAT_JPEG; // Streaming ke liye JPEG best hai
  config.grab_mode = CAMERA_GRAB_WHEN_EMPTY;
  config.fb_location = CAMERA_FB_IN_PSRAM;
  config.jpeg_quality = 12; // Quality (10-63), low number means high quality
  config.fb_count = 1;

  // Frame size chota karna taaki live video fast chale (bina lag ke)
  if(psramFound()){
    config.frame_size = FRAMESIZE_VGA; // SIH drone streaming ke liye VGA (640x480) best hai
    config.jpeg_quality = 10;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_SVGA;
    config.jpeg_quality = 12;
    config.fb_count = 1;
  }

  // Camera Initialize karna
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  // ==========================================
  // WI-FI CONNECTION LOGIC
  // ==========================================
  WiFi.begin(ssid, password);
  WiFi.setSleep(false); // Drone udate waqt Wi-Fi disconnect na ho isliye sleep off

  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.println("Wi-Fi Connected Successfully!");

  startCameraServer();

  Serial.print("Camera Ready! Use 'http://");
  Serial.print(WiFi.localIP());
  Serial.println("' to connect");
}

void loop() {
  // Web server background me run hota rahega, yaha kuch dalne ki jarurat nahi hai
  delay(10000);
}
