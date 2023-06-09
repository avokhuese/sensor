# Sensor

########################################

The ExtraSensory Dataset

Primary data files (features and labels)

########################################

The ExtraSensory Dataset was collected by
Yonatan Vaizman and Katherine Ellis, with the supervision of Gert Lanckriet.
Department of Electrical and Computer Engineering,
University of California, San Diego.

The dataset is publicly available.
Any usage of the dataset for publications requires citing the official paper that introduced the dataset:
Vaizman, Y., Ellis, K., and Lanckriet, G. "Recognizing Detailed Human Context In-the-Wild from Smartphones and Smartwatches".
IEEE Pervasive Computing, vol. 16, no. 4, October-December 2017, pp. 62-74. doi:10.1109/MPRV.2017.3971131
(In the website, we refer to this original paper as Vaizman2017a)

########################################

Content of the primary data files:
There are 60 'csv.gz' files, one for each participant (user, subject) in the data collection.
Each of these files has filename with the form:
[UUID].features_labels.csv.gz
where each user has a unique (randomly generated) universal user identification (UUID) number.
Each file is a textual CSV file, compressed using the gzip format.

Within every user's CSV file:
-----------------------------
- The first row specifies the columns of the file.
- Every other row refers to an example from the user. The examples are sorted according to the primary key - the timestamp.
- The columns:

-- First column is 'timestamp'. This is represented as standard number of seconds since the epoch.

-- Second, come columns for the extracted features.
   Unavailable features are represented with 'nan'.
   The name of each feature contains reference to the sensor it was extracted from, in the form [sensor_name]:[feature_name].
   The current version contains features from the following sensors, with sensor names:
--- raw_acc: Accelerometer from the phone. The 'raw' version of acceleration (as opposed to the decomposed versions of gravity and user-acceleration).   
--- proc_gyro: Gyroscope from the phone. Processed version of gyroscope measurements (the OS calculates a version that removes drift).
--- raw_magnet: Magnetometer from the phone. Raw version (as opposed to bias-fixed version that the OS also provides).
--- watch_acceleration: Accelerometer from the watch.
--- watch_heading: Heading from the compass on the watch.
--- location: Location services. These features were extracted offline for every example from the sequence of latitude-longitude-altitude updates from the example's minute.
              These features regard only to relative-location (not absolute location in the world) - meaning, they describe variability of movement within the minute.
--- location_quick_features: Location services. These features were calculated on the phone when data was collected. 
                             These are available even in cases that the other location features are not because the user wanted to conceal their absolute location coordinates.
							 These quick features are very simple heuristics that approximate the more thoughtful offline features.
--- audio_naive: Microphone. These naive features are simply averages and standard deviations of the 13 MFCCs from the ~20sec recording window of every example.
--- discrete: Phone-state. These are binary indicators for the state of the phone.
              Notice that time_of_day features are also considered phone-state features (also have prefix 'discrete:'), but their columns appear not right after the other 'discrete' columns.
--- lf_measurements: Various sensors that were recorded in low-frequency (meaning, once per example).

-- Third, come columns for the ground truth labels.
   The values are either 1 (label is relevant for the example), 0 (label is not relevant for the example), or 'nan' (label is considered 'missing' for this example).
   Originally, users could only report 'positive' labels (in the original ExtraSensory paper, Vaizman2017a, we assumed that when a label was not reported it is a 'negative' example).
   This cleaned version of the labels has the notion of 'missing labels'; Details about how we inferred missing label information is provided in the second paper, Vaizman2017b (see http://extrasensory.ucsd.edu for updated references).
   The names of the labels have prefix 'label:'. After the prefix:
   If the label name is all capitalized, it is an original label from the mobile app's interface and the values were taken from what the user originally reported.
   If the label name begins with 'FIX_', this is a fixes/cleaned version of a corresponding label, meaning that the researchers fixed some of the values that were reported by users because of inconsistencies.
   If the label name begins with 'OR_', this is a synthesized label, meaning it did not appear in the app's label menu, but rather the researchers created it as combination (using logical or) of other related labels.
   If the label name begins with 'LOC_', this is a fixed/cleaned version of a corresponding label that was fixed by researchers based on absolute location.
      LOC_beach was based on original label 'AT_THE_BEACH'.
	  LOC_home was based on original label 'AT_HOME'.
	  LOC_main_workplace was based on original label 'AT_WORK'.

-- Fourth, the last column is label_source, describing where the original labeling came from in the mobile app's interface. It has 8 possible values:
   -1: The user did not report any labels for this example (notice, however, that this example may still have labeling for the 'LOC_' labels).
   0 : The user used the 'active feedback' interface (reporting immediate future). This example is the first in relevant minute sequence.
   1 : The user used the 'active feedback' interface. This example is a continuation of a sequence of minutes since the user started the reported context.
   2 : The user used the history interface to label an example from the past.
   3 : The user replied to a notification that simply asked to provide any labels.
   4 : The user replied to a notification that asked 'In the past [minutes] minutes were you still [recent context]?'. The user replied 'correct' on the phone.
   5 : The user replied to a notification that asked 'In the past [minutes] minutes were you still [recent context]?'. The user replied 'not exactly' and then corrected the context labels.
   6 : The user replied to a notification that asked 'In the past [minutes] minutes were you still [recent context]?'. The user replied 'correct' on the watch interface.


########################################
