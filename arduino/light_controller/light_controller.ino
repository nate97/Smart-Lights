String inputString = "";         // a string to hold incoming data
int led = 0;
boolean stringComplete = false;  // whether the string is complete


void setup() {
  // initialize serial:
  Serial.begin(9600);  
  // reserve 256 bytes for the inputString:
  inputString.reserve(256);
  // initialize the digital pin as an output.
  pinMode(led, OUTPUT);  
}


void loop() {
  // print the string when a newline arrives:
  if (stringComplete) {
    
    inputString.trim();
    
    // Declare the variables of the parts of the data
    String lampID, state;
    
    // For loop which will separate the String in parts
    // and assign them the the variables we declare
    for (int i = 0; i < inputString.length(); i++) {
      if (inputString.substring(i, i+1) == ":") {
        lampID = inputString.substring(0, i);
        state = inputString.substring(i+1);
        break;
      }
    }
    
    // Define lamp and state integers
    int lampIDInt = lampID.toInt();
    int stateInt = state.toInt();
    
    if (stateInt == 0) {
      digitalWrite(lampIDInt, HIGH);
      Serial.println("Light ON");
    }
    else if (stateInt == 1) {
      digitalWrite(lampIDInt, LOW);
      Serial.println("Light OFF");
    }
    
    // clear the string:
    inputString = "";
    stringComplete = false;
  }
}


/*
  SerialEvent occurs whenever a new data comes in the
 hardware serial RX.  This routine is run between each
 time loop() runs, so using delay inside loop can delay
 response.  Multiple bytes of data may be available.
 */
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read(); 
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    } 
  }
}


