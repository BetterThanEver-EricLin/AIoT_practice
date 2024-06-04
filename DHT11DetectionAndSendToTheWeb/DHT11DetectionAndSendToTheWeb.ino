#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT11.h>
#include <ArduinoJson.h>

// WiFi credentials
const char* ssid = "AndroidAP_3884";
const char* password = "12345678";

// Server address
const char* server_address = "http://192.168.100.103:5000/post_data";

// DHT11 sensor pin
const int pinDHT11 = 15;

// DHT11 instance
DHT11 dht11(pinDHT11); 

void setup() {
  Serial.begin(115200);
  delay(1000);

  // Connect to WiFi
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");
}

void loop() {
  int temperature = 0;
  int humidity = 0;
  
  // Read temperature and humidity from DHT11 sensor
  int result = dht11.readTemperatureHumidity(temperature, humidity);
  
  if (result == 0) {
    // Print temperature and humidity
    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.print(" °C\tHumidity: ");
    Serial.print(humidity);
    Serial.println(" %");
  } else {
    // Print error message
    Serial.print("Error reading DHT11 sensor: ");
    Serial.println(DHT11::getErrorString(result));
  }

  // Prepare JSON data
  DynamicJsonDocument jsonDoc(200);
  jsonDoc["temperature"] = temperature;
  jsonDoc["humidity"] = humidity;

  String payload;
  serializeJson(jsonDoc, payload);

  // HTTP POST Request
  HTTPClient http;

  Serial.println("Sending POST request to server...");
  http.begin(server_address);
  http.addHeader("Content-Type", "application/json");

  int httpResponseCode = http.POST(payload);

  if (httpResponseCode > 0) {
    Serial.printf("HTTP Response code: %d\n", httpResponseCode);
    String response = http.getString();
    Serial.println(response);
  } else {
    Serial.printf("HTTP Request failed: %s\n", http.errorToString(httpResponseCode).c_str());
  }

  http.end();

  // Delay and Serial Output
  Serial.println("Waiting for 5 seconds before next iteration...");
  delay(5000);
  Serial.println();
}
