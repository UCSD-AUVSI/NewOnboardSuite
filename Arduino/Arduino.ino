/*==========================================================================================
   Arduino code for camera triggering, gimbal angle reading, and gimbal settings
   For UCSD AUVSI 2015 Competition
   
   The arduino waits for the string "1\n" which causes it to start timed camera triggering.
   
   When triggering it will continuously shoot images at 1 Hz until it receives a stop message
   "0\n" over serial from the OBC.
   
   Immediately after the digitalWrite(HIGH) to trigger image capture, it sends a serial string
   back to the OBC telling it that it took a picture; this should contain gimbal angles as well.
   The OBC will then match the time it receives these messages with telemetry and images.
   
   todo: use AnalogRead with pins for gimbal controller, convert voltages to angles, and
         send back to OBC when an image is taken
*/
 
/*==========================================================================================
   ARDUINO UNO PINS, and SETTINGS
*/

#define	SHOOT_PIN       12      // Trigger Pin

#define TIMER_HALF_PERIOD_MILLISECONDS  500


/*==========================================================================================
   VARIABLES (NOT SETTINGS)
*/

uint8_t flags = 0;

#define FLAG_SHOOT (1<<0)
#define FLAG_TRIGGER_TIMER_STARTED (1<<1)


/*==========================================================================================
   SETUP
*/

void setup()  {
    Serial.begin(19200);
    pinMode(SHOOT_PIN, OUTPUT);
}


/*==========================================================================================
   TRIGGER CAMERA SHOOT 
*/

char shootmsg[256];

void triggerShoot() {
    digitalWrite(SHOOT_PIN, flags & FLAG_SHOOT);
    if(flags & FLAG_SHOOT) {
        memset(shootmsg,0,256);
        sprintf(shootmsg, "shot\n"); //todo: if this Arduino is reading gimbal angles, put them in this message
        Serial.print(shootmsg);
    }
    flags ^= FLAG_SHOOT;
}

/*==========================================================================================
   LOOP
*/
String inputString = "";
int waitloops = 0;

void loop() {
    // Check for confirm start trigger
    while(Serial.available()) {
        char inputChar = Serial.read();
        inputString += inputChar;
        if(inputChar == '\n') {	// Require newline message deliminator at the end of messages
            if(inputString.equals("1\n")) {    // Message received: "1\n"
                flags |= FLAG_TRIGGER_TIMER_STARTED; //enable triggering by setting flag bit to 1
                inputString = "";
            }
            if(inputString.equals("0\n")) {    // Message received: "0\n"
                flags &= (~FLAG_TRIGGER_TIMER_STARTED); //disable triggering by setting flag bit to 0
                inputString = "";
            }
        }
    }
    
    waitloops++;
    if(waitloops >= TIMER_HALF_PERIOD_MILLISECONDS) {
        if(flags & FLAG_TRIGGER_TIMER_STARTED) {
            triggerShoot();
        }
        waitloops = 0;
    }
    delay(1); //wait one millisecond
}






