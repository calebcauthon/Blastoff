#include <Arduino.h>
#include <Vector.h>
#include <Screen.cpp>
#include <AceButton.h>
using namespace ace_button;

Screen screen;

const int BUTTON_PIN = 2;
AceButton button(BUTTON_PIN);
void handleEvent(AceButton*, uint8_t, uint8_t);

const int SLIDER_PIN = A1;
const int KNOB_PIN = A0;

// event names
int bootup = 1;
int heartbeat = 2;
int buttonPush = 3;
int valueChange = 4;
int inputInitialization = 5;

// info's
int timestamp = 1;
int location = 2;
int eventType = 3;
int value = 4;
int minimum = 5;
int maximum = 6;
int identification = 7;

// identification
int sliderId = 1;
int knobId = 2;

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

  pinMode(SLIDER_PIN, INPUT);
  pinMode(KNOB_PIN, INPUT);

  int initId = triggerEventStart(inputInitialization);
  addEventInfo(initId, identification, sliderId);
  addEventInfo(initId, timestamp, millis());
  triggerEventEnd(initId);

  initId = triggerEventStart(inputInitialization);
  addEventInfo(initId, identification, knobId);
  addEventInfo(initId, timestamp, millis());
  triggerEventEnd(initId);
}

int lastSliderValue = 0;
void sliderCheck() {
  int sliderValue = analogRead(SLIDER_PIN);
  int diff = abs(sliderValue - lastSliderValue);
  if (diff > 100) {
    int sliderEventId = triggerEventStart(valueChange);
    addEventInfo(sliderEventId, identification, sliderId);
    addEventInfo(sliderEventId, timestamp, millis());
    addEventInfo(sliderEventId, value, sliderValue);
    triggerEventEnd(sliderEventId);
    lastSliderValue = sliderValue;
  }
}

int lastKnobValue = 0;
void knobCheck() {
  int knobValue = analogRead(KNOB_PIN);
  int diff = abs(knobValue - lastKnobValue);
  if (diff > 100) {
    int knobEventId = triggerEventStart(valueChange);
    addEventInfo(knobEventId, identification, knobId);
    addEventInfo(knobEventId, timestamp, millis());
    addEventInfo(knobEventId, value, knobValue);
    triggerEventEnd(knobEventId);
    lastKnobValue = knobValue;
  }
}

void loop() {
  sliderCheck();
  knobCheck();
  button.check();
}

void handleEvent(AceButton* /* button */, uint8_t eventType,
    uint8_t buttonState) {

  switch (eventType) {
    case AceButton::kEventPressed:
      int buttonPushId = triggerEventStart(buttonPush);
      addEventInfo(buttonPushId, timestamp, millis());
      triggerEventEnd(buttonPushId);
      break;
    case AceButton::kEventReleased:
      break;
  }
}
