# Fundamentals of AE
## Introduction 
Acoustic Emission is kind of non-destructive passive testing, where the signal is detected by surface-mounted piezoelectric sensors as opposed to ultrasonic active testing where the signals are emitted through the specimen and transmitted back. To acquire such signals, the component under test is submitted to external stimuli, such as  loads , high pressure, or relatively high temperature. As the damage grows through the component, more energy is released in the process. This kind of testing is generally used for evaluating the structural integrity of certain component to monitor defects like fatigue cracking, fiber break, and corrosion progression through the material. Also, being  non-destructive, AE testing allows large structures to be monitored while they are operating causing minimal disruption.

## Signal Parameters
Analysis of AE data is quite difficult as the number of data point produced from a single test is large. So Extracting features from the waveform allows comparisons between different set of data. 

**Amplitude:** is the greatest measured voltage across the waveform. It is an important parameter as it determines the parts of the wave which will not be included in the analysis (some points do not cross the threshold defined based on the value of the amplitude).

**Time of arrival :**  regarded as the most import feature in the waveform. ToA determines the time that sensor began to sense the wave coming form the AE event. They are some method to compute ToA, like threshold crossing and Akaike information criterion (AIC), but they will be discussed in detail later.

→ wave figure with parameters here

There are some other important signal parameters like: rise time , counts , duration; however, they are irrelevant to the scope of this project. 

## Data Acquisition Setup
The setup is quite easy, just  four sensors placed on a known size grid. When the hit takes place each of the sensor sends its received signal to the corresponding channels to be filtered as some noise might interfere. After that the signal get recorded by a specialized acquisition software to be further exported to CSV  files , for example. This short journey can be summarized by the following figure.

→ setup here


