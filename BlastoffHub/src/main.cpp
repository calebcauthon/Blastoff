#include <Arduino.h>
#include <Vector.h>
#include <Screen.cpp>
#include <AceButton.h>
using namespace ace_button;

Screen screen;


const int BUTTON_PIN = 2;
AceButton button(BUTTON_PIN);
void handleEvent(AceButton*, uint8_t, uint8_t);

// events
int bootup = 1;
int heartbeat = 2;
int buttonPush = 3;

// info's
int timestamp = 1;
int location = 2;


char buffer[50];
char startTemplate[20] = "START-%i"; // event
char infoTemplate[20] = "INFO-%i:%i:%i"; // event:name:value
char endTemplate[20] = "END-%i"; // event

int names [10];
Vector<int> v_names(names, 10); 

int values [10];
Vector<int> v_values(values, 10);

void printEventStart(int id) {
  sprintf(buffer, startTemplate, id);
  Serial.println(buffer);
}

void printEventInfo(int eventId, int name, int value) {
  sprintf(buffer, infoTemplate, eventId, name, value);
  Serial.println(buffer);
}

void printEventEnd(int id) {
  sprintf(buffer, endTemplate, id);
  Serial.println(buffer);
}

void sendEvent(int event, Vector<int> names, Vector<int> values) {
  printEventStart(bootup);
  for(int i = 0; i < names.size(); i++) {
    printEventInfo(event, names.at(i), values.at(i));
  }
  printEventEnd(event);
}

void resetSerialParameters() {
  v_names.clear();
  v_values.clear(); 
}

void triggerEventStart(int event) {
  printEventStart(event);
  //resetSerialParameters();
}

void addEventInfo(int event, int name, int value) {
  printEventInfo(event, name, value);
  //v_names.push_back(name);
  //v_values.push_back(value);
}

void triggerEventEnd(int event) {
  printEventEnd(event);
  //sendEvent(event, v_names, v_values);
}

int buttonInput = 2;
void setup() {
  Serial.begin(9600);

  screen.init();

  triggerEventStart(bootup);
  addEventInfo(bootup, timestamp, millis());
  addEventInfo(bootup, location, 35);


  pinMode(BUTTON_PIN, INPUT_PULLUP);
  ButtonConfig* buttonConfig = button.getButtonConfig();
  buttonConfig->setEventHandler(handleEvent);
  buttonConfig->setFeature(ButtonConfig::kFeatureClick);
  buttonConfig->setFeature(ButtonConfig::kFeatureDoubleClick);
  buttonConfig->setFeature(ButtonConfig::kFeatureLongPress);
  buttonConfig->setFeature(ButtonConfig::kFeatureRepeatPress);

}

int i = 0;
void loop() {
  if (false && Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    if (data.charAt(0) == '9') {
      screen.showText("Command received.");
    }
  }
  button.check();
}

void handleEvent(AceButton* /* button */, uint8_t eventType,
    uint8_t buttonState) {

  switch (eventType) {
    case AceButton::kEventPressed:
      Serial.println("button push.");
      triggerEventStart(buttonPush);
      triggerEventEnd(buttonPush);
      break;
    case AceButton::kEventReleased:
      break;
  }
}
