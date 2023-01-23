# Material Study 

In order to run simulations and localize the acoustic emission events, we have to study the specimen material very carefully to compute things like signal velocity through the material, and also understand how the signal travels within the material, which can be affected by the orientation of layers in case of composite materials.  

## Velocity Computation 
The method used to compute the signal velocity is somehow trivial. The procedures go as follows:
- Placing two piezoelectric sensors on the composite structure(wind turbine) with pre-defined distance of $25cm$ 
- Connecting the components as discussed in the acquisition setup section.
- Outside the area between the two sensors, we make $n$ hits using the lead tip of a mechanical pencil.
- Recording the hit data into CSV files for further processing.

→ exp1 figure

To make it easy for me, i have implemented a Signal class in python with different modes one for attenuation, velocity calculation, and localization. Each one has its own feature, but the common attribute among them is the arrival time. It is calculated with AIC method (discussed in next part). We know that:
$$velocity = \frac{distance}{time}$$
By which we can compute the mean velocity of different hits through the following equation:
$$\bar{v}= \frac{1}{n} \sum_{i=1}^{n}\frac{d}{|t_{i,1} -t_{i,2}|}$$
Where,
- $d$ is the distance between the two sensors that equals $25cm$.
- $n$ is the number of hits.
- $t_{i,1}$ is the arrival time of the signal to sensor $1$ from hit $i$
- $t_{i,2}$ is the arrival time of the signal to sensor $2$ from hit $i$

→ vel1 here
We ran the experiment three times, but first we tested the the reading to outliers, like the following figure shows one of the experiments has an outlier reading, so we have to eliminate it.

→ vel2  figure 

The final results  are summed  up in the following table:

| $\bar{v}_1$     | $\bar{v}_2$   | $\bar{v}_3$  |
| -----------| ----------- |-----------|
| $4107.52 m/s$| $3715 m/s$  |  $2740.8 m/s$ |


Clearly, there is slight variations as the we assumed that the blade is linear and we ignored the $y$ component of velocity. In addition, we did not consider the problem of line of sight. The signal is not guaranteed to the take the shortest path between the hit and sensor, it might take a long curved one. After all, the readings fall within the reasonable range based on past tests on the host material, which is carbon fiber.


## Attenuation in the material 

The is section is concerned with how the signal loses its energy through traveling from the source to the sensor. Hence, we can answer a lot of questions regarding the quality of the readings we get from a given hit.

The study can be made through the following procedure:
- Placing a piezoelectric sensor on the composite structure.
-  Drawing a line through the sensor and it has a $i$ marks each one is $d(cm)$ from the previous one.
- Making $i$ hits using the mechanical pencil at each mark 
- Recording the data to CSV files for further processing 

–> exp2 

For this study, we made a $7$ marks equidistant from each other at $5cm$, However, $10$ files were recorded, which means we have a 3 files as noise.
There are variety  of methods to eliminate noise, i have used SNR (signal to noise ratio), and ignoring negative values which excludes the hit $5,8,10$. 

→ att1 

We then compute the amplitude $A_i$(maximum voltage reading in the waveform), and plot $A_i$ against hit $i$ to get a sense of the nature of energy attenuation. 
→ att2                  → att 3

The second sub-figure represents the fitted curve over  the raw data. The exponential curve is given by the following equation.
$$y \approx 5.482 e^{-0.1976}$$
This means , the study verified the exponential decay of the signal energy through the composite structure.
