#include <Arduino.h>
#include <Vector.h>
#include <Screen.cpp>
#include <AceButton.h>
using namespace ace_button;

Screen screen;


const int BUTTON_PIN = 2;
AceButton button(BUTTON_PIN);
void handleEvent(AceButton*, uint8_t, uint8_t);

// event names
int bootup = 1;
int heartbeat = 2;
int buttonPush = 3;

// info's
int timestamp = 1;
int location = 2;
int eventType = 3;

int id = 1;

char buffer[50];
char startTemplate[20] = "START-%i"; // event
char infoTemplate[20] = "INFO-%i:%i:%i"; // event:name:value
char endTemplate[20] = "END-%i"; // event

int names [10];
Vector<int> v_names(names, 10); 

int values [10];
Vector<int> v_values(values, 10);

int printEventStart() {
  int thisId = id;
  sprintf(buffer, startTemplate, thisId);
  Serial.println(buffer);
  id++;

  return thisId;
}

void printEventInfo(int eventId, int name, int value) {
  sprintf(buffer, infoTemplate, eventId, name, value);
  Serial.println(buffer);
}

void printEventEnd(int id) {
  sprintf(buffer, endTemplate, id);
  Serial.println(buffer);
}

void addEventInfo(int event, int attributeName, int value) {
  printEventInfo(event, attributeName, value);
}

int triggerEventStart(int event) {
  int thisId = printEventStart();
  addEventInfo(thisId, eventType, event);
  return thisId;
}

void triggerEventEnd(int event) {
  printEventEnd(event);
}

int buttonInput = 2;
void setup() {
  Serial.begin(9600);

  screen.init();

  int bootupId = triggerEventStart(bootup);
  addEventInfo(bootupId, timestamp, millis());
  triggerEventEnd(bootupId);

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
      int buttonPushId = triggerEventStart(buttonPush);
      addEventInfo(buttonPushId, timestamp, millis());
      triggerEventEnd(buttonPushId);
      break;
    case AceButton::kEventReleased:
      break;
  }
}
